"""
Interface for the Technology Review Repository.

This port defines the contract for operations
on the `TechnologyReview` audit log model.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain import TechnologyReview


class ITechnologyReviewRepository(ABC):
    """
    Abstract base class for technology review log persistence.
    """

    @abstractmethod
    async def add(self, review: TechnologyReview) -> None:
        """
        Adds a new `TechnologyReview` log to the repository.

        :param review: The `TechnologyReview` domain model.
        """
        ...

    @abstractmethod
    async def list_for_state(self, state_id: UUID) -> list[TechnologyReview]:
        """
        Lists all review logs for a specific
        technology state "task card".

        :param state_id: The `TraineeTechnologyState` ID.
        :return: A list of `TechnologyReview` models.
        """
        ...
