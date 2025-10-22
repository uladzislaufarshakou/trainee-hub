"""
Interface for the Trainee Technology State Repository.

This is a critical port defining the contract for operations
on the `TraineeTechnologyState` "task card" model.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain import TraineeTechnologyState, LearningState
from src.core.exceptions import TraineeTechnologyStateNotFoundError


class ITraineeTechnologyStateRepository(ABC):
    """
    Abstract base class for trainee technology state persistence.
    """

    @abstractmethod
    async def get_by_id(self, state_id: UUID) -> TraineeTechnologyState:
        """
        Retrieves a technology state "task card" by its unique ID.

        :param state_id: The UUID of the state entry.
        :raises TraineeTechnologyStateNotFoundError: If no entry is found.
        :return: The `TraineeTechnologyState` domain model.
        """
        ...

    @abstractmethod
    async def find_by_trainee_and_technology(
        self, trainee_id: UUID, technology_id: UUID
    ) -> TraineeTechnologyState | None:
        """
        Finds a technology state "task card" by its business key
        (trainee + technology).

        :param trainee_id: The `User` ID of the trainee.
        :param technology_id: The `LearnedTechnology` ID.
        :return: The `TraineeTechnologyState` model or None if not found.
        """
        ...

    @abstractmethod
    async def add(self, state: TraineeTechnologyState) -> None:
        """
        Adds a new `TraineeTechnologyState` to the repository.

        :param state: The `TraineeTechnologyState` domain model.
        """
        ...

    @abstractmethod
    async def update(self, state: TraineeTechnologyState) -> None:
        """
        Updates an existing `TraineeTechnologyState` in the repository.

        Implementations should use the `state.id` to find and
        update the record.

        :param state: The `TraineeTechnologyState` model with updated data.
        """
        ...

    @abstractmethod
    async def list_by_trainee_id(
        self, trainee_id: UUID
    ) -> list[TraineeTechnologyState]:
        """
        Lists all technology states for a specific trainee.

        :param trainee_id: The `User` ID of the trainee.
        :return: A list of `TraineeTechnologyState` models.
        """
        ...

    @abstractmethod
    async def list_by_mentor_id_and_states(
        self, mentor_id: UUID, states: list[LearningState]
    ) -> list[TraineeTechnologyState]:
        """
        Lists all technology states assigned to a mentor that
        match one of the provided states.

        (e.g., list all tasks "READY_FOR_REVIEW" for a mentor)

        :param mentor_id: The `User` ID of the mentor.
        :param states: A list of `LearningState` enums to filter by.
        :return: A list of `TraineeTechnologyState` models.
        """
        ...
