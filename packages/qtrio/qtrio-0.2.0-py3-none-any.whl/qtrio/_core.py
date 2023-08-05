"""The module holding the core features of QTrio.

Attributes:
    _reenter_event_type: The event type enumerator for our reenter events.
"""
import contextlib
import functools
import math
import sys
import traceback
import typing

import async_generator
import attr
import outcome
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets
import trio
import trio.abc

import qtrio
import qtrio._qt
import qtrio._util

_reenter_event_type: typing.Optional[QtCore.QEvent.Type] = None


def registered_event_type() -> typing.Optional[QtCore.QEvent.Type]:
    """Get the registered event type.

    Returns:
        The type registered with Qt for the reenter event.  :obj:`None` if no event type
        has been registered yet.
    """
    return _reenter_event_type


def register_event_type() -> None:
    """Register a Qt event type for use by Trio to reenter into the Qt event loop.

    Raises:
        qtrio.EventTypeAlreadyRegisteredError: if an event type has already been
            registered.
        qtrio.EventTypeRegistrationFailedError:  if a type was not able to be
            registered.
    """
    global _reenter_event_type

    if _reenter_event_type is not None:
        raise qtrio.EventTypeAlreadyRegisteredError()

    event_hint = QtCore.QEvent.registerEventType()

    if event_hint == -1:
        raise qtrio.EventTypeRegistrationFailedError()

    # assign to the global
    _reenter_event_type = QtCore.QEvent.Type(event_hint)


def register_requested_event_type(
    requested_value: typing.Union[int, QtCore.QEvent.Type]
) -> None:
    """Register the requested Qt event type for use by Trio to reenter into the Qt event
    loop.

    Arguments:
        requested_value: The value to ask Qt to use for the event type being registered.

    Raises:
        qtrio.EventTypeAlreadyRegisteredError: if an event type has already been
            registered.
        qtrio.EventTypeRegistrationFailedError: if a type was not able to be registered.
        qtrio.RequestedEventTypeUnavailableError: if the type returned by Qt does not
            match the requested type.
    """
    global _reenter_event_type

    if _reenter_event_type is not None:
        raise qtrio.EventTypeAlreadyRegisteredError()

    event_hint = QtCore.QEvent.registerEventType(requested_value)

    if event_hint == -1:
        raise qtrio.EventTypeRegistrationFailedError()
    elif event_hint != requested_value:
        raise qtrio.RequestedEventTypeUnavailableError(
            requested_type=requested_value, returned_type=event_hint
        )

    # assign to the global
    _reenter_event_type = QtCore.QEvent.Type(event_hint)


class ReenterEvent(QtCore.QEvent):
    """A proper ``ReenterEvent`` for reentering into the Qt host loop."""

    def __init__(self, fn: typing.Callable[[], object]):
        super().__init__(_reenter_event_type)
        self.fn = fn


class Reenter(QtCore.QObject):
    """A ``QtCore.QObject`` for handling reenter events."""

    def event(self, event: QtCore.QEvent) -> bool:
        """Qt calls this when the object receives an event."""

        reenter_event = typing.cast(Reenter, event)
        reenter_event.fn()
        return False


async def wait_signal(signal: qtrio._util.SignalInstance) -> typing.Tuple[object, ...]:
    """Block for the next emission of ``signal`` and return the emitted arguments.

    Warning:
        In many cases this can result in a race condition since you are unable to
        first connect the signal and then wait for it.

    Args:
        signal: The signal instance to wait for emission of.

    Returns:
        A tuple containing the values emitted by the signal.
    """
    event = trio.Event()
    result: typing.Tuple[object, ...] = ()

    def slot(*args: object) -> None:
        """Receive and store the emitted arguments and set the event so we can continue.

        Args:
            args: The arguments emitted from the signal.
        """
        nonlocal result
        result = args
        event.set()

    with qtrio._qt.connection(signal, slot):
        await event.wait()

    return result


@attr.s(auto_attribs=True, frozen=True, slots=True, eq=False)
class Emission:
    """Stores the emission of a signal including the emitted arguments.  Can be
    compared against a signal instance to check the source.  Do not construct this class
    directly.  Instead, instances will be received through a channel created by
    :func:`qtrio.enter_emissions_channel`.

    Note:
        Each time you access a signal such as ``a_qobject.some_signal`` you get a
        different signal instance object so the ``signal`` attribute generally will not
        be the same object.  A signal instance is a ``QtCore.SignalInstance`` in
        PySide2 or ``QtCore.pyqtBoundSignal`` in PyQt5.
    """

    signal: qtrio._util.SignalInstance
    """An instance of the original signal."""
    args: typing.Tuple[object, ...]
    """A tuple of the arguments emitted by the signal."""

    def is_from(self, signal: qtrio._util.SignalInstance) -> bool:
        """Check if this emission came from ``signal``.

        Args:
            signal: The signal instance to check for being the source.

        Returns:
            Whether the passed signal was the source of this emission.
        """

        # bool() to accomodate SignalInstance being typed Any right now...
        return bool(self.signal == signal)

    def __eq__(self, other: object) -> bool:
        if type(other) != type(self):
            return False

        # TODO: workaround for https://github.com/python/mypy/issues/4445
        if not isinstance(other, type(self)):  # pragma: no cover
            return False

        return self.is_from(signal=other.signal) and self.args == other.args


@attr.s(auto_attribs=True)
class Emissions:
    """Hold elements useful for the application to work with emissions from signals.
    Do not construct this class directly.  Instead, use
    :func:`qtrio.enter_emissions_channel`.
    """

    channel: trio.MemoryReceiveChannel
    """A memory receive channel to be fed by signal emissions."""
    send_channel: trio.MemorySendChannel
    """A memory send channel collecting signal emissions."""

    async def aclose(self) -> None:
        """Asynchronously close the send channel when signal emissions are no longer of
        interest.
        """
        await self.send_channel.aclose()


@async_generator.asynccontextmanager
async def open_emissions_channel(
    signals: typing.Collection[qtrio._util.SignalInstance],
    max_buffer_size: typing.Union[int, float] = math.inf,
) -> typing.AsyncGenerator[Emissions, None]:
    """Create a memory channel fed by the emissions of the signals.  Each signal
    emission will be converted to a :class:`qtrio.Emission` object.  On exit the send
    channel is closed.  Management of the receive channel is left to the caller.

    Note:
        Use this only if you need to process emissions *after* exiting the context
        manager.  Otherwise use :func:`qtrio.enter_emissions_channel`.

    Args:
        signals: A collection of signals which will be monitored for emissions.
        max_buffer_size: When the number of unhandled emissions in the channel reaches
            this limit then additional emissions will be silently thrown out the window.

    Returns:
        The emissions manager with the signals connected to it.
    """

    # Infinite buffer because I don't think there's any use in storing the emission
    # info in a `slot()` stack frame rather than in the memory channel.  Perhaps in the
    # future we can implement a limit beyond which events are thrown away to avoid
    # infinite queueing.  Maybe trio.MemorySendChannel.send_nowait() instead.
    send_channel, receive_channel = trio.open_memory_channel(
        max_buffer_size=max_buffer_size
    )

    async with send_channel:
        with contextlib.ExitStack() as stack:
            for signal in signals:

                def slot(
                    *args: object, internal_signal: qtrio._util.SignalInstance = signal
                ) -> None:
                    try:
                        send_channel.send_nowait(
                            Emission(signal=internal_signal, args=args)
                        )
                    except trio.WouldBlock:
                        # TODO: log this or... ?
                        pass

                stack.enter_context(qtrio._qt.connection(signal, slot))

            yield Emissions(channel=receive_channel, send_channel=send_channel)


@async_generator.asynccontextmanager
async def enter_emissions_channel(
    signals: typing.Collection[qtrio._util.SignalInstance],
    max_buffer_size: typing.Union[int, float] = math.inf,
) -> typing.AsyncGenerator[Emissions, None]:
    """Create a memory channel fed by the emissions of the signals and enter both the
    send and receive channels' context managers.

    Args:
        signals: A collection of signals which will be monitored for emissions.
        max_buffer_size: When the number of unhandled emissions in the channel reaches
            this limit then additional emissions will be silently thrown out the window.

    Returns:
        The emissions manager.
    """
    async with open_emissions_channel(
        signals=signals, max_buffer_size=max_buffer_size
    ) as emissions:
        async with emissions.channel:
            async with emissions.send_channel:
                yield emissions


@attr.s(auto_attribs=True)
class EmissionsNursery:
    """Holds the nursery, exit stack, and wrapper needed to support connecting signals
    to both async and sync slots in the nursery.
    """

    nursery: trio.Nursery
    """The Trio nursery that will handle execution of the slots."""
    exit_stack: contextlib.ExitStack
    """The exit stack that will manage the connections so they get disconnected."""
    wrapper: typing.Optional[
        typing.Callable[
            [typing.Callable[..., typing.Awaitable[object]]],
            typing.Awaitable[object],
        ]
    ] = None
    """The wrapper for handling the slots.  This could, for example, handle exceptions
    and present a dialog to avoid cancelling the entire nursery.
    """

    def connect(
        self,
        signal: qtrio._util.SignalInstance,
        slot: typing.Callable[..., typing.Awaitable[object]],
    ) -> None:
        """Connect to an async slot to this emissions nursery so when called the slot
        will be run in the nursery.
        """
        if self.wrapper is not None:

            def starter(*args: object) -> None:
                self.nursery.start_soon(self.wrapper, slot, *args)

        else:

            def starter(*args: object) -> None:
                self.nursery.start_soon(slot, *args)

        self.exit_stack.enter_context(qtrio._qt.connection(signal, starter))

    def connect_sync(
        self, signal: qtrio._util.SignalInstance, slot: typing.Callable[..., object]
    ) -> None:
        """Connect to a sync slot to this emissions nursery so when called the slot will
        be run in the nursery.
        """

        async def async_slot(*args: object) -> None:
            slot(*args)

        self.connect(signal=signal, slot=async_slot)


@async_generator.asynccontextmanager
async def open_emissions_nursery(
    until: typing.Optional[qtrio._util.SignalInstance] = None,
    wrapper: typing.Optional[typing.Callable[..., typing.Awaitable[object]]] = None,
) -> typing.AsyncGenerator[EmissionsNursery, None]:
    """Open a nursery for handling callbacks triggered by signal emissions.  This allows
    a 'normal' Qt callback structure while still executing the callbacks within a Trio
    nursery such that errors have a place to go.  Both async and sync callbacks can be
    connected.  Sync callbacks will be wrapped in an async call to allow execution in
    the nursery.

    Arguments:
        until: Keep the nursery open until this signal is emitted.
        wrapper: A wrapper for the callbacks such as to process exceptions.

    Returns:
        The emissions manager.
    """
    async with trio.open_nursery() as nursery:
        with contextlib.ExitStack() as exit_stack:
            emissions_nursery = EmissionsNursery(
                nursery=nursery,
                exit_stack=exit_stack,
                wrapper=wrapper,
            )

            if until is not None:
                async with wait_signal_context(until):
                    yield emissions_nursery
            else:
                yield emissions_nursery


@async_generator.asynccontextmanager
async def wait_signal_context(
    signal: qtrio._util.SignalInstance,
) -> typing.AsyncGenerator[None, None]:
    """Connect a signal during the context and wait for it on exit.  Presently no
    mechanism is provided for retrieving the emitted arguments.

    Args:
        signal: The signal to connect to and wait for.
    """
    event = trio.Event()

    def slot(*args: object, **kwargs: object) -> None:
        event.set()

    with qtrio._qt.connection(signal=signal, slot=slot):
        yield
        await event.wait()


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Outcomes:
    """This class holds an :class:`outcome.Outcome` from each of the Trio and the Qt
    application execution.  Do not construct instances directly.  Instead, an instance
    will be returned from :func:`qtrio.run` or available on instances of
    :attr:`qtrio.Runner.outcomes`.
    """

    qt: typing.Optional[outcome.Outcome] = None
    """The Qt application :class:`outcome.Outcome`"""
    trio: typing.Optional[outcome.Outcome] = None
    """The Trio async function :class:`outcome.Outcome`"""

    def unwrap(self) -> object:
        """Unwrap either the Trio or Qt outcome.  First, errors are given priority over
        success values.  Second, the Trio outcome gets priority over the Qt outcome.

        Returns:
            Whatever captured value was selected.

        Raises:
            Exception: Whatever captured exception was selected.
            qtrio.NoOutcomesError: if no value or exception has been captured.
        """

        if self.trio is not None:
            # highest priority to the Trio outcome, if it is an error we are done
            result = self.trio.unwrap()

            # since a Trio result is higher priority, we only care if Qt gave an error
            if self.qt is not None:
                self.qt.unwrap()

            # no Qt error so go ahead and return the Trio result
            return result
        elif self.qt is not None:
            # either it is a value that gets returned or an error that gets raised
            return self.qt.unwrap()

        # neither Trio nor Qt outcomes have been set so we have nothing to unwrap()
        raise qtrio.NoOutcomesError()


def run(
    async_fn: typing.Callable[[], typing.Awaitable[None]],
    *args: object,
    done_callback: typing.Optional[typing.Callable[[Outcomes], None]] = None,
    clock: trio.abc.Clock = None,
) -> Outcomes:
    """Run a Trio-flavored async function in guest mode on a Qt host application, and
    return the outcomes.

    Args:
        async_fn: The async function to run.
        args: Positional arguments to pass to `async_fn`.
        done_callback: See :class:`qtrio.Runner.done_callback`.
        clock: See :class:`qtrio.Runner.clock`.

    Returns:
        The :class:`qtrio.Outcomes` with both the Trio and Qt outcomes.
    """
    runner = Runner(done_callback=done_callback, clock=clock)
    runner.run(async_fn, *args)

    return runner.outcomes


def outcome_from_application_return_code(return_code: int) -> outcome.Outcome:
    """Create either an :class:`outcome.Value` in the case of a 0 `return_code` or an
    :class:`outcome.Error` with a :class:`ReturnCodeError` otherwise.

    Args:
        return_code: The return code to be processed.

    Returns:
        The outcome wrapping the passed in return code.
    """

    if return_code == 0:
        return outcome.Value(return_code)

    return outcome.Error(qtrio.ReturnCodeError(return_code))


def build_application() -> QtGui.QGuiApplication:
    application = QtWidgets.QApplication(sys.argv[1:])
    application.setQuitOnLastWindowClosed(False)

    return application


@attr.s(auto_attribs=True, slots=True)
class Runner:
    """This class helps run Trio in guest mode on a Qt host application."""

    application: QtGui.QGuiApplication = attr.ib(factory=build_application)
    """The Qt application object to run as the host.  If not set before calling
    :meth:`run` the application will be created as
    ``QtWidgets.QApplication(sys.argv[1:])`` and ``.setQuitOnLastWindowClosed(False)``
    will be called on it to allow the application to continue throughout the lifetime of
    the async function passed to :meth:`qtrio.Runner.run`.
    """
    quit_application: bool = True
    """When true, the :meth:`done_callback` method will quit the application when the
    async function passed to :meth:`qtrio.Runner.run` has completed.
    """
    timeout: typing.Optional[float] = None
    """If not :obj:`None`, use :func:`trio.move_on_after()` to cancel after ``timeout``
    seconds and raise.
    """
    clock: trio.abc.Clock = None
    """The clock to use for this run.  This is primarily used to speed up tests that
    include timeouts.  The value will be passed on to
    :func:`trio.lowlevel.start_guest_run`.
    """

    reenter: Reenter = attr.ib(factory=Reenter)
    """The :class:`QtCore.QObject` instance which will receive the events requesting
    execution of the needed Trio and user code in the host's event loop and thread.
    """

    done_callback: typing.Optional[typing.Callable[[Outcomes], None]] = attr.ib(
        default=None
    )
    """The builtin :meth:`done_callback` will be passed to
    :func:`trio.lowlevel.start_guest_run` but will call the callback passed here before
    (maybe) quitting the application.  The :class:`outcome.Outcome` from the completion
    of the async function passed to :meth:`run` will be passed to this callback.
    """

    outcomes: Outcomes = attr.ib(factory=Outcomes, init=False)
    """The outcomes from the Qt and Trio runs."""
    cancel_scope: trio.CancelScope = attr.ib(default=None, init=False)
    """An all encompassing cancellation scope for the Trio execution."""

    _done: bool = attr.ib(default=False, init=False)
    """Just an indicator that the run is done.  Presently used only for a test."""

    def run(
        self,
        async_fn: typing.Callable[[], typing.Awaitable[object]],
        *args: object,
        execute_application: bool = True,
    ) -> Outcomes:
        """Start the guest loop executing ``async_fn``.

        Args:
            async_fn: The async function to be run in the Qt host loop by the Trio
                guest.
            args: Arguments to pass when calling ``async_fn``.
            execute_application: If True, the Qt application will be executed and this
                call will block until it finishes.

        Returns:
            If ``execute_application`` is true, a :class:`qtrio.Outcomes` containing
            outcomes from the Qt application and ``async_fn`` will be returned.
            Otherwise, an empty :class:`qtrio.Outcomes`.
        """
        if _reenter_event_type is None:
            register_event_type()

        trio.lowlevel.start_guest_run(
            self.trio_main,
            async_fn,
            args,
            run_sync_soon_threadsafe=self.run_sync_soon_threadsafe,
            done_callback=self.trio_done,
            clock=self.clock,
        )

        if execute_application:
            return_code = self.application.exec_()

            self.outcomes = attr.evolve(
                self.outcomes,
                qt=outcome_from_application_return_code(return_code),
            )

        return self.outcomes

    def run_sync_soon_threadsafe(self, fn: typing.Callable[[], object]) -> None:
        """Helper for the Trio guest to execute a sync function in the Qt host
        thread when called from the Trio guest thread.  This call will not block waiting
        for completion of ``fn`` nor will it return the result of calling ``fn``.

        Args:
            fn: A no parameter callable.
        """
        event = ReenterEvent(fn=fn)
        self.application.postEvent(self.reenter, event)

    async def trio_main(
        self,
        async_fn: typing.Callable[..., typing.Awaitable[object]],
        args: typing.Tuple[object, ...],
    ) -> object:
        """Will be run as the main async function by the Trio guest.  It creates a
        cancellation scope to be cancelled when
        :meth:`QtGui.QGuiApplication.lastWindowClosed` is emitted.  Within this scope
        the application's ``async_fn`` will be run and passed ``args``.

        Args:
            async_fn: The application's main async function to be run by Trio in the Qt
                host's thread.
            args: Positional arguments to be passed to ``async_fn``

        Returns:
            The result returned by `async_fn`.
        """
        result: object = None
        timeout_cancel_scope = None

        try:
            with trio.CancelScope() as self.cancel_scope:
                with contextlib.ExitStack() as exit_stack:
                    if self.application.quitOnLastWindowClosed():
                        exit_stack.enter_context(
                            qtrio._qt.connection(
                                signal=self.application.lastWindowClosed,
                                slot=self.cancel_scope.cancel,
                            )
                        )
                    if self.timeout is not None:
                        timeout_cancel_scope = exit_stack.enter_context(
                            trio.fail_after(self.timeout)
                        )

                    result = await async_fn(*args)
        except trio.TooSlowError as e:
            if (
                timeout_cancel_scope is not None
                and timeout_cancel_scope.cancelled_caught
            ):
                raise qtrio.RunnerTimedOutError() from e

            raise

        return result

    def trio_done(self, run_outcome: outcome.Outcome) -> None:
        """Will be called after the Trio guest run has finished.  This allows collection
        of the :class:`outcome.Outcome` and execution of any application provided done
        callback.  Finally, if :attr:`qtrio.Runner.quit_application` was set when
        creating the instance then the Qt application will be requested to quit.

        Actions such as outputting error information or unwrapping the outcomes need
        to be further considered.

        Arguments:
            run_outcome: The outcome of the Trio guest run.
        """
        self.outcomes = attr.evolve(self.outcomes, trio=run_outcome)

        if self.done_callback is not None:
            self.done_callback(self.outcomes)

        if self.quit_application:
            self.application.quit()

        self._done = True
