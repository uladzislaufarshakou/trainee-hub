"""
This module defines all custom, domain-specific exceptions.

These exceptions are raised by the application service layer when
business rules are violated or domain entities are not found.
The presentation (API) layer is responsible for catching these
and translating them into appropriate HTTP error responses.
"""


class DomainError(Exception):
    """Base class for all domain-specific exceptions."""

    pass


# --- "Not Found" Group ---


class NotFoundError(DomainError):
    """Base class for exceptions raised when a domain entity is not found."""

    def __init__(self, message: str):
        super().__init__(message)


class UserNotFoundError(NotFoundError):
    """Raised when a User is not found."""

    pass


class TechnologyNotFoundError(NotFoundError):
    """Raised when a LearnedTechnology is not found."""

    pass


class TraineeTechnologyStateNotFoundError(NotFoundError):
    """Raised when a TraineeTechnologyState is not found."""

    pass


class StatusUpdateNotFoundError(NotFoundError):
    """Raised when a StatusUpdate is not found."""

    pass


# --- "Business Rule" Group ---


class BusinessRuleError(DomainError):
    """
    Base class for exceptions raised when a business rule is violated.
    """

    def __init__(self, message: str):
        super().__init__(message)


class InvalidLearningStateTransitionError(BusinessRuleError):
    """
    Raised when a `TraineeTechnologyState` transition is not allowed.
    (e.g., from PLANNED to APPROVED).
    """

    def __init__(self, from_state: str, to_state: str):
        self.from_state = from_state
        self.to_state = to_state
        message = f"Cannot transition from {from_state} to {to_state}."
        super().__init__(message)


class TechnologyAlreadyApprovedError(BusinessRuleError):
    """
    Raised when an action is attempted on a technology state
    that is already in the APPROVED state.
    """

    pass


class NoActiveLearningSessionError(BusinessRuleError):
    """
    Raised when trying to stop a `LearningSessionLog`, but no
    active (end_time=None) session is found for that task.
    """

    pass


class LearningSessionAlreadyInProgressError(BusinessRuleError):
    """
    Raised when trying to start a new `LearningSessionLog` for a task
    that already has an active session (end_time=None).
    """

    pass
