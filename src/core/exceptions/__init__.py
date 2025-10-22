"""
Exceptions Package

This package exposes all custom domain exceptions for the application.
It uses ``__all__`` to define the public API.
"""

from .exceptions import (
    DomainError,
    NotFoundError,
    UserNotFoundError,
    TechnologyNotFoundError,
    TraineeTechnologyStateNotFoundError,
    StatusUpdateNotFoundError,
    TechnologyReviewNotFoundError,
    CheckQuestionNotFoundError,
    BusinessRuleError,
    InvalidLearningStateTransitionError,
    TechnologyAlreadyApprovedError,
    NoActiveLearningSessionError,
    LearningSessionAlreadyInProgressError,
)

__all__ = [
    # Base classes
    "DomainError",
    "NotFoundError",
    "BusinessRuleError",
    # "Not Found" errors
    "UserNotFoundError",
    "TechnologyNotFoundError",
    "TraineeTechnologyStateNotFoundError",
    "StatusUpdateNotFoundError",
    "TechnologyReviewNotFoundError",
    "CheckQuestionNotFoundError",
    # "Business Rule" errors
    "InvalidLearningStateTransitionError",
    "TechnologyAlreadyApprovedError",
    "NoActiveLearningSessionError",
    "LearningSessionAlreadyInProgressError",
]
