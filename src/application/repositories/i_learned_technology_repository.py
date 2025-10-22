"""
Interface for the Learned Technology Repository.

This port defines the contract for all data persistence
operations related to the `LearnedTechnology` domain model.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain import LearnedTechnology
from src.core.exceptions import TechnologyNotFoundError


class ILearnedTechnologyRepository(ABC):
    """
    Abstract base class for technology data persistence.
    """

    @abstractmethod
    async def get_by_id(self, technology_id: UUID) -> LearnedTechnology:
        """
        Retrieves a technology by its unique ID.

        :param technology_id: The UUID of the technology.
        :raises TechnologyNotFoundError: If no technology is found.
        :return: The `LearnedTechnology` domain model.
        """
        ...

    @abstractmethod
    async def get_by_name(self, name: str) -> LearnedTechnology:
        """
        Retrieves a technology by its unique, normalized name.

        :param name: The name of the technology (e.g., "python").
        :raises TechnologyNotFoundError: If no technology is found.
        :return: The `LearnedTechnology` domain model.
        """
        ...

    @abstractmethod
    async def add(self, technology: LearnedTechnology) -> None:
        """
        Adds a new `LearnedTechnology` to the repository.

        :param technology: The `LearnedTechnology` domain model.
        """
        ...

    @abstractmethod
    async def list_all(self) -> list[LearnedTechnology]:
        """
        Lists all available technologies in the system.

        :return: A list of `LearnedTechnology` models.
        """
        ...
