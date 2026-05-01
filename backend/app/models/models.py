"""SQLAlchemy ORM models for the Slooze Food Ordering Platform."""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, String, Float, Integer, Boolean, DateTime, ForeignKey,
    Enum as SAEnum, Text, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.session import Base


# ─── Enums ───────────────────────────────────────────────────────────────────

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    MEMBER = "MEMBER"


class CountryEnum(str, enum.Enum):
    INDIA = "INDIA"
    AMERICA = "AMERICA"


class OrderStatusEnum(str, enum.Enum):
    CART = "CART"
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class PaymentMethodEnum(str, enum.Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    UPI = "UPI"
    NET_BANKING = "NET_BANKING"
    WALLET = "WALLET"


class PaymentStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


# ─── Helper ──────────────────────────────────────────────────────────────────

def generate_uuid():
    return str(uuid.uuid4())


def utcnow():
    return datetime.now(timezone.utc)


# ─── Models ──────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(RoleEnum), nullable=False, default=RoleEnum.MEMBER)
    country = Column(SAEnum(CountryEnum), nullable=False)
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    payment_methods = relationship("PaymentMethod", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username} ({self.role.value}, {self.country.value})>"


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    cuisine_type = Column(String(100), nullable=False)
    country = Column(SAEnum(CountryEnum), nullable=False, index=True)
    address = Column(Text, nullable=True)
    rating = Column(Float, default=4.0)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    opening_hours = Column(String(100), default="09:00-22:00")
    delivery_time_mins = Column(Integer, default=30)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Restaurant {self.name} ({self.country.value})>"


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    restaurant_id = Column(String(36), ForeignKey("restaurants.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    image_url = Column(String(500), nullable=True)
    is_vegetarian = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    preparation_time_mins = Column(Integer, default=15)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="menu_items")

    def __repr__(self):
        return f"<MenuItem {self.name} (${self.price})>"


class Order(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    restaurant_id = Column(String(36), ForeignKey("restaurants.id"), nullable=False, index=True)
    country = Column(SAEnum(CountryEnum), nullable=False, index=True)
    status = Column(SAEnum(OrderStatusEnum), default=OrderStatusEnum.CART, nullable=False)
    total_amount = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    user = relationship("User", back_populates="orders")
    restaurant = relationship("Restaurant")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order {self.id[:8]} ({self.status.value})>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False, index=True)
    menu_item_id = Column(String(36), ForeignKey("menu_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    special_instructions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem")

    def __repr__(self):
        return f"<OrderItem {self.id[:8]} (qty: {self.quantity})>"


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    method_type = Column(SAEnum(PaymentMethodEnum), nullable=False)
    label = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)  # Masked card number, UPI ID, etc.
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    user = relationship("User", back_populates="payment_methods")

    def __repr__(self):
        return f"<PaymentMethod {self.label} ({self.method_type.value})>"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False, unique=True)
    payment_method_id = Column(String(36), ForeignKey("payment_methods.id"), nullable=True)
    amount = Column(Float, nullable=False)
    status = Column(SAEnum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING, nullable=False)
    transaction_id = Column(String(255), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    order = relationship("Order", back_populates="payment")
    payment_method = relationship("PaymentMethod")

    def __repr__(self):
        return f"<Payment {self.id[:8]} ({self.status.value})>"
