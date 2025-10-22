"""
Core Domain Models

This module defines all core business entities (domain models) for the
mentorship application.

These models are implemented as Pydantic `BaseModel` classes and are
configured to be immutable via ``IMMUTABLE_CONFIG``.

They represent the pure, canonical "language" of the business and are
intentionally decoupled from any database (e.g., SQLAlchemy)
or API (e.g., DTOs) implementation details.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl

# --- Configuration ---

# This config makes our domain models immutable (read-only).
# Business logic should return *new* instances of models,
# not modify existing ones in place.
IMMUTABLE_CONFIG = ConfigDict(frozen=True)


# --- Enumerations (Business Rules) ---


class Role(str, Enum):
    """
    Defines the roles a User can have within the system.
    """

    TRAINEE = "trainee"
    MENTOR = "mentor"
    ADMIN = "admin"  #: e.g., Head of Mentorship


class LearningState(str, Enum):
    """
    Describes the *current* state of a Trainee's progress
    on a *single* technology.
    """

    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    READY_FOR_REVIEW = "ready_for_review"
    REVIEW_SCHEDULED = "review_scheduled"
    APPROVED = "approved"
    CANCELLED = "cancelled"


class ReviewState(str, Enum):
    """
    Describes the *overall result* of a single review event.
    """

    APPROVED = "approved"
    REJECTED = "rejected"


class QuestionRating(str, Enum):
    """
    NEW ENUM
    Describes the rating for a *single question* during a check.
    """

    CORRECT = "correct"  #: (+)
    PARTIAL = "partial"  #: (+-)
    INCORRECT = "incorrect"  #: (-)


# --- Core Domain Models ---


class User(BaseModel):
    """
    Represents a canonical User in the system.

    :param id: Unique identifier for the user.
    :param email: Primary identifier from Gmail.
    :param full_name: User's full name.
    :param avatar_url: URL to the user's profile picture.
    :param role: The user's role in the system.
    :param is_active: Flag to mark the user as active or inactive.
    :param created_at: Timestamp when the user was created.
    :param mentor_id: If role is TRAINEE, this links to their assigned Mentor (User.id).
    """

    model_config = IMMUTABLE_CONFIG

    id: UUID
    email: EmailStr
    full_name: str
    avatar_url: HttpUrl | None = None
    role: Role
    is_active: bool = True
    created_at: datetime
    mentor_id: UUID | None = None


class LearnedTechnology(BaseModel):
    """
    Represents a canonical "tag" for a skill or technology.

    :param id: Unique identifier for the technology.
    :param name: Normalized name (e.g., "python", "fastapi").
    """

    model_config = IMMUTABLE_CONFIG

    id: UUID
    name: str


class TraineeTechnologyState(BaseModel):
    """
    Represents the *current state* of a Trainee learning a Technology.

    :param id: Unique identifier for this state entry.
    :param trainee_id: The ID of the `User` (Trainee).
    :param technology_id: The ID of the `LearnedTechnology`.
    :param mentor_id: The ID of the responsible `User` (Mentor).
    :param state: The current `LearningState` of this task.
    :param added_at: Timestamp when this task was first added to the trainee's list.
    :param scheduled_review_at: Timestamp for a scheduled review (if state is REVIEW_SCHEDULED).
    """

    model_config = IMMUTABLE_CONFIG

    id: UUID
    trainee_id: UUID
    technology_id: UUID
    mentor_id: UUID
    state: LearningState
    added_at: datetime
    scheduled_review_at: datetime | None = None


class LearningSessionLog(BaseModel):
    """
    Logs a *single continuous period* of work in the 'IN_PROGRESS' state.

    :param id: Unique identifier for the log entry.
    :param trainee_technology_state_id: Links to the "task card" this session belongs to.
    :param start_time: Timestamp when the 'IN_PROGRESS' session began.
    :param end_time: Timestamp when the session ended. None if active.
    """

    model_config = IMMUTABLE_CONFIG

    id: UUID
    trainee_technology_state_id: UUID
    start_time: datetime
    end_time: datetime | None = None


class TechnologyReview(BaseModel):
    """
    MODIFIED MODEL
    A "log entry" representing one review attempt (a "check").

    This is now a "header" for a collection of CheckQuestionResult items.
    The `feedback` field is the *overall summary* of the check.

    `questions_asked` and `questions_correct` are REMOVED, as they
    will be calculated by the ApplicationService from the associated
    `CheckQuestionResult` entries.

    :param id: Unique identifier for the review.
    :param trainee_technology_state_id: Links to the "task card" this review is for.
    :param mentor_id: The ID of the `User` (Mentor) who conducted the review.
    :param review_state: The *overall* outcome of the review (APPROVED or REJECTED).
    :param feedback: The mentor's *overall summary* comments for this review.
    :param created_at: Timestamp when the review was submitted.
    """

    model_config = IMMUTABLE_CONFIG

    id: UUID
    trainee_technology_state_id: UUID
    mentor_id: UUID
    review_state: ReviewState
    feedback: str
    created_at: datetime


class CheckQuestion(BaseModel):
    """
    NEW MODEL
    Represents a single question in the "Question Bank".
    Each question is tied to a specific technology.

    :param id: Unique identifier for the question.
    :param technology_id: Links to the `LearnedTechnology` this question is about.
    :param question_text: The text of the question (e.g., "What is the GIL?").
    :param is_active: Allows mentors to "delete" (archive) questions without breaking history.
    :param created_by_mentor_id: The ID of the `User` (Mentor) who added this question.
    """

    model_config = IMMUTABLE_CONFIG

    id: UUID
    technology_id: UUID
    question_text: str
    is_active: bool = True
    created_at: datetime
    created_by_mentor_id: UUID


class CheckQuestionResult(BaseModel):
    """
    NEW MODEL
    Represents the result of a *single question* during a *single review*.
    This is the log of `+`, `-`, or `+-`.

    :param id: Unique identifier for this result.
    :param technology_review_id: Links to the specific `TechnologyReview` (check) this was part of.
    :param check_question_id: Links to the `CheckQuestion` that was asked.
    :param rating: The rating given by the mentor (`correct`, `partial`, `incorrect`).
    :param mentor_comment: (Optional) A specific note for this answer (e.g., "Confused X with Y").
    """

    model_config = IMMUTABLE_CONFIG

    id: UUID
    technology_review_id: UUID
    check_question_id: UUID
    rating: QuestionRating
    mentor_comment: str | None = None


class StatusUpdate(BaseModel):
    """
    Represents a daily status log submitted by a Trainee.

    :param id: Unique identifier for the status update.
    :param trainee_id: The ID of the `User` (Trainee) who submitted.
    :param created_at: Timestamp of submission.
    :param raw_text: The original, unmodified text from the Trainee.
    :param processed_at: Timestamp when LLM processing was completed.
    :param llm_summary: AI-generated summary of the raw text.
    :param llm_metrics: AI-extracted metrics (e.g., {"mood": "positive"}).
    :param learned_technology_ids: List of `LearnedTechnology` IDs extracted by the LLM.
    """

    model_config = IMMUTABLE_CONFIG

    id: UUID
    trainee_id: UUID
    created_at: datetime
    raw_text: str
    processed_at: datetime | None = None
    llm_summary: str | None = None
    llm_metrics: dict | None = None
    learned_technology_ids: list[UUID] = []


class StatusFeedback(BaseModel):
    """
    Represents a Mentor's comment on a *specific* daily `StatusUpdate`.


    :param id: Unique identifier for the feedback.
    :param status_update_id: Links to the daily `StatusUpdate`.
    :param mentor_id: The ID of the `User` (Mentor) who wrote the comment.
    :param text: The content of the feedback comment.
    :param created_at: Timestamp when the feedback was submitted.
    """

    model_config = IMMUTABLE_CONFIG

    id: UUID
    status_update_id: UUID
    mentor_id: UUID
    text: str
    created_at: datetime
