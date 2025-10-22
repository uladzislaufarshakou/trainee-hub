"""
Domain Models Package

This package defines the public API for the core domain models.

It imports all models from the ``models`` module and exposes
them directly at the package level (e.g., ``from src.core.domain import User``).

The ``__all__`` list is used to explicitly define which models
are part of this public API, enabling clean imports and
controlling wildcard imports.
"""

from .models import (
    Role,
    LearningState,
    ReviewState,
    User,
    LearnedTechnology,
    TraineeTechnologyState,
    LearningSessionLog,
    TechnologyReview,
    StatusUpdate,
    StatusFeedback,
)

__all__ = [
    "Role",
    "LearningState",
    "ReviewState",
    "User",
    "LearnedTechnology",
    "TraineeTechnologyState",
    "LearningSessionLog",
    "TechnologyReview",
    "StatusUpdate",
    "StatusFeedback",
]
