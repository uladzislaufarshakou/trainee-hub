"""
Data Transfer Objects for LearnedTechnology operations.
"""

from uuid import UUID
from pydantic import BaseModel, Field


class TechnologyDTO(BaseModel):
    """
    Output DTO: Represents a LearnedTechnology.
    """

    id: UUID
    name: str

    class Config:
        # Pydantic v1 style for ORM mode.
        # Use `from_attributes = True` in Pydantic v2.
        # This helps create DTOs directly from domain/db models.
        orm_mode = True


class AdminTechnologyCreateDTO(BaseModel):
    """
    Input DTO: Data required for an Admin to create a new technology.
    """

    name: str = Field(..., min_length=1, max_length=100)
