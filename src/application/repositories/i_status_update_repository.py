"""
Interface for the Status Update Repository.

This port defines the contract for operations
on the `StatusUpdate` daily log model.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain import StatusUpdate
from src.core.exceptions import StatusUpdateNotFoundError


class IStatusUpdateRepository(ABC):
    """
    Abstract base class for status update persistence.
    """

    @abstractmethod
    async def get_by_id(self, status_id: UUID) -> StatusUpdate:
        """
        Retrieves a status update by its unique ID.

        :param status_id: The UUID of the status update.
        :raises StatusUpdateNotFoundError: If no entry is found.
        :return: The `StatusUpdate` domain model.
        """
        ...

    @abstractmethod
    async def add(self, status: StatusUpdate) -> None:
        """
        Adds a new `StatusUpdate` to the repository.

        :param status: The `StatusUpdate` domain model.
        """
        ...

    @abstractmethod
    async def update(self, status: StatusUpdate) -> None:
        """
        Updates an existing `StatusUpdate`.

        This is primarily used by the LLM worker to add
        the summary and metrics after processing.

        :param status: The `StatusUpdate` model with updated data.
        """
        ...

    @abstractmethod
    async def list_by_trainee_id(self, trainee_id: UUID) -> list[StatusUpdate]:
        """
        Lists all status updates for a specific trainee.

        :param trainee_id: The `User` ID of the trainee.
        :return: A list of `StatusUpdate` models.
        """
        ...
