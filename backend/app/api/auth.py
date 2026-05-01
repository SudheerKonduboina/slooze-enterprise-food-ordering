"""Authentication API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.schemas import LoginRequest, TokenResponse, UserResponse
from app.services.services import AuthService
from app.rbac.guards import get_current_user, CurrentUser

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT token.

    The token contains the user's role and country for authorization.
    """
    auth_service = AuthService(db)
    return auth_service.authenticate(login_data)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser = Depends(get_current_user)):
    """Get the currently authenticated user's profile."""
    user = current_user.user
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        role=user.role.value if hasattr(user.role, 'value') else user.role,
        country=user.country.value if hasattr(user.country, 'value') else user.country,
        is_active=user.is_active,
        avatar_url=user.avatar_url,
        created_at=user.created_at,
    )
