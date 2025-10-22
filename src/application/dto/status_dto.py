"""
Data Transfer Objects for daily Status Updates
(from Google Chat) and Status Feedback (comments).
"""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class WebhookStatusUpdateDTO(BaseModel):
    """
    Input DTO: The raw data we expect to receive from
    the Google Chat Webhook.

    The structure will depend on the Google Chat API,
    this is a placeholder.
    """

    user_email: str  # Email of the user who sent the message
    message_text: str
    message_id: str  # Unique ID from Google Chat


class MentorStatusFeedbackDTO(BaseModel):
    """
    Input DTO: A mentor writes a comment on a daily status.
    """

    status_update_id: UUID
    feedback_text: str = Field(..., min_length=1)


class StatusFeedbackDTO(BaseModel):
    """
    Output DTO: Represents a single feedback comment.
    """

    id: UUID
    mentor_id: UUID
    mentor_name: str  # Denormalized for the UI
    text: str
    created_at: datetime

    class Config:
        # Pydantic v1 style for ORM mode.
        # Use `from_attributes = True` in Pydantic v2.
        # This helps create DTOs directly from domain/db models.
        orm_mode = True


class StatusUpdateDTO(BaseModel):
    """
    Output DTO: A full daily status update for the UI.
    """

    id: UUID
    trainee_id: UUID
    trainee_name: str  # Denormalized
    created_at: datetime
    raw_text: str

    # LLM-generated fields
    llm_summary: str | None = None

    # Comments from mentors
    feedback: list[StatusFeedbackDTO] = []

    class Config:
        orm_mode = True
