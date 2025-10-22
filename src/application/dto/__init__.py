"""
Data Transfer Objects Package

This package defines the public API for all DTOs
used by the Application Service layer.

It imports all DTO classes from their respective modules
and exposes them here, controlling the public API
via the ``__all__`` list.
"""

# Imports from user_dto.py
from .user_dto import (
    AuthRequestDTO,
    AuthResponseDTO,
    UserDTO,
)

# Imports from technology_dto.py
from .technology_dto import (
    TechnologyDTO,
)

# Imports from trainee_dto.py
from .trainee_dto import (
    TraineeStartLearningDTO,
    TraineeMarkReadyDTO,
    TraineeTechnologyStateDTO,
)

# Imports from status_dto.py
from .status_dto import (
    WebhookStatusUpdateDTO,
    MentorStatusFeedbackDTO,
    StatusFeedbackDTO,
    StatusUpdateDTO,
)

# Imports from check_dto.py (the new file)
from .check_dto import (
    CreateCheckQuestionDTO,
    UpdateCheckQuestionDTO,
    CheckQuestionDTO,
    CheckQuestionResultInputDTO,
)

# Imports from mentor_dto.py
from .mentor_dto import (
    MentorSubmitReviewDTO,
)


# --- Public API Definition ---

__all__ = [
    # Auth & User
    "AuthRequestDTO",
    "AuthResponseDTO",
    "UserDTO",
    # Technology
    "TechnologyDTO",
    # Trainee Actions
    "TraineeStartLearningDTO",
    "TraineeMarkReadyDTO",
    "TraineeTechnologyStateDTO",
    # Mentor Actions
    "MentorSubmitReviewDTO",
    # Check System
    "CreateCheckQuestionDTO",
    "UpdateCheckQuestionDTO",
    "CheckQuestionDTO",
    "CheckQuestionResultInputDTO",
    # Status & Feedback
    "WebhookStatusUpdateDTO",
    "MentorStatusFeedbackDTO",
    "StatusFeedbackDTO",
    "StatusUpdateDTO",
]
