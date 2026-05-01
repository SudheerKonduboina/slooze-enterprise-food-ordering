"""
RBAC (Role-Based Access Control) Policy Engine.

Defines permissions per role and provides the @require_permission decorator
and dependency injection guards for enforcing access policies.
"""

from enum import Enum
from functools import wraps
from typing import Callable

from fastapi import Depends, HTTPException, status

from app.models.models import RoleEnum


# ─── Permission Actions ─────────────────────────────────────────────────────

class Action(str, Enum):
    """All granular actions in the system."""
    VIEW_RESTAURANTS = "view_restaurants"
    VIEW_MENU = "view_menu"
    CREATE_ORDER = "create_order"
    CHECKOUT = "checkout"
    CANCEL_ORDER = "cancel_order"
    ADD_PAYMENT_METHOD = "add_payment_method"
    MODIFY_PAYMENT_METHOD = "modify_payment_method"
    VIEW_ALL_ORDERS = "view_all_orders"
    MANAGE_USERS = "manage_users"
    VIEW_DASHBOARD = "view_dashboard"
    VIEW_OWN_ORDERS = "view_own_orders"
    UPDATE_ORDER_PAYMENT = "update_order_payment"


# ─── Role-Permission Matrix ─────────────────────────────────────────────────

ROLE_PERMISSIONS: dict[RoleEnum, set[Action]] = {
    RoleEnum.ADMIN: {
        Action.VIEW_RESTAURANTS,
        Action.VIEW_MENU,
        Action.CREATE_ORDER,
        Action.CHECKOUT,
        Action.CANCEL_ORDER,
        Action.ADD_PAYMENT_METHOD,
        Action.MODIFY_PAYMENT_METHOD,
        Action.VIEW_ALL_ORDERS,
        Action.MANAGE_USERS,
        Action.VIEW_DASHBOARD,
        Action.VIEW_OWN_ORDERS,
        Action.UPDATE_ORDER_PAYMENT,
    },
    RoleEnum.MANAGER: {
        Action.VIEW_RESTAURANTS,
        Action.VIEW_MENU,
        Action.CREATE_ORDER,
        Action.CHECKOUT,
        Action.CANCEL_ORDER,
        Action.VIEW_OWN_ORDERS,
        Action.VIEW_DASHBOARD,
        Action.UPDATE_ORDER_PAYMENT,
    },
    RoleEnum.MEMBER: {
        Action.VIEW_RESTAURANTS,
        Action.VIEW_MENU,
        Action.CREATE_ORDER,
        Action.VIEW_OWN_ORDERS,
    },
}


def has_permission(role: RoleEnum, action: Action) -> bool:
    """Check if a role has a specific permission."""
    permissions = ROLE_PERMISSIONS.get(role, set())
    return action in permissions


def get_permissions_for_role(role: RoleEnum) -> list[str]:
    """Get all permission strings for a role."""
    permissions = ROLE_PERMISSIONS.get(role, set())
    return [p.value for p in permissions]
