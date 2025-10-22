"""
Interface for the Learning Session Log Repository.

This port defines the contract for operations
on the `LearningSessionLog` time-tracking model.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain import LearningSessionLog
# NoActiveLearningSessionError убрано из импортов,
# т.к. репозиторий не должен принимать решения, он должен
# сообщать о фактах (т.е. возвращать None).


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
    async def find_active_session_by_trainee_id(
        self, trainee_id: UUID
    ) -> LearningSessionLog | None:
        """
        Finds the currently active (end_time=None) session for
        a specific trainee.

        This enforces the business rule that a trainee can only
        have one active session at a time.

        :param trainee_id: The `User` ID of the trainee.
        :return: The `LearningSessionLog` model or None if no
                 active session is found.
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
