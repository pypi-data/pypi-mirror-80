"""The action class."""
from datetime import datetime, date, timedelta
from typing import Callable, Optional

from remind_me_some.event import Event


class Action(Event):
    """The action class."""

    def __init__(
            self,
            name: str,
            due: date,
            priority: float,
            interest_rate: float,
            callback: Optional[Callable[[], None]] = None,
            is_ready_fn: Optional[Callable[[], bool]] = None,
            is_completed_fn: Optional[Callable[[], bool]] = None,
    ) -> None:
        """Initialize an action.

        :param name:
            The name of the action.
        :param due:
            The planned date for the action to be completed on.
        :param priority:
            The priority of the action (for determining its relative
            importance).
        :param interest_rate:
            The rate that the priority of the action grows each day it
            is pushed back past its original due date.
        :param callback:
            A function to be called when the action is run.
        :param is_ready_fn:
            A function to determine if the action is ready. If nothing is
            supplied this will default to be on or after the action's due
            date.
        :param is_completed_fn:
            A function to determine if the action has been completed. If
            nothing is supplied, this will default to be true if the
            callback has been called at least once.
        """
        super().__init__(
            name=name,
            priority=priority,
            interest_rate=interest_rate,
            callback=callback,
            is_ready_fn=is_ready_fn,
            is_completed_fn=is_completed_fn,
        )
        self.due: date = due

    def __str__(self) -> str:
        """Return string information for the current action."""
        return (
            f"{super().__str__()}  =>  "
            f"{self.due} ({'READY' if self.is_ready() else 'NOT READY'})"
        )

    def push_forward(self, days: int = 1) -> None:
        """Bump the due date of the current action and add interest.

        :param days: The number of days to bump the due date by.
        """
        self.due += timedelta(days=days)
        super().push_forward(days)

    def is_due(self) -> bool:
        """Check if the current action is due.

        :return:
            True if the current date is the due date or after;
            False, otherwise.
        """
        return datetime.now().date() >= self.due
