"""
Interface for the User Repository.

This port defines the contract for all data persistence
operations related to the `User` domain model.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain import User, Role
from src.core.exceptions import UserNotFoundError


class IUserRepository(ABC):
    """
    Abstract base class for user data persistence.
    """

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User:
        """
        Retrieves a user by their unique ID.

        :param user_id: The UUID of the user.
        :raises UserNotFoundError: If no user with that ID is found.
        :return: The `User` domain model.
        """
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        """
        Retrieves a user by their email address.

        :param email: The user's email address.
        :raises UserNotFoundError: If no user with that email is found.
        :return: The `User` domain model.
        """
        ...

    @abstractmethod
    async def add(self, user: User) -> None:
        """
        Adds a new `User` to the repository.

        :param user: The `User` domain model to add.
        """
        ...

    @abstractmethod
    async def list_by_role(self, *roles: Role) -> list[User]:
        """
        Lists all users that match any of the provided roles.

        :param roles: One or more `Role` enums (e.g., Role.TRAINEE).
        :return: A list of `User` domain models.
        """
        ...

    @abstractmethod
    async def list_trainees_for_mentor(self, mentor_id: UUID) -> list[User]:
        """
        Lists all active trainees assigned to a specific mentor.

        :param mentor_id: The `User` ID of the mentor.
        :return: A list of `User` models (trainees).
        """
        ...
