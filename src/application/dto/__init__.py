"""
Data Transfer Objects (DTOs) Package

This package defines the data structures used for communication
between the Presentation layer (API) and the Application
Service layer (Use Cases).

DTOs define the "shape" of data for inputs (e.g., `...CreateDTO`)
and outputs (e.g., `...DTO`) of our business logic.
"""

from .user_dto import (
    AuthRequestDTO,
    AuthResponseDTO,
    UserDTO,
)
from .technology_dto import (
    TechnologyDTO,
    AdminTechnologyCreateDTO,
)
from .trainee_dto import (
    TraineeStartLearningDTO,
    TraineeMarkReadyDTO,
    TraineeTechnologyStateDTO,
)
from .mentor_dto import (
    MentorScheduleReviewDTO,
    MentorSubmitReviewDTO,
)
from .status_dto import (
    WebhookStatusUpdateDTO,
    MentorStatusFeedbackDTO,
    StatusFeedbackDTO,
    StatusUpdateDTO,
)

__all__ = [
    # User & Auth
    "AuthRequestDTO",
    "AuthResponseDTO",
    "UserDTO",
    # Technology
    "TechnologyDTO",
    "AdminTechnologyCreateDTO",
    # Trainee
    "TraineeStartLearningDTO",
    "TraineeMarkReadyDTO",
    "TraineeTechnologyStateDTO",
    # Mentor
    "MentorScheduleReviewDTO",
    "MentorSubmitReviewDTO",
    # Status & Feedback
    "WebhookStatusUpdateDTO",
    "MentorStatusFeedbackDTO",
    "StatusFeedbackDTO",
    "StatusUpdateDTO",
]
