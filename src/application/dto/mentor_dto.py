"""
Data Transfer Objects for Mentor-specific actions.
"""

from typing import Annotated
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, model_validator

from src.core.domain import ReviewState


class MentorScheduleReviewDTO(BaseModel):
    """
    Input DTO: Mentor schedules a review for a trainee's task.
    """

    trainee_technology_state_id: UUID
    scheduled_at: datetime  # The future date/time for the review


class MentorSubmitReviewDTO(BaseModel):
    """
    Input DTO: Mentor submits the result of a review.
    """

    trainee_technology_state_id: UUID
    review_state: ReviewState
    feedback: Annotated[str, Field(min_length=10)]
    questions_asked: Annotated[int, Field(ge=0)] | None = None
    questions_correct: Annotated[int, Field(ge=0)] | None = None

    @model_validator(mode="after")
    def validate_questions(self) -> "MentorSubmitReviewDTO":
        """
        Validates that questions_correct is not greater than questions_asked.
        """
        if self.questions_asked is not None and self.questions_correct is not None:
            if self.questions_correct > self.questions_asked:
                raise ValueError(
                    "Correct questions cannot be greater than total questions asked."
                )
        return self
