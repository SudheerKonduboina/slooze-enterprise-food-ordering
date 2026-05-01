"""
Repository layer: Database access abstraction.

Implements the Repository Pattern for clean separation of
data access logic from business logic.
"""

from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.models.models import (
    User, Restaurant, MenuItem, Order, OrderItem,
    PaymentMethod, Payment, CountryEnum, OrderStatusEnum,
    RoleEnum
)


# ─── User Repository ────────────────────────────────────────────────────────

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_all(self, page: int = 1, page_size: int = 20) -> tuple[list[User], int]:
        total = self.db.query(func.count(User.id)).scalar()
        users = (
            self.db.query(User)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return users, total

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


# ─── Restaurant Repository ──────────────────────────────────────────────────

class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        return (
            self.db.query(Restaurant)
            .options(joinedload(Restaurant.menu_items))
            .filter(Restaurant.id == restaurant_id, Restaurant.is_active == True)
            .first()
        )

    def get_all_by_country(
        self, country: CountryEnum, page: int = 1, page_size: int = 20
    ) -> tuple[list[Restaurant], int]:
        query = self.db.query(Restaurant).filter(
            Restaurant.country == country,
            Restaurant.is_active == True,
        )
        total = query.count()
        restaurants = (
            query.offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return restaurants, total

    def get_all(self, page: int = 1, page_size: int = 20) -> tuple[list[Restaurant], int]:
        query = self.db.query(Restaurant).filter(Restaurant.is_active == True)
        total = query.count()
        restaurants = query.offset((page - 1) * page_size).limit(page_size).all()
        return restaurants, total


# ─── MenuItem Repository ────────────────────────────────────────────────────

class MenuItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, item_id: str) -> Optional[MenuItem]:
        return self.db.query(MenuItem).filter(MenuItem.id == item_id).first()

    def get_by_restaurant(
        self, restaurant_id: str, page: int = 1, page_size: int = 50,
        category: Optional[str] = None
    ) -> tuple[list[MenuItem], int]:
        query = self.db.query(MenuItem).filter(
            MenuItem.restaurant_id == restaurant_id,
            MenuItem.is_available == True,
        )
        if category:
            query = query.filter(MenuItem.category == category)
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total


# ─── Order Repository ────────────────────────────────────────────────────────

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.order_items).joinedload(OrderItem.menu_item),
                joinedload(Order.payment),
                joinedload(Order.restaurant),
            )
            .filter(Order.id == order_id)
            .first()
        )

    def get_user_orders(
        self, user_id: str, country: CountryEnum,
        page: int = 1, page_size: int = 20,
        status: Optional[OrderStatusEnum] = None
    ) -> tuple[list[Order], int]:
        query = (
            self.db.query(Order)
            .options(
                joinedload(Order.order_items).joinedload(OrderItem.menu_item),
                joinedload(Order.payment),
                joinedload(Order.restaurant),
            )
            .filter(Order.user_id == user_id, Order.country == country)
        )
        if status:
            query = query.filter(Order.status == status)
        total = query.count()
        orders = (
            query.order_by(Order.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return orders, total

    def get_all_by_country(
        self, country: CountryEnum, page: int = 1, page_size: int = 20
    ) -> tuple[list[Order], int]:
        query = (
            self.db.query(Order)
            .options(
                joinedload(Order.order_items).joinedload(OrderItem.menu_item),
                joinedload(Order.payment),
                joinedload(Order.restaurant),
                joinedload(Order.user),
            )
            .filter(Order.country == country)
        )
        total = query.count()
        orders = (
            query.order_by(Order.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return orders, total

    def get_all(self, page: int = 1, page_size: int = 20) -> tuple[list[Order], int]:
        query = (
            self.db.query(Order)
            .options(
                joinedload(Order.order_items).joinedload(OrderItem.menu_item),
                joinedload(Order.payment),
                joinedload(Order.restaurant),
                joinedload(Order.user),
            )
        )
        total = query.count()
        orders = (
            query.order_by(Order.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return orders, total

    def get_user_cart(self, user_id: str, restaurant_id: str) -> Optional[Order]:
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.order_items).joinedload(OrderItem.menu_item),
                joinedload(Order.restaurant),
            )
            .filter(
                Order.user_id == user_id,
                Order.restaurant_id == restaurant_id,
                Order.status == OrderStatusEnum.CART,
            )
            .first()
        )

    def create(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update(self, order: Order) -> Order:
        self.db.commit()
        self.db.refresh(order)
        return order

    def count_by_status(self, country: Optional[CountryEnum] = None) -> dict[str, int]:
        query = self.db.query(Order.status, func.count(Order.id))
        if country:
            query = query.filter(Order.country == country)
        result = query.group_by(Order.status).all()
        return {status.value: count for status, count in result}

    def get_total_revenue(self, country: Optional[CountryEnum] = None) -> float:
        query = self.db.query(func.sum(Order.total_amount)).filter(
            Order.status.in_([
                OrderStatusEnum.CONFIRMED,
                OrderStatusEnum.PREPARING,
                OrderStatusEnum.DELIVERED,
            ])
        )
        if country:
            query = query.filter(Order.country == country)
        result = query.scalar()
        return result or 0.0


# ─── OrderItem Repository ───────────────────────────────────────────────────

class OrderItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_item(self, order_item: OrderItem) -> OrderItem:
        self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order_item)
        return order_item

    def remove_item(self, item_id: str) -> None:
        item = self.db.query(OrderItem).filter(OrderItem.id == item_id).first()
        if item:
            self.db.delete(item)
            self.db.commit()


# ─── PaymentMethod Repository ───────────────────────────────────────────────

class PaymentMethodRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, method_id: str) -> Optional[PaymentMethod]:
        return self.db.query(PaymentMethod).filter(PaymentMethod.id == method_id).first()

    def get_user_methods(self, user_id: str) -> list[PaymentMethod]:
        return (
            self.db.query(PaymentMethod)
            .filter(PaymentMethod.user_id == user_id)
            .order_by(PaymentMethod.is_default.desc())
            .all()
        )

    def create(self, method: PaymentMethod) -> PaymentMethod:
        self.db.add(method)
        self.db.commit()
        self.db.refresh(method)
        return method

    def update(self, method: PaymentMethod) -> PaymentMethod:
        self.db.commit()
        self.db.refresh(method)
        return method

    def delete(self, method: PaymentMethod) -> None:
        self.db.delete(method)
        self.db.commit()


# ─── Payment Repository ─────────────────────────────────────────────────────

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_order_id(self, order_id: str) -> Optional[Payment]:
        return self.db.query(Payment).filter(Payment.order_id == order_id).first()

    def create(self, payment: Payment) -> Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def update(self, payment: Payment) -> Payment:
        self.db.commit()
        self.db.refresh(payment)
        return payment
