"""
Authorization guards using FastAPI dependency injection.

Provides:
- get_current_user: Extracts and validates the JWT token
- require_permission: Decorator/dependency for action-level authorization
- CountryGuard: Ensures resources belong to the user's country
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.core.exceptions import AuthenticationError, AuthorizationError, CountryAccessError
from app.database.session import get_db
from app.models.models import User, RoleEnum, CountryEnum
from app.rbac.permissions import Action, has_permission, get_permissions_for_role

security_scheme = HTTPBearer()


class CurrentUser:
    """Encapsulates authenticated user context."""

    def __init__(self, user: User, role: RoleEnum, country: CountryEnum):
        self.user = user
        self.id = user.id
        self.role = role
        self.country = country
        self.email = user.email
        self.full_name = user.full_name
        self.permissions = get_permissions_for_role(role)

    def has_permission(self, action: Action) -> bool:
        return has_permission(self.role, action)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> CurrentUser:
    """Extract and validate the current user from the JWT token."""
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return CurrentUser(
        user=user,
        role=RoleEnum(user.role),
        country=CountryEnum(user.country),
    )


def require_permission(action: Action):
    """
    Dependency factory that enforces action-level authorization.

    Usage:
        @router.post("/orders", dependencies=[Depends(require_permission(Action.CREATE_ORDER))])
        async def create_order(...):
            ...
    """

    async def permission_checker(
        current_user: CurrentUser = Depends(get_current_user),
    ) -> CurrentUser:
        if not current_user.has_permission(action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {action.value} is not allowed for {current_user.role.value} role",
            )
        return current_user

    return permission_checker


def require_role(*roles: RoleEnum):
    """Dependency factory that enforces role-level authorization."""

    async def role_checker(
        current_user: CurrentUser = Depends(get_current_user),
    ) -> CurrentUser:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This endpoint requires one of: {[r.value for r in roles]}",
            )
        return current_user

    return role_checker


class CountryGuard:
    """
    Validates that a resource belongs to the user's country.

    Usage:
        country_guard = CountryGuard()
        country_guard.validate(user_country=current_user.country, resource_country=restaurant.country)
    """

    @staticmethod
    def validate(user_country: CountryEnum, resource_country: CountryEnum) -> None:
        """Raise if the user's country doesn't match the resource's country."""
        if user_country != resource_country:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: You can only access resources in {user_country.value}",
            )

    @staticmethod
    def filter_query(query, model_country_field, user_country: CountryEnum):
        """Add a country filter to a SQLAlchemy query for row-level access control."""
        return query.filter(model_country_field == user_country)
