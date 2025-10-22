"""
Interface for a repository that manages `CheckQuestionResult` entities.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain import CheckQuestionResult


class ICheckQuestionResultRepository(ABC):
    """
    Abstract contract for managing the results of a check.
    """

    @abstractmethod
    async def add_batch(
        self, results: list[CheckQuestionResult]
    ) -> list[CheckQuestionResult]:
        """
        Adds a batch of question results from a single review.
        This should be done in a transaction.

        :param results: A list of `CheckQuestionResult` domain models.
        :return: The list of added `CheckQuestionResult` models.
        """
        ...

    @abstractmethod
    async def list_by_review_id(self, review_id: UUID) -> list[CheckQuestionResult]:
        """
        Gets all question results associated with a single review.

        :param review_id: The ID of the `TechnologyReview`.
        :return: A list of `CheckQuestionResult` models.
        """
        ...
