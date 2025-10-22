"""
Data Transfer Objects for the Check System.

Defines the data structures for managing the "Question Bank"
(Create, Update, View) and for submitting the results
of a "Check" (the individual question ratings).
"""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated

from src.core.domain import QuestionRating, LearnedTechnology, User


class CreateCheckQuestionDTO(BaseModel):
    """
    Input DTO for a mentor creating a new question in the question bank.

    :param technology_id: The ID of the technology this question is for.
    :param question_text: The text of the question (min 10 chars).
    """

    technology_id: UUID
    question_text: Annotated[
        str,
        Field(
            ...,
            min_length=10,
            description="The text of the question (min 10 chars).",
        ),
    ]


class UpdateCheckQuestionDTO(BaseModel):
    """
    Input DTO for a mentor updating an existing question.

    :param question_text: The new text of the question (min 10 chars).
    :param is_active: The new active status (e.g., for archiving).
    """

    question_text: Annotated[
        str,
        Field(
            ...,
            min_length=10,
            description="The text of the question (min 10 chars).",
        ),
    ]
    is_active: bool


class CheckQuestionDTO(BaseModel):
    """
    Output DTO representing a single question from the question bank.

    This is a denormalized model for UI consumption,
    which will be assembled by an Application Service.

    :param id: The unique ID of the question.
    :param technology: The denormalized `LearnedTechnology` model.
    :param question_text: The text of the question.
    :param is_active: The active status of the question.
    :param created_at: The timestamp when the question was created.
    :param created_by_mentor: The denormalized `User` model of the mentor.
    """

    id: UUID
    technology: LearnedTechnology
    question_text: str
    is_active: bool
    created_at: datetime
    created_by_mentor: User

    class Config:
        orm_mode = True


class CheckQuestionResultInputDTO(BaseModel):
    """
    Input DTO representing the result for a *single* question
    submitted by a mentor.

    Used as part of the `MentorSubmitReviewDTO`.

    :param check_question_id: The ID of the question being answered.
    :param rating: The rating given by the mentor ('correct', 'partial', 'incorrect').
    :param mentor_comment: An optional specific comment for this question's answer.
    """

    check_question_id: UUID
    rating: QuestionRating
    mentor_comment: str | None = None
