"""
Data Transfer Objects for Trainee-specific actions.

These define the inputs for actions a trainee can perform
and the outputs they will receive.
"""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from src.core.domain import LearningState
from .technology_dto import TechnologyDTO
from .user_dto import UserDTO


class TraineeStartLearningDTO(BaseModel):
    """
    Input DTO: Trainee wants to start learning a new technology.
    """

    technology_id: UUID


class TraineeMarkReadyDTO(BaseModel):
    """
    Input DTO: Trainee marks a technology as ready for review.
    """

    trainee_technology_state_id: UUID


class TraineeTechnologyStateDTO(BaseModel):
    """
    Output DTO: A full "Task Card" for the Trainee's UI.

    This is a "denormalized" model, combining data from
    multiple domain models for easy consumption by a frontend.
    """

    id: UUID
    trainee: UserDTO
    technology: TechnologyDTO
    mentor: UserDTO
    state: LearningState
    added_at: datetime
    scheduled_review_at: datetime | None = None

    # This data will be calculated by the Application Service
    total_learning_time_hours: float
    review_history_ids: list[UUID]
