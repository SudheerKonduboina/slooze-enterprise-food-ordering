"""Payment method management API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.rbac.guards import CurrentUser, require_permission, get_current_user
from app.rbac.permissions import Action
from app.services.services import PaymentMethodService
from app.schemas.schemas import (
    PaymentMethodCreate, PaymentMethodUpdate,
    PaymentMethodResponse, MessageResponse,
)

router = APIRouter(prefix="/payment-methods", tags=["Payment Methods"])


@router.get("", response_model=list[PaymentMethodResponse])
async def list_payment_methods(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List all payment methods for the current user.
    """
    service = PaymentMethodService(db)
    return service.get_methods(current_user)


@router.post("", response_model=PaymentMethodResponse)
async def create_payment_method(
    data: PaymentMethodCreate,
    current_user: CurrentUser = Depends(require_permission(Action.ADD_PAYMENT_METHOD)),
    db: Session = Depends(get_db),
):
    """
    Add a new payment method.

    Admin role only. Supports CREDIT_CARD, DEBIT_CARD, UPI, NET_BANKING, WALLET.
    """
    service = PaymentMethodService(db)
    return service.create_method(data, current_user)


@router.put("/{method_id}", response_model=PaymentMethodResponse)
async def update_payment_method(
    method_id: str,
    data: PaymentMethodUpdate,
    current_user: CurrentUser = Depends(require_permission(Action.MODIFY_PAYMENT_METHOD)),
    db: Session = Depends(get_db),
):
    """
    Update an existing payment method.

    Admin role only.
    """
    service = PaymentMethodService(db)
    return service.update_method(method_id, data, current_user)


@router.delete("/{method_id}", response_model=MessageResponse)
async def delete_payment_method(
    method_id: str,
    current_user: CurrentUser = Depends(require_permission(Action.MODIFY_PAYMENT_METHOD)),
    db: Session = Depends(get_db),
):
    """
    Delete a payment method.

    Admin role only.
    """
    service = PaymentMethodService(db)
    service.delete_method(method_id, current_user)
    return MessageResponse(message="Payment method deleted successfully")
