"""
Service layer: Business logic orchestration.

Services coordinate between repositories, enforce business rules,
and handle cross-cutting concerns like country-based access control.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.models import (
    User, Restaurant, MenuItem, Order, OrderItem,
    PaymentMethod, Payment, CountryEnum, OrderStatusEnum,
    PaymentStatusEnum, PaymentMethodEnum, RoleEnum
)
from app.repositories.repositories import (
    UserRepository, RestaurantRepository, MenuItemRepository,
    OrderRepository, OrderItemRepository, PaymentMethodRepository,
    PaymentRepository
)
from app.rbac.guards import CurrentUser, CountryGuard
from app.core.security import hash_password, verify_password, create_access_token
from app.core.logging import get_logger
from app.schemas.schemas import (
    OrderCreate, OrderItemCreate, CheckoutRequest,
    PaymentMethodCreate, PaymentMethodUpdate, LoginRequest,
    TokenResponse, UserResponse, OrderResponse, OrderItemResponse,
    RestaurantResponse, MenuItemResponse, PaymentMethodResponse,
    PaymentResponse, DashboardStats
)

logger = get_logger(__name__)


# ─── Auth Service ────────────────────────────────────────────────────────────

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def authenticate(self, login: LoginRequest) -> TokenResponse:
        """Authenticate user and return JWT token."""
        user = self.user_repo.get_by_email(login.email)
        if not user or not verify_password(login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated",
            )

        token_data = {
            "sub": user.id,
            "role": user.role.value if isinstance(user.role, RoleEnum) else user.role,
            "country": user.country.value if isinstance(user.country, CountryEnum) else user.country,
            "email": user.email,
        }
        access_token = create_access_token(data=token_data)

        logger.info("user_authenticated", user_id=user.id, role=user.role)

        return TokenResponse(
            access_token=access_token,
            user=UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                role=user.role.value if isinstance(user.role, RoleEnum) else user.role,
                country=user.country.value if isinstance(user.country, CountryEnum) else user.country,
                is_active=user.is_active,
                avatar_url=user.avatar_url,
                created_at=user.created_at,
            ),
        )


# ─── Restaurant Service ─────────────────────────────────────────────────────

class RestaurantService:
    def __init__(self, db: Session):
        self.restaurant_repo = RestaurantRepository(db)
        self.menu_repo = MenuItemRepository(db)

    def get_restaurants(
        self, current_user: CurrentUser, page: int = 1, page_size: int = 20
    ) -> tuple[list[RestaurantResponse], int]:
        """Get restaurants filtered by user's country (admin sees all)."""
        if current_user.role == RoleEnum.ADMIN:
            restaurants, total = self.restaurant_repo.get_all(page, page_size)
        else:
            restaurants, total = self.restaurant_repo.get_all_by_country(
                current_user.country, page, page_size
            )

        result = []
        for r in restaurants:
            result.append(RestaurantResponse(
                id=r.id,
                name=r.name,
                description=r.description,
                cuisine_type=r.cuisine_type,
                country=r.country.value if isinstance(r.country, CountryEnum) else r.country,
                address=r.address,
                rating=r.rating,
                image_url=r.image_url,
                opening_hours=r.opening_hours,
                delivery_time_mins=r.delivery_time_mins,
                is_active=r.is_active,
                created_at=r.created_at,
                menu_item_count=len(r.menu_items) if r.menu_items else 0,
            ))
        return result, total

    def get_restaurant(
        self, restaurant_id: str, current_user: CurrentUser
    ) -> RestaurantResponse:
        """Get a single restaurant with country validation."""
        restaurant = self.restaurant_repo.get_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        # Country guard (admin bypasses)
        if current_user.role != RoleEnum.ADMIN:
            CountryGuard.validate(current_user.country, restaurant.country)

        return RestaurantResponse(
            id=restaurant.id,
            name=restaurant.name,
            description=restaurant.description,
            cuisine_type=restaurant.cuisine_type,
            country=restaurant.country.value if isinstance(restaurant.country, CountryEnum) else restaurant.country,
            address=restaurant.address,
            rating=restaurant.rating,
            image_url=restaurant.image_url,
            opening_hours=restaurant.opening_hours,
            delivery_time_mins=restaurant.delivery_time_mins,
            is_active=restaurant.is_active,
            created_at=restaurant.created_at,
            menu_item_count=len(restaurant.menu_items) if restaurant.menu_items else 0,
        )

    def get_menu(
        self, restaurant_id: str, current_user: CurrentUser,
        page: int = 1, page_size: int = 50, category: Optional[str] = None
    ) -> tuple[list[MenuItemResponse], int]:
        """Get menu items for a restaurant with country validation."""
        restaurant = self.restaurant_repo.get_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        if current_user.role != RoleEnum.ADMIN:
            CountryGuard.validate(current_user.country, restaurant.country)

        items, total = self.menu_repo.get_by_restaurant(restaurant_id, page, page_size, category)
        result = [
            MenuItemResponse(
                id=item.id,
                restaurant_id=item.restaurant_id,
                name=item.name,
                description=item.description,
                price=item.price,
                category=item.category,
                image_url=item.image_url,
                is_vegetarian=item.is_vegetarian,
                is_available=item.is_available,
                preparation_time_mins=item.preparation_time_mins,
                created_at=item.created_at,
            )
            for item in items
        ]
        return result, total


# ─── Order Service ───────────────────────────────────────────────────────────

class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.order_item_repo = OrderItemRepository(db)
        self.restaurant_repo = RestaurantRepository(db)
        self.menu_repo = MenuItemRepository(db)
        self.payment_repo = PaymentRepository(db)
        self.payment_method_repo = PaymentMethodRepository(db)

    def create_order(
        self, order_data: OrderCreate, current_user: CurrentUser
    ) -> OrderResponse:
        """Create a new order with items. Enforces country access."""
        restaurant = self.restaurant_repo.get_by_id(order_data.restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        if current_user.role != RoleEnum.ADMIN:
            CountryGuard.validate(current_user.country, restaurant.country)

        # Check for existing cart for this restaurant
        existing_cart = self.order_repo.get_user_cart(current_user.id, restaurant.id)
        if existing_cart:
            # Add items to existing cart
            return self._add_items_to_order(existing_cart, order_data.items, current_user)

        # Create new order
        order = Order(
            user_id=current_user.id,
            restaurant_id=restaurant.id,
            country=restaurant.country,
            status=OrderStatusEnum.CART,
            notes=order_data.notes,
        )
        self.db.add(order)
        self.db.flush()

        total = 0.0
        for item_data in order_data.items:
            menu_item = self.menu_repo.get_by_id(item_data.menu_item_id)
            if not menu_item:
                raise HTTPException(status_code=404, detail=f"Menu item {item_data.menu_item_id} not found")
            if menu_item.restaurant_id != restaurant.id:
                raise HTTPException(status_code=400, detail="Menu item does not belong to this restaurant")

            subtotal = menu_item.price * item_data.quantity
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=item_data.quantity,
                unit_price=menu_item.price,
                subtotal=subtotal,
                special_instructions=item_data.special_instructions,
            )
            self.db.add(order_item)
            total += subtotal

        order.total_amount = round(total, 2)
        self.db.commit()
        self.db.refresh(order)

        logger.info("order_created", order_id=order.id, user_id=current_user.id)
        return self._to_order_response(order)

    def _add_items_to_order(
        self, order: Order, items: list[OrderItemCreate], current_user: CurrentUser
    ) -> OrderResponse:
        """Add items to an existing cart order."""
        total = order.total_amount or 0.0

        for item_data in items:
            menu_item = self.menu_repo.get_by_id(item_data.menu_item_id)
            if not menu_item:
                raise HTTPException(status_code=404, detail=f"Menu item not found")

            subtotal = menu_item.price * item_data.quantity
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=item_data.quantity,
                unit_price=menu_item.price,
                subtotal=subtotal,
                special_instructions=item_data.special_instructions,
            )
            self.db.add(order_item)
            total += subtotal

        order.total_amount = round(total, 2)
        self.db.commit()
        self.db.refresh(order)
        return self._to_order_response(order)

    def get_orders(
        self, current_user: CurrentUser,
        page: int = 1, page_size: int = 20,
        status_filter: Optional[str] = None
    ) -> tuple[list[OrderResponse], int]:
        """Get orders for the current user (admin sees country-filtered all)."""
        order_status = OrderStatusEnum(status_filter) if status_filter else None

        if current_user.role == RoleEnum.ADMIN:
            orders, total = self.order_repo.get_all(page, page_size)
        else:
            orders, total = self.order_repo.get_user_orders(
                current_user.id, current_user.country, page, page_size, order_status
            )

        result = [self._to_order_response(o) for o in orders]
        return result, total

    def get_order(self, order_id: str, current_user: CurrentUser) -> OrderResponse:
        """Get a single order with authorization checks."""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Ownership + country check
        if current_user.role != RoleEnum.ADMIN:
            if order.user_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not your order")
            CountryGuard.validate(current_user.country, order.country)

        return self._to_order_response(order)

    def checkout(
        self, order_id: str, checkout_data: CheckoutRequest,
        current_user: CurrentUser
    ) -> OrderResponse:
        """Checkout an order: validate, process payment, update status."""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if current_user.role != RoleEnum.ADMIN:
            if order.user_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not your order")
            CountryGuard.validate(current_user.country, order.country)

        if order.status != OrderStatusEnum.CART:
            raise HTTPException(status_code=400, detail="Order has already been placed or processed")

        # Validate payment method
        payment_method = self.payment_method_repo.get_by_id(checkout_data.payment_method_id)
        if not payment_method or payment_method.user_id != current_user.id:
            raise HTTPException(status_code=400, detail="Invalid payment method")

        # Create payment
        payment = Payment(
            order_id=order.id,
            payment_method_id=payment_method.id,
            amount=order.total_amount,
            status=PaymentStatusEnum.COMPLETED,
            transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
            paid_at=datetime.now(timezone.utc),
        )
        self.db.add(payment)

        order.status = OrderStatusEnum.CONFIRMED
        self.db.commit()
        self.db.refresh(order)

        logger.info("order_checked_out", order_id=order.id, amount=order.total_amount)
        return self._to_order_response(order)

    def cancel_order(self, order_id: str, current_user: CurrentUser) -> OrderResponse:
        """Cancel an order. Only allowed for CART/PLACED/CONFIRMED statuses."""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if current_user.role != RoleEnum.ADMIN:
            if order.user_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not your order")
            CountryGuard.validate(current_user.country, order.country)

        cancellable = {OrderStatusEnum.CART, OrderStatusEnum.PLACED, OrderStatusEnum.CONFIRMED}
        if order.status not in cancellable:
            raise HTTPException(status_code=400, detail=f"Cannot cancel order with status {order.status.value}")

        order.status = OrderStatusEnum.CANCELLED

        # Refund if payment exists
        if order.payment and order.payment.status == PaymentStatusEnum.COMPLETED:
            order.payment.status = PaymentStatusEnum.REFUNDED

        self.db.commit()
        self.db.refresh(order)

        logger.info("order_cancelled", order_id=order.id)
        return self._to_order_response(order)

    def update_order_payment(
        self, order_id: str, payment_method_id: str,
        current_user: CurrentUser
    ) -> OrderResponse:
        """Update the payment method for an order."""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if current_user.role != RoleEnum.ADMIN:
            if order.user_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not your order")

        payment_method = self.payment_method_repo.get_by_id(payment_method_id)
        if not payment_method or payment_method.user_id != current_user.id:
            raise HTTPException(status_code=400, detail="Invalid payment method")

        if order.payment:
            order.payment.payment_method_id = payment_method.id
        else:
            payment = Payment(
                order_id=order.id,
                payment_method_id=payment_method.id,
                amount=order.total_amount,
                status=PaymentStatusEnum.PENDING,
            )
            self.db.add(payment)

        self.db.commit()
        self.db.refresh(order)
        return self._to_order_response(order)

    def _to_order_response(self, order: Order) -> OrderResponse:
        """Convert Order model to OrderResponse schema."""
        items = []
        for oi in (order.order_items or []):
            items.append(OrderItemResponse(
                id=oi.id,
                menu_item_id=oi.menu_item_id,
                menu_item_name=oi.menu_item.name if oi.menu_item else None,
                quantity=oi.quantity,
                unit_price=oi.unit_price,
                subtotal=oi.subtotal,
                special_instructions=oi.special_instructions,
            ))

        payment = None
        if order.payment:
            payment = PaymentResponse(
                id=order.payment.id,
                order_id=order.payment.order_id,
                payment_method_id=order.payment.payment_method_id,
                amount=order.payment.amount,
                status=order.payment.status.value if isinstance(order.payment.status, PaymentStatusEnum) else order.payment.status,
                transaction_id=order.payment.transaction_id,
                paid_at=order.payment.paid_at,
                created_at=order.payment.created_at,
            )

        return OrderResponse(
            id=order.id,
            user_id=order.user_id,
            restaurant_id=order.restaurant_id,
            restaurant_name=order.restaurant.name if order.restaurant else None,
            country=order.country.value if isinstance(order.country, CountryEnum) else order.country,
            status=order.status.value if isinstance(order.status, OrderStatusEnum) else order.status,
            total_amount=order.total_amount,
            notes=order.notes,
            items=items,
            payment=payment,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )


# ─── Payment Method Service ─────────────────────────────────────────────────

class PaymentMethodService:
    def __init__(self, db: Session):
        self.db = db
        self.pm_repo = PaymentMethodRepository(db)

    def get_methods(self, current_user: CurrentUser) -> list[PaymentMethodResponse]:
        """Get all payment methods for the current user."""
        methods = self.pm_repo.get_user_methods(current_user.id)
        return [
            PaymentMethodResponse(
                id=m.id,
                user_id=m.user_id,
                method_type=m.method_type.value if isinstance(m.method_type, PaymentMethodEnum) else m.method_type,
                label=m.label,
                details=m.details,
                is_default=m.is_default,
                created_at=m.created_at,
            )
            for m in methods
        ]

    def create_method(
        self, data: PaymentMethodCreate, current_user: CurrentUser
    ) -> PaymentMethodResponse:
        """Create a new payment method."""
        method = PaymentMethod(
            user_id=current_user.id,
            method_type=PaymentMethodEnum(data.method_type),
            label=data.label,
            details=data.details,
            is_default=data.is_default,
        )

        # If this is the default, unset others
        if data.is_default:
            existing = self.pm_repo.get_user_methods(current_user.id)
            for m in existing:
                m.is_default = False

        method = self.pm_repo.create(method)
        return PaymentMethodResponse(
            id=method.id,
            user_id=method.user_id,
            method_type=method.method_type.value if isinstance(method.method_type, PaymentMethodEnum) else method.method_type,
            label=method.label,
            details=method.details,
            is_default=method.is_default,
            created_at=method.created_at,
        )

    def update_method(
        self, method_id: str, data: PaymentMethodUpdate, current_user: CurrentUser
    ) -> PaymentMethodResponse:
        """Update a payment method."""
        method = self.pm_repo.get_by_id(method_id)
        if not method or method.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Payment method not found")

        if data.method_type is not None:
            method.method_type = PaymentMethodEnum(data.method_type)
        if data.label is not None:
            method.label = data.label
        if data.details is not None:
            method.details = data.details
        if data.is_default is not None:
            if data.is_default:
                existing = self.pm_repo.get_user_methods(current_user.id)
                for m in existing:
                    m.is_default = False
            method.is_default = data.is_default

        method = self.pm_repo.update(method)
        return PaymentMethodResponse(
            id=method.id,
            user_id=method.user_id,
            method_type=method.method_type.value if isinstance(method.method_type, PaymentMethodEnum) else method.method_type,
            label=method.label,
            details=method.details,
            is_default=method.is_default,
            created_at=method.created_at,
        )

    def delete_method(self, method_id: str, current_user: CurrentUser) -> None:
        """Delete a payment method."""
        method = self.pm_repo.get_by_id(method_id)
        if not method or method.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Payment method not found")
        self.pm_repo.delete(method)


# ─── Dashboard Service ───────────────────────────────────────────────────────

class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.restaurant_repo = RestaurantRepository(db)
        self.user_repo = UserRepository(db)

    def get_stats(self, current_user: CurrentUser) -> DashboardStats:
        """Get dashboard statistics."""
        from sqlalchemy import func

        country_filter = None if current_user.role == RoleEnum.ADMIN else current_user.country

        # Total orders
        order_query = self.db.query(func.count(Order.id))
        if country_filter:
            order_query = order_query.filter(Order.country == country_filter)
        total_orders = order_query.scalar() or 0

        # Revenue
        total_revenue = self.order_repo.get_total_revenue(country_filter)

        # Restaurants
        rest_query = self.db.query(func.count(Restaurant.id)).filter(Restaurant.is_active == True)
        if country_filter:
            rest_query = rest_query.filter(Restaurant.country == country_filter)
        total_restaurants = rest_query.scalar() or 0

        # Users
        total_users = self.db.query(func.count(User.id)).scalar() or 0

        # Recent orders
        if current_user.role == RoleEnum.ADMIN:
            recent, _ = self.order_repo.get_all(page=1, page_size=5)
        else:
            recent, _ = self.order_repo.get_user_orders(
                current_user.id, current_user.country, page=1, page_size=5
            )

        order_service = OrderService(self.db)
        recent_responses = [order_service._to_order_response(o) for o in recent]

        # Orders by status
        orders_by_status = self.order_repo.count_by_status(country_filter)

        return DashboardStats(
            total_orders=total_orders,
            total_revenue=round(total_revenue, 2),
            total_restaurants=total_restaurants,
            total_users=total_users,
            recent_orders=recent_responses,
            orders_by_status=orders_by_status,
        )
