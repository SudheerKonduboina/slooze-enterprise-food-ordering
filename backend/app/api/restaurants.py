"""Restaurant and Menu API endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.rbac.guards import get_current_user, CurrentUser, require_permission
from app.rbac.permissions import Action
from app.services.services import RestaurantService
from app.schemas.schemas import (
    RestaurantResponse, RestaurantListResponse,
    MenuItemResponse, MenuItemListResponse,
)

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("", response_model=RestaurantListResponse)
async def list_restaurants(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUser = Depends(require_permission(Action.VIEW_RESTAURANTS)),
    db: Session = Depends(get_db),
):
    """
    List all restaurants.

    Results are filtered by the user's country (row-level access control).
    Admin users see all restaurants across countries.
    """
    service = RestaurantService(db)
    restaurants, total = service.get_restaurants(current_user, page, page_size)
    return RestaurantListResponse(
        restaurants=restaurants, total=total, page=page, page_size=page_size
    )


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: str,
    current_user: CurrentUser = Depends(require_permission(Action.VIEW_RESTAURANTS)),
    db: Session = Depends(get_db),
):
    """
    Get a specific restaurant by ID.

    Country access control is enforced — users can only view restaurants
    in their assigned country.
    """
    service = RestaurantService(db)
    return service.get_restaurant(restaurant_id, current_user)


@router.get("/{restaurant_id}/menu", response_model=MenuItemListResponse)
async def get_restaurant_menu(
    restaurant_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    category: Optional[str] = Query(None),
    current_user: CurrentUser = Depends(require_permission(Action.VIEW_MENU)),
    db: Session = Depends(get_db),
):
    """
    Get the menu items for a specific restaurant.

    Supports pagination and filtering by category.
    Country access control is enforced.
    """
    service = RestaurantService(db)
    items, total = service.get_menu(
        restaurant_id, current_user, page, page_size, category
    )
    return MenuItemListResponse(
        menu_items=items, total=total, page=page, page_size=page_size
    )
