"""
Data Transfer Objects for Mentor-specific actions.
"""

from uuid import UUID
from pydantic import BaseModel, Field
from typing import Annotated

from src.core.domain import ReviewState

from .check_dto import CheckQuestionResultInputDTO


class MentorSubmitReviewDTO(BaseModel):
    """
    Input DTO for a mentor submitting a complete review/check.
    This is the "header" DTO for the entire operation.

    :param trainee_technology_state_id: The ID of the `TraineeTechnologyState` being reviewed.
    :param review_state: The overall outcome of the review (e.g., 'approved', 'rejected').
    :param overall_feedback: The mentor's summary feedback for the whole review.
    :param question_results: A list of individual question results,
                             each containing the question ID, rating, and comment.
    """

    trainee_technology_state_id: UUID
    review_state: ReviewState

    overall_feedback: Annotated[
        str,
        Field(
            ...,
            min_length=10,
            description="Overall feedback for the review (min 10 chars).",
        ),
    ]

    question_results: list[CheckQuestionResultInputDTO]
