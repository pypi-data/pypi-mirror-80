"""The event class."""

import logging
from typing import Any, Callable, Optional


logger = logging.getLogger(__name__)


class Event:
    """The event class."""

    def __init__(
            self,
            name: str,
            priority: float,
            interest_rate: float,
            callback: Optional[Callable[[], None]] = None,
            is_ready_fn: Optional[Callable[[], bool]] = None,
            is_completed_fn: Optional[Callable[[], bool]] = None,
    ) -> None:
        """Initialize an event.

        :param name:
            The name of the event.
        :param priority:
            The priority of the event (for determining its relative
            importance).
        :param interest_rate:
            The rate that the priority of the event grows each step it
            is pushed back past its original due date.
        :param callback:
            A function to be called when the event is run.
        :param is_ready_fn:
            A function to determine if the event is ready. If nothing is
            supplied, this will default to be true if the event has not
            been completed.
        :param is_completed_fn:
            A function to determine if the event has been completed. If
            nothing is supplied, this will default to be true if the
            callback has been called at least once.
        """
        if priority <= 0:
            raise ValueError("Priority must be a positive number")
        if interest_rate < 0:
            raise ValueError("Interest should be a non-negative number")
        if is_ready_fn is None:
            is_ready_fn = self.is_due
        if is_completed_fn is None:
            is_completed_fn = self.is_called
        self.name: str = name
        self.priority: float = priority
        self._interest_rate: float = interest_rate
        self._callback: Optional[Callable] = callback
        self._is_ready_fn: Callable = is_ready_fn
        self._is_completed_fn: Callable = is_completed_fn

        self._callback_count: int = 0

    def __str__(self) -> str:
        """Get a string with details of the current event."""
        return f"{self.name:<15} (priority={self.priority:.2f})"

    def __eq__(self, other):
        """Check if two events are the same by comparing their names."""
        return self.name == other.name

    def push_forward(self, steps: int = 1) -> None:
        """Increase the priority of event by applying interest.

        :param steps:
            The number of times to apply the interest rate to the event's
            priority.
        """
        logger.debug(f"Push forward '{self.name}' by {steps} steps")
        if steps < 1:
            raise ValueError('Must push forward a positive number of steps')
        self.priority *= (1 + self._interest_rate) ** steps

    def is_due(self) -> bool:
        """Check if the event is due.

        :return:
            True if the completion function doesn't return true;
            false otherwise.
        """
        return not self.is_completed()

    def is_called(self) -> bool:
        """Check if the event has been called.

        :return:
            True if the callback has been called at least once;
            false otherwise.
        """
        return self._callback_count > 0

    def callback(self) -> Any:
        """Call the event's callback.

        :return: Whatever the callback returns.
        """
        logger.debug(f"Call callback for '{self.name}'")
        if self.is_ready():
            self._callback_count += 1
            if callable(self._callback):
                return self._try_run_args(self._callback)
        else:
            raise RuntimeError(
                f"Callback '{self.name}' called before it's ready")

    def is_ready(self) -> bool:
        """Check if an event is ready.

        :return:
            True if the ready function returns true and the event
            has not been completed; false otherwise.
        """
        return (
            self._try_run_args(self._is_ready_fn)
            and not self.is_completed()
        )

    def is_completed(self) -> bool:
        """Check if an event has been completed.

        :return:
            True if the is completed function returns true; false
            otherwise.
        """
        return self._try_run_args(self._is_completed_fn)

    def _try_run_args(self, fn) -> Any:
        """Try calling a function with and without the self arguement."""
        try:
            return fn()
        except TypeError:
            pass
        try:
            return fn(self)
        except TypeError:
            pass

        raise TypeError("Function could not be run")
