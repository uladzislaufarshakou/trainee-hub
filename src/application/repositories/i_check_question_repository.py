"""
Interface for a repository that manages `CheckQuestion` entities.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain import CheckQuestion
from src.core.exceptions import CheckQuestionNotFoundError


class ICheckQuestionRepository(ABC):
    """
    Abstract contract for managing the question bank.
    """

    @abstractmethod
    async def add(self, question: CheckQuestion) -> CheckQuestion:
        """
        Adds a new question to the repository.

        :param question: The `CheckQuestion` domain model to add.
        :return: The added `CheckQuestion`.
        """
        ...

    @abstractmethod
    async def get_by_id(self, question_id: UUID) -> CheckQuestion:
        """
        Gets a question by its unique ID.

        :param question_id: The ID of the question.
        :return: The `CheckQuestion` domain model.
        :raises CheckQuestionNotFoundError: If the question is not found.
        """
        ...

    @abstractmethod
    async def list_by_technology_id(self, technology_id: UUID) -> list[CheckQuestion]:
        """
        Gets a list of all active questions for a specific technology.

        :param technology_id: The ID of the `LearnedTechnology`.
        :return: A list of `CheckQuestion` domain models.
        """
        ...

    @abstractmethod
    async def update(self, question: CheckQuestion) -> CheckQuestion:
        """
        Updates an existing question (e.g., text or active status).

        :param question: The `CheckQuestion` domain model with updated data.
        :return: The updated `CheckQuestion`.
        :raises CheckQuestionNotFoundError: If the question is not found.
        """
        ...
