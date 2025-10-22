"""
Interface for the Status Feedback Repository.

This port defines the contract for operations
on the `StatusFeedback` (comment) model.
"""

from abc import ABC, abstractmethod

from src.core.domain import StatusFeedback


class IStatusFeedbackRepository(ABC):
    """
    Abstract base class for status feedback persistence.
    """

    @abstractmethod
    async def add(self, feedback: StatusFeedback) -> None:
        """
        Adds a new `StatusFeedback` comment to the repository.

        :param feedback: The `StatusFeedback` domain model.
        """
        ...

    @abstractmethod
    async def list_for_status(self, status_id: UUID) -> list[StatusFeedback]:
        """
        Lists all feedback comments for a specific `StatusUpdate`.

        :param status_id: The `StatusUpdate` ID.
        :return: A list of `StatusFeedback` models.
        """
        ...
