"""
Database seed data for the Slooze Food Ordering Platform.

Seeds users, restaurants, menu items, and payment methods
with realistic test data.
"""

from app.database.session import SessionLocal, engine
from app.models.models import (
    Base, User, Restaurant, MenuItem, PaymentMethod,
    RoleEnum, CountryEnum, PaymentMethodEnum
)
from app.core.security import hash_password
from app.core.logging import get_logger

logger = get_logger("seed")


def seed_database():
    """Seed the database with initial data."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).first():
            logger.info("Database already seeded, skipping...")
            return

        logger.info("Seeding database...")

        # ─── Users ───────────────────────────────────────────────────────

        users = [
            User(
                id="usr-nick-fury",
                email="nick.fury@shield.gov",
                username="nick.fury",
                full_name="Nick Fury",
                hashed_password=hash_password("password123"),
                role=RoleEnum.ADMIN,
                country=CountryEnum.AMERICA,
                avatar_url="https://ui-avatars.com/api/?name=Nick+Fury&background=6366f1&color=fff&size=128",
            ),
            User(
                id="usr-captain-marvel",
                email="carol.danvers@shield.gov",
                username="captain.marvel",
                full_name="Captain Marvel",
                hashed_password=hash_password("password123"),
                role=RoleEnum.MANAGER,
                country=CountryEnum.INDIA,
                avatar_url="https://ui-avatars.com/api/?name=Captain+Marvel&background=ec4899&color=fff&size=128",
            ),
            User(
                id="usr-captain-america",
                email="steve.rogers@shield.gov",
                username="captain.america",
                full_name="Captain America",
                hashed_password=hash_password("password123"),
                role=RoleEnum.MANAGER,
                country=CountryEnum.AMERICA,
                avatar_url="https://ui-avatars.com/api/?name=Captain+America&background=3b82f6&color=fff&size=128",
            ),
            User(
                id="usr-thanos",
                email="thanos@titan.space",
                username="thanos",
                full_name="Thanos",
                hashed_password=hash_password("password123"),
                role=RoleEnum.MEMBER,
                country=CountryEnum.INDIA,
                avatar_url="https://ui-avatars.com/api/?name=Thanos&background=8b5cf6&color=fff&size=128",
            ),
            User(
                id="usr-thor",
                email="thor@asgard.realm",
                username="thor",
                full_name="Thor Odinson",
                hashed_password=hash_password("password123"),
                role=RoleEnum.MEMBER,
                country=CountryEnum.INDIA,
                avatar_url="https://ui-avatars.com/api/?name=Thor&background=f59e0b&color=fff&size=128",
            ),
            User(
                id="usr-travis",
                email="travis@avengers.org",
                username="travis",
                full_name="Travis",
                hashed_password=hash_password("password123"),
                role=RoleEnum.MEMBER,
                country=CountryEnum.AMERICA,
                avatar_url="https://ui-avatars.com/api/?name=Travis&background=10b981&color=fff&size=128",
            ),
        ]
        db.add_all(users)
        db.flush()

        # ─── Indian Restaurants ──────────────────────────────────────────

        indian_restaurants = [
            Restaurant(
                id="rest-taj-mahal",
                name="Taj Mahal Palace Kitchen",
                description="Experience the royal flavors of India with our authentic Mughlai cuisine, crafted by master chefs with centuries-old recipes.",
                cuisine_type="Mughlai",
                country=CountryEnum.INDIA,
                address="Apollo Bunder, Colaba, Mumbai 400001",
                rating=4.8,
                image_url="https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800",
                delivery_time_mins=35,
            ),
            Restaurant(
                id="rest-spice-garden",
                name="Spice Garden",
                description="A South Indian culinary haven serving traditional dosas, idlis, and authentic Kerala cuisine.",
                cuisine_type="South Indian",
                country=CountryEnum.INDIA,
                address="MG Road, Bangalore 560001",
                rating=4.5,
                image_url="https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a?w=800",
                delivery_time_mins=25,
            ),
            Restaurant(
                id="rest-punjab-dhaba",
                name="Punjab Da Dhaba",
                description="The heartiest North Indian comfort food — butter chicken, naan, and lassi that will transport you to the streets of Amritsar.",
                cuisine_type="Punjabi",
                country=CountryEnum.INDIA,
                address="Connaught Place, New Delhi 110001",
                rating=4.6,
                image_url="https://images.unsplash.com/photo-1596797038530-2c107229654b?w=800",
                delivery_time_mins=30,
            ),
        ]

        # ─── American Restaurants ────────────────────────────────────────

        american_restaurants = [
            Restaurant(
                id="rest-liberty-grill",
                name="Liberty Grill & Steakhouse",
                description="Premium USDA Prime steaks grilled to perfection, paired with craft cocktails and a stunning Manhattan view.",
                cuisine_type="American Steakhouse",
                country=CountryEnum.AMERICA,
                address="5th Avenue, New York, NY 10001",
                rating=4.7,
                image_url="https://images.unsplash.com/photo-1544025162-d76694265947?w=800",
                delivery_time_mins=40,
            ),
            Restaurant(
                id="rest-golden-gate",
                name="Golden Gate Seafood",
                description="Fresh Pacific seafood and California-style cuisine, sourced daily from sustainable fisheries.",
                cuisine_type="Seafood",
                country=CountryEnum.AMERICA,
                address="Fisherman's Wharf, San Francisco, CA 94133",
                rating=4.4,
                image_url="https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=800",
                delivery_time_mins=35,
            ),
            Restaurant(
                id="rest-smoky-bbq",
                name="Smoky Mountain BBQ",
                description="Slow-smoked Texas-style BBQ with house-made sauces and authentic pit-master techniques.",
                cuisine_type="BBQ",
                country=CountryEnum.AMERICA,
                address="Main Street, Austin, TX 78701",
                rating=4.6,
                image_url="https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=800",
                delivery_time_mins=45,
            ),
        ]

        all_restaurants = indian_restaurants + american_restaurants
        db.add_all(all_restaurants)
        db.flush()

        # ─── Indian Menu Items ───────────────────────────────────────────

        indian_menu_items = [
            # Taj Mahal Palace Kitchen
            MenuItem(restaurant_id="rest-taj-mahal", name="Butter Chicken", description="Tender chicken in rich tomato-butter gravy", price=450.0, category="Main Course", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400"),
            MenuItem(restaurant_id="rest-taj-mahal", name="Paneer Tikka Masala", description="Grilled cottage cheese in spiced tomato sauce", price=380.0, category="Main Course", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400"),
            MenuItem(restaurant_id="rest-taj-mahal", name="Biryani Hyderabadi", description="Fragrant basmati rice with aromatic spices and tender meat", price=520.0, category="Rice", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400"),
            MenuItem(restaurant_id="rest-taj-mahal", name="Garlic Naan", description="Soft bread with garlic and butter", price=80.0, category="Bread", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400"),
            MenuItem(restaurant_id="rest-taj-mahal", name="Gulab Jamun", description="Warm milk-solid dumplings in rose syrup", price=180.0, category="Dessert", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1666190050857-22e940730844?w=400"),
            # Spice Garden
            MenuItem(restaurant_id="rest-spice-garden", name="Masala Dosa", description="Crispy rice crepe with spiced potato filling", price=220.0, category="Main Course", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1668236543090-82eb5eae7e10?w=400"),
            MenuItem(restaurant_id="rest-spice-garden", name="Idli Sambar", description="Steamed rice cakes with lentil soup", price=160.0, category="Breakfast", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400"),
            MenuItem(restaurant_id="rest-spice-garden", name="Kerala Fish Curry", description="Fish in coconut milk with curry leaves", price=480.0, category="Main Course", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1626776876729-bab4369a5a5a?w=400"),
            MenuItem(restaurant_id="rest-spice-garden", name="Chettinad Chicken", description="Spicy chicken from the Chettinad region", price=420.0, category="Main Course", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1610057099443-fde6c99db9e1?w=400"),
            MenuItem(restaurant_id="rest-spice-garden", name="Payasam", description="Traditional South Indian sweet pudding", price=150.0, category="Dessert", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1571167530149-c1105da4c2c7?w=400"),
            # Punjab Da Dhaba
            MenuItem(restaurant_id="rest-punjab-dhaba", name="Dal Makhani", description="Creamy black lentils slow-cooked overnight", price=320.0, category="Main Course", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400"),
            MenuItem(restaurant_id="rest-punjab-dhaba", name="Tandoori Chicken", description="Charcoal-grilled chicken marinated in yogurt spices", price=450.0, category="Starter", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400"),
            MenuItem(restaurant_id="rest-punjab-dhaba", name="Chole Bhature", description="Spicy chickpeas with deep-fried bread", price=250.0, category="Main Course", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=400"),
            MenuItem(restaurant_id="rest-punjab-dhaba", name="Lassi", description="Traditional Punjabi sweet yogurt drink", price=120.0, category="Beverages", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1571006682205-08b30c5c4265?w=400"),
        ]

        # ─── American Menu Items ─────────────────────────────────────────

        american_menu_items = [
            # Liberty Grill
            MenuItem(restaurant_id="rest-liberty-grill", name="USDA Prime Ribeye", description="16oz prime ribeye, chargrilled, served with truffle mash", price=65.0, category="Steaks", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1600891964092-4316c288032e?w=400"),
            MenuItem(restaurant_id="rest-liberty-grill", name="Classic Burger", description="Angus beef patty with aged cheddar and house sauce", price=22.0, category="Burgers", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400"),
            MenuItem(restaurant_id="rest-liberty-grill", name="Caesar Salad", description="Romaine lettuce with parmesan and croutons", price=16.0, category="Salads", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=400"),
            MenuItem(restaurant_id="rest-liberty-grill", name="New York Cheesecake", description="Classic creamy cheesecake with berry compote", price=14.0, category="Desserts", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1524351199432-d330df18e76e?w=400"),
            MenuItem(restaurant_id="rest-liberty-grill", name="Craft IPA", description="Local craft India Pale Ale", price=9.0, category="Beverages", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=400"),
            # Golden Gate Seafood
            MenuItem(restaurant_id="rest-golden-gate", name="Dungeness Crab", description="Fresh whole Dungeness crab with drawn butter", price=55.0, category="Seafood", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1559737558-2f5a35f4523b?w=400"),
            MenuItem(restaurant_id="rest-golden-gate", name="Clam Chowder", description="San Francisco-style clam chowder in sourdough bowl", price=18.0, category="Soups", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1588710920068-1r1a0cd9b7a4?w=400"),
            MenuItem(restaurant_id="rest-golden-gate", name="Grilled Salmon", description="Pacific wild salmon with lemon dill sauce", price=38.0, category="Seafood", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400"),
            MenuItem(restaurant_id="rest-golden-gate", name="Fish & Chips", description="Beer-battered cod with crispy fries", price=24.0, category="Classics", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1579208030886-b1715a0e76f6?w=400"),
            # Smoky Mountain BBQ
            MenuItem(restaurant_id="rest-smoky-bbq", name="Brisket Plate", description="12-hour smoked brisket with coleslaw and beans", price=28.0, category="BBQ", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=400"),
            MenuItem(restaurant_id="rest-smoky-bbq", name="Pulled Pork Sandwich", description="Slow-smoked pulled pork with tangy sauce", price=18.0, category="Sandwiches", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1586816001966-79b736744398?w=400"),
            MenuItem(restaurant_id="rest-smoky-bbq", name="Baby Back Ribs", description="Full rack of ribs with house BBQ glaze", price=35.0, category="BBQ", is_vegetarian=False, image_url="https://images.unsplash.com/photo-1544025162-d76694265947?w=400"),
            MenuItem(restaurant_id="rest-smoky-bbq", name="Mac & Cheese", description="Creamy three-cheese macaroni, oven-baked", price=12.0, category="Sides", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1543339494-b4cd4f7ba686?w=400"),
            MenuItem(restaurant_id="rest-smoky-bbq", name="Sweet Tea", description="Classic Southern sweet iced tea", price=5.0, category="Beverages", is_vegetarian=True, image_url="https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400"),
        ]

        db.add_all(indian_menu_items + american_menu_items)
        db.flush()

        # ─── Payment Methods (for Admin) ─────────────────────────────────

        payment_methods = [
            PaymentMethod(
                user_id="usr-nick-fury",
                method_type=PaymentMethodEnum.CREDIT_CARD,
                label="SHIELD Corporate Card",
                details="**** **** **** 1234",
                is_default=True,
            ),
            PaymentMethod(
                user_id="usr-nick-fury",
                method_type=PaymentMethodEnum.UPI,
                label="Personal UPI",
                details="nick@fury.upi",
            ),
            PaymentMethod(
                user_id="usr-captain-marvel",
                method_type=PaymentMethodEnum.CREDIT_CARD,
                label="Avengers Card",
                details="**** **** **** 5678",
                is_default=True,
            ),
            PaymentMethod(
                user_id="usr-captain-america",
                method_type=PaymentMethodEnum.DEBIT_CARD,
                label="Freedom Bank Card",
                details="**** **** **** 9012",
                is_default=True,
            ),
        ]
        db.add_all(payment_methods)

        db.commit()
        logger.info("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        logger.error("seed_failed", error=str(e))
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
