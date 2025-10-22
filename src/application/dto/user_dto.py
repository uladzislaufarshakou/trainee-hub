"""
Data Transfer Objects for User and Authentication operations.

These models define the shape of data for:
1.  Exchanging an OAuth code for a JWT (Auth).
2.  Representing a User safely to the outside world (e.g., in an API response).
"""

from uuid import UUID
from pydantic import BaseModel, EmailStr, HttpUrl
from src.core.domain import Role


class AuthRequestDTO(BaseModel):
    """
    Input DTO: The data received from the frontend after Google login.
    """

    auth_code: str


class AuthResponseDTO(BaseModel):
    """
    Output DTO: The JWT token (and user info) we send back to the client.
    """

    access_token: str
    token_type: str = "bearer"
    user_id: UUID
    role: Role


class UserDTO(BaseModel):
    """
    Output DTO: A safe representation of a User model.

    This is what the API will return when asked for user info.
    It omits sensitive data and is shaped for a client's needs.
    """

    id: UUID
    email: EmailStr
    full_name: str
    avatar_url: HttpUrl | None
    role: Role
    mentor_id: UUID | None = None
