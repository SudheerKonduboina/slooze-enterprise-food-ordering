"""Dashboard and admin API endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.rbac.guards import CurrentUser, require_permission, require_role
from app.rbac.permissions import Action
from app.models.models import RoleEnum
from app.services.services import DashboardService
from app.schemas.schemas import DashboardStats, UserListResponse, UserResponse
from app.repositories.repositories import UserRepository
from app.rbac.permissions import get_permissions_for_role

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(
    current_user: CurrentUser = Depends(require_permission(Action.VIEW_DASHBOARD)),
    db: Session = Depends(get_db),
):
    """
    Get dashboard statistics.

    Available to Admin and Manager roles.
    Managers see their country-scoped data. Admins see all.
    """
    service = DashboardService(db)
    return service.get_stats(current_user)


@router.get("/users", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUser = Depends(require_permission(Action.MANAGE_USERS)),
    db: Session = Depends(get_db),
):
    """
    List all users (Admin only).
    """
    user_repo = UserRepository(db)
    users, total = user_repo.get_all(page, page_size)
    user_responses = [
        UserResponse(
            id=u.id,
            email=u.email,
            username=u.username,
            full_name=u.full_name,
            role=u.role.value if hasattr(u.role, 'value') else u.role,
            country=u.country.value if hasattr(u.country, 'value') else u.country,
            is_active=u.is_active,
            avatar_url=u.avatar_url,
            created_at=u.created_at,
        )
        for u in users
    ]
    return UserListResponse(
        users=user_responses, total=total, page=page, page_size=page_size
    )


@router.get("/permissions")
async def get_role_permissions(
    current_user: CurrentUser = Depends(require_permission(Action.VIEW_DASHBOARD)),
):
    """
    Get permission matrix for all roles.
    """
    return {
        "roles": {
            role.value: get_permissions_for_role(role)
            for role in RoleEnum
        },
        "current_user": {
            "role": current_user.role.value,
            "permissions": current_user.permissions,
        },
    }
