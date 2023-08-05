"""The goal class."""

from datetime import datetime, date, timedelta
import logging
from typing import Callable, Optional

from remind_me_some.event import Event
from remind_me_some.action import Action


logger = logging.getLogger(__name__)


class Goal(Event):
    """The goal class."""

    def __init__(
            self,
            name: str,
            frequency: timedelta,
            priority: float = 1.0,
            interest_rate: float = 0.05,
            last_completed: Optional[date] = None,
            callback: Optional[Callable] = None,
            is_ready_fn: Optional[Callable] = None,
            is_completed_fn: Optional[Callable] = None,
    ) -> None:
        """Initialize a goal object.

        Goal objects are used to create action objects at some frequency.
        Most of the information given to the goal object is used to create
        new action objects.

        :param name:
            The name of the event.
        :param frequency:
            How often this goal should be completed.
        :param priority:
            The starting priority an action this goal generates
            (for determining its relative importance).
        :param interest_rate:
            The rate that the priority of a generated action grows each
            day it is pushed back past its original due date.
        :param last_completed:
            The date that this goal was last completed.
        :param callback:
            A function to be called when a generated action is run.
        :param is_ready_fn:
            A function to determine if a generated action is ready. If
            nothing is supplied this will default to be on or after the
            action's due date.
        :param is_completed_fn:
            A function to determine if the generated action has been
            completed. If nothing is supplied, this will default to be
            true if the callback has been called at least once.
        """
        super().__init__(
            name=name,
            priority=priority,
            interest_rate=interest_rate,
            callback=callback,
            is_ready_fn=is_ready_fn,
            is_completed_fn=is_completed_fn,
        )
        self._frequency = frequency
        self._last_completed = last_completed

    def make_action(self) -> Action:
        """Generate a new action instance.

        :return: An action object.
        """
        logger.debug(f"Make new action for goal '{self.name}'")
        if self._last_completed is not None:
            due = self._last_completed + self._frequency
        else:
            due = datetime.now().date()

        return Action(
            name=self.name,
            due=due,
            priority=self.priority,
            interest_rate=self._interest_rate,
            callback=self._callback,
            is_ready_fn=Action.is_due,
            is_completed_fn=Action.is_called,
        )

    def mark_as_completed(self) -> None:
        """Set the last completed date to today's date."""
        logger.debug(f"Update last completion of goal '{self.name}'")
        self._last_completed = datetime.now().date()

    @property
    def last_completed(self) -> Optional[date]:
        """Get the date when this goal was last completed.

        :return:
            The last date that this goal was completed or None, if it
            hasn't been completed yet.
        """
        return self._last_completed
