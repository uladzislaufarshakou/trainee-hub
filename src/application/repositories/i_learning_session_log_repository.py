"""
Interface for the Learning Session Log Repository.

This port defines the contract for operations
on the `LearningSessionLog` time-tracking model.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain import LearningSessionLog
from src.core.exceptions import NoActiveLearningSessionError


class ILearningSessionLogRepository(ABC):
    """
    Abstract base class for learning session log persistence.
    """

    @abstractmethod
    async def add(self, session_log: LearningSessionLog) -> None:
        """
        Adds a new `LearningSessionLog` to the repository.

        :param session_log: The `LearningSessionLog` domain model.
        """
        ...

    @abstractmethod
    async def get_active_session(self, state_id: UUID) -> LearningSessionLog:
        """
        Gets the currently active (end_time=None) session for
        a specific technology state "task card".

        :param state_id: The `TraineeTechnologyState` ID.
        :raises NoActiveLearningSessionError: If no active session is found.
        :return: The `LearningSessionLog` domain model.
        """
        ...

    @abstractmethod
    async def update(self, session_log: LearningSessionLog) -> None:
        """
        Updates an existing `LearningSessionLog` in the repository.

        This is primarily used to set the `end_time` on an
        active session.

        :param session_log: The `LearningSessionLog` with updated data.
        """
        ...

    @abstractmethod
    async def list_for_state(self, state_id: UUID) -> list[LearningSessionLog]:
        """
        Lists all session logs (past and present) for a
        specific technology state "task card".

        :param state_id: The `TraineeTechnologyState` ID.
        :return: A list of `LearningSessionLog` models.
        """
        ...
