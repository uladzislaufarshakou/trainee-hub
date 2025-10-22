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
    on a *single* technology. This is the core of the
    learning tracking system.
    """

    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    READY_FOR_REVIEW = "ready_for_review"
    REVIEW_SCHEDULED = "review_scheduled"
    APPROVED = "approved"
    CANCELLED = "cancelled"


class ReviewState(str, Enum):
    """
    Describes the *result* of a single review event.
    Used by the `TechnologyReview` log.
    """

    APPROVED = "approved"
    REJECTED = "rejected"


# --- Core Domain Models ---


class User(BaseModel):
    """
    Represents a canonical User in the system.
    A User's capabilities are defined by their `role`.
    Both Trainees and Mentors are Users.

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
    This is the global "library" of all technologies
    a trainee can choose to learn.

    :param id: Unique identifier for the technology.
    :param name: Normalized name (e.g., "python", "fastapi").
    """

    model_config = IMMUTABLE_CONFIG

    id: UUID
    name: str


class TraineeTechnologyState(BaseModel):
    """
    Represents the *current state* of a Trainee learning a Technology.
    This is the "task card" for a specific learning goal.
    It no longer contains history, only the *current* status.

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

    A new record is created when state changes to 'IN_PROGRESS'.
    The active log is updated with an `end_time` when the state
    changes away from 'IN_PROGRESS'.

    Total learning time = SUM(end_time - start_time) for all
    logs linked to a TraineeTechnologyState.

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
    A "log entry" representing one review attempt (a "check").

    This creates a full history of all review cycles,
    including all rejections ("failed checks") and feedback.

    :param id: Unique identifier for the review.
    :param trainee_technology_state_id: Links to the "task card" this review is for.
    :param mentor_id: The ID of the `User` (Mentor) who conducted the review.
    :param review_state: The outcome of the review (APPROVED or REJECTED).
    :param feedback: The mentor's textual comments for this review.
    :param created_at: Timestamp when the review was submitted.
    :param questions_asked: Optional: number of questions asked during the review.
    :param questions_correct: Optional: number of questions answered correctly.
    """

    model_config = IMMUTABLE_CONFIG

    id: UUID
    trainee_technology_state_id: UUID
    mentor_id: UUID
    review_state: ReviewState
    feedback: str
    created_at: datetime
    questions_asked: int | None = None
    questions_correct: int | None = None


class StatusUpdate(BaseModel):
    """
    Represents a daily status log submitted by a Trainee.
    This is the "raw input" from Google Chat.

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

    .. note::
       This is different from `TechnologyReview.feedback`,
       which is feedback on a final technology check.

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
