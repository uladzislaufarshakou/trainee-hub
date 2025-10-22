"""
Repository Interfaces Package

This package defines the public API for all repository interfaces
(ports) in the application layer.

These abstract classes define the persistence contract that the
infrastructure layer must implement.

The application service layer depends *only* on these interfaces,
not on concrete database implementations.
"""

from .i_user_repository import IUserRepository
from .i_learned_technology_repository import ILearnedTechnologyRepository
from .i_trainee_technology_state_repository import ITraineeTechnologyStateRepository
from .i_learning_session_log_repository import ILearningSessionLogRepository
from .i_technology_review_repository import ITechnologyReviewRepository
from .i_status_update_repository import IStatusUpdateRepository
from .i_status_feedback_repository import IStatusFeedbackRepository

__all__ = [
    "IUserRepository",
    "ILearnedTechnologyRepository",
    "ITraineeTechnologyStateRepository",
    "ILearningSessionLogRepository",
    "ITechnologyReviewRepository",
    "IStatusUpdateRepository",
    "IStatusFeedbackRepository",
]
