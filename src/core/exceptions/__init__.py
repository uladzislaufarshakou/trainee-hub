"""
Exceptions Package

This package exposes all custom domain exceptions for the application.
"""

from .exceptions import (
    DomainError,
    NotFoundError,
    UserNotFoundError,
    TechnologyNotFoundError,
    TraineeTechnologyStateNotFoundError,
    StatusUpdateNotFoundError,
    BusinessRuleError,
    InvalidLearningStateTransitionError,
    TechnologyAlreadyApprovedError,
    NoActiveLearningSessionError,
    LearningSessionAlreadyInProgressError,
)

__all__ = [
    # Base classes (good for catching groups of errors)
    "DomainError",
    "NotFoundError",
    "BusinessRuleError",
    # Specific "Not Found" errors
    "UserNotFoundError",
    "TechnologyNotFoundError",
    "TraineeTechnologyStateNotFoundError",
    "StatusUpdateNotFoundError",
    # Specific "Business Rule" errors
    "InvalidLearningStateTransitionError",
    "TechnologyAlreadyApprovedError",
    "NoActiveLearningSessionError",
    "LearningSessionAlreadyInProgressError",
]
