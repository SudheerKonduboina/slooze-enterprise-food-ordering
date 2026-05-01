"""Order management API endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.rbac.guards import CurrentUser, require_permission
from app.rbac.permissions import Action
from app.services.services import OrderService
from app.schemas.schemas import (
    OrderCreate, OrderResponse, OrderListResponse,
    CheckoutRequest, UpdatePaymentMethodRequest, MessageResponse,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    current_user: CurrentUser = Depends(require_permission(Action.CREATE_ORDER)),
    db: Session = Depends(get_db),
):
    """
    Create a new order with food items.

    If an active cart exists for the same restaurant, items will be added
    to the existing cart. Country access control is enforced.
    """
    service = OrderService(db)
    return service.create_order(order_data, current_user)


@router.get("", response_model=OrderListResponse)
async def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    current_user: CurrentUser = Depends(require_permission(Action.VIEW_OWN_ORDERS)),
    db: Session = Depends(get_db),
):
    """
    List orders for the current user.

    Admin users see all orders. Results are filtered by country.
    Supports filtering by status and pagination.
    """
    service = OrderService(db)
    orders, total = service.get_orders(current_user, page, page_size, status)
    return OrderListResponse(
        orders=orders, total=total, page=page, page_size=page_size
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: CurrentUser = Depends(require_permission(Action.VIEW_OWN_ORDERS)),
    db: Session = Depends(get_db),
):
    """
    Get a specific order by ID.

    Ownership and country access control are enforced.
    """
    service = OrderService(db)
    return service.get_order(order_id, current_user)


@router.post("/{order_id}/checkout", response_model=OrderResponse)
async def checkout_order(
    order_id: str,
    checkout_data: CheckoutRequest,
    current_user: CurrentUser = Depends(require_permission(Action.CHECKOUT)),
    db: Session = Depends(get_db),
):
    """
    Checkout and pay for an order.

    Only CART orders can be checked out. A valid payment method is required.
    Admin and Manager roles only.
    """
    service = OrderService(db)
    return service.checkout(order_id, checkout_data, current_user)


@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: str,
    current_user: CurrentUser = Depends(require_permission(Action.CANCEL_ORDER)),
    db: Session = Depends(get_db),
):
    """
    Cancel an order.

    Only CART, PLACED, and CONFIRMED orders can be cancelled.
    Payments are refunded automatically. Admin and Manager roles only.
    """
    service = OrderService(db)
    return service.cancel_order(order_id, current_user)


@router.put("/{order_id}/payment-method", response_model=OrderResponse)
async def update_order_payment_method(
    order_id: str,
    data: UpdatePaymentMethodRequest,
    current_user: CurrentUser = Depends(require_permission(Action.UPDATE_ORDER_PAYMENT)),
    db: Session = Depends(get_db),
):
    """
    Update the payment method for an order.

    Allows changing the payment method before or after checkout.
    """
    service = OrderService(db)
    return service.update_order_payment(order_id, data.payment_method_id, current_user)
