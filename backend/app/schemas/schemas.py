"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ─── Auth Schemas ────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=4, description="User password")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class TokenPayload(BaseModel):
    sub: str  # user_id
    role: str
    country: str
    exp: int


# ─── User Schemas ────────────────────────────────────────────────────────────

class UserBase(BaseModel):
    email: str
    username: str
    full_name: str
    role: str
    country: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=4)


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    role: str
    country: str
    is_active: bool
    avatar_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
    page: int
    page_size: int


# ─── Restaurant Schemas ──────────────────────────────────────────────────────

class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    cuisine_type: str
    country: str
    address: Optional[str] = None
    rating: float = 4.0
    image_url: Optional[str] = None
    opening_hours: str = "09:00-22:00"
    delivery_time_mins: int = 30


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantResponse(RestaurantBase):
    id: str
    is_active: bool
    created_at: datetime
    menu_item_count: Optional[int] = 0

    class Config:
        from_attributes = True


class RestaurantListResponse(BaseModel):
    restaurants: list[RestaurantResponse]
    total: int
    page: int
    page_size: int


# ─── MenuItem Schemas ────────────────────────────────────────────────────────

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: str
    image_url: Optional[str] = None
    is_vegetarian: bool = False
    is_available: bool = True
    preparation_time_mins: int = 15


class MenuItemCreate(MenuItemBase):
    restaurant_id: str


class MenuItemResponse(MenuItemBase):
    id: str
    restaurant_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class MenuItemListResponse(BaseModel):
    menu_items: list[MenuItemResponse]
    total: int
    page: int
    page_size: int


# ─── Order Schemas ───────────────────────────────────────────────────────────

class OrderItemCreate(BaseModel):
    menu_item_id: str
    quantity: int = Field(..., ge=1)
    special_instructions: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: str
    menu_item_id: str
    menu_item_name: Optional[str] = None
    quantity: int
    unit_price: float
    subtotal: float
    special_instructions: Optional[str] = None

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    restaurant_id: str
    items: list[OrderItemCreate] = Field(..., min_length=1)
    notes: Optional[str] = None


class AddItemToOrder(BaseModel):
    menu_item_id: str
    quantity: int = Field(..., ge=1)
    special_instructions: Optional[str] = None


class OrderResponse(BaseModel):
    id: str
    user_id: str
    restaurant_id: str
    restaurant_name: Optional[str] = None
    country: str
    status: str
    total_amount: float
    notes: Optional[str] = None
    items: list[OrderItemResponse] = []
    payment: Optional["PaymentResponse"] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    orders: list[OrderResponse]
    total: int
    page: int
    page_size: int


# ─── Payment Schemas ─────────────────────────────────────────────────────────

class PaymentMethodCreate(BaseModel):
    method_type: str
    label: str
    details: Optional[str] = None
    is_default: bool = False


class PaymentMethodUpdate(BaseModel):
    method_type: Optional[str] = None
    label: Optional[str] = None
    details: Optional[str] = None
    is_default: Optional[bool] = None


class PaymentMethodResponse(BaseModel):
    id: str
    user_id: str
    method_type: str
    label: str
    details: Optional[str] = None
    is_default: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CheckoutRequest(BaseModel):
    payment_method_id: str


class PaymentResponse(BaseModel):
    id: str
    order_id: str
    payment_method_id: Optional[str] = None
    amount: float
    status: str
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UpdatePaymentMethodRequest(BaseModel):
    payment_method_id: str


# ─── Dashboard / Stats Schemas ───────────────────────────────────────────────

class DashboardStats(BaseModel):
    total_orders: int
    total_revenue: float
    total_restaurants: int
    total_users: int
    recent_orders: list[OrderResponse]
    orders_by_status: dict[str, int]


# ─── Generic Response ────────────────────────────────────────────────────────

class MessageResponse(BaseModel):
    message: str
    success: bool = True


# Rebuild models for forward references
TokenResponse.model_rebuild()
OrderResponse.model_rebuild()
