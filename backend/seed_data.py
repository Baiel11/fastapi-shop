import random
from faker import Faker
from app.core.database import SessionLocal
from app.models.category import Category
from app.models.product import Product

"""
Script for populating the database with realistic test data.
Combines Faker-generated descriptions with curated product name lists
and category-specific Unsplash images to produce 100 believable products.

Usage:
    python seed_data.py
"""

fake = Faker()

# ── Product Name Lists (per category) ────────────────────────────────────────

ELECTRONICS_NAMES = [
    "Wireless Mouse", "Mechanical Keyboard", "Gaming Monitor", "Bluetooth Speaker",
    "USB-C Hub", "Laptop Stand", "Webcam HD", "External SSD", "Wireless Charger",
    "Smart Watch", "Noise-Cancelling Headphones", "LED Desk Lamp", "Portable Projector",
    "Ring Light", "Wireless Earbuds", "Phone Tripod", "Power Bank 20000mAh",
    "Mini Drone", "Drawing Tablet", "Smart Home Hub", "HDMI Cable 4K", "VR Headset",
    "Gaming Mouse Pad", "USB Flash Drive 128GB", "Smart Plug Wi-Fi", "Bluetooth Receiver",
    "Portable SSD 1TB", "Microphone Condenser", "Action Camera 4K", "Laptop Sleeve",
]

CLOTHING_NAMES = [
    "Running Shoes", "Denim Jacket", "Black Hoodie", "Cotton T-Shirt", "Baseball Cap",
    "Leather Sneakers", "Jogger Pants", "Windbreaker Jacket", "Graphic Tee",
    "Athletic Shorts", "Zip-Up Hoodie", "Slim Fit Chinos", "Bomber Jacket",
    "Crew Neck Sweater", "Puffer Vest", "Canvas Backpack", "Sling Bag",
    "Ankle Socks Pack", "Beanie Hat", "Crossbody Bag", "Leather Belt", "Fleece Pullover",
    "Rain Coat", "Pajama Set", "Swim Shorts", "Running Socks", "Cargo Pants",
    "Scarf Cashmere", "Leather Gloves", "Polo Shirt",
]

BOOKS_NAMES = [
    "Python Crash Course", "Clean Code", "The Pragmatic Programmer",
    "Designing Data-Intensive Applications", "Deep Work", "Atomic Habits",
    "The Lean Startup", "Zero to One", "Thinking, Fast and Slow",
    "The Psychology of Money", "Rich Dad Poor Dad", "A Brief History of Time",
    "Sapiens", "The Alchemist", "1984", "Dune", "The Great Gatsby",
    "To Kill a Mockingbird", "The Hitchhiker's Guide to the Galaxy", "Educated",
    "Introduction to Algorithms", "Computer Networks", "Refactoring", "Clean Architecture",
    "Domain-Driven Design", "JavaScript: The Good Parts", "Effective C++", "Fluent Python",
    "Rust in Action", "The Phoenix Project",
]

HOME_GARDEN_NAMES = [
    "Ceramic Plant Pot", "Bamboo Cutting Board", "Essential Oil Diffuser",
    "Scented Candle Set", "Stainless Steel Water Bottle", "French Press Coffee Maker",
    "Non-Stick Frying Pan", "Glass Food Containers", "Throw Pillow Cover",
    "Linen Duvet Set", "LED Fairy Lights", "Bathroom Organizer",
    "Hanging Wall Shelf", "Magnetic Knife Strip", "Vegetable Seed Kit",
    "Indoor Herb Garden", "Compost Bin", "Garden Gloves Set", "Watering Can",
    "Doormat with Quote", "Desk Organizer", "Wall Clock Modern", "Plant Stand Wood",
    "Self-Watering Pot", "Throw Blanket Knit", "Storage Baskets Set", "Bath Towels Set",
    "Kitchen Scale Digital", "Electric Kettle", "Garden Hose Expandable",
]

# ── Category-Specific Images ──────────────────────────────────────────────────
# Multiple images per category ensure variety across generated products.

ELECTRONICS_IMAGES = [
    "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=500",
    "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500",
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500",
    "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=500",
    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
    "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=500",
    "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=500",
    "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=500",
]

CLOTHING_IMAGES = [
    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500",
    "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500",
    "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=500",
    "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500",
    "https://images.unsplash.com/photo-1525507119028-ed4c629a60a3?w=500",
    "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500",
    "https://images.unsplash.com/photo-1516762689617-e1cffcef479d?w=500",
    "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=500",
]

BOOKS_IMAGES = [
    "https://images.unsplash.com/photo-1589998059171-988d887df646?w=500",
    "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
    "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=500",
    "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=500",
    "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=500",
    "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=500",
]

HOME_GARDEN_IMAGES = [
    "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=500",
    "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500",
    "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=500",
    "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=500",
    "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=500",
    "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=500",
]

# ── Price Ranges per Category (min, max) ──────────────────────────────────────

PRICE_RANGES = {
    "electronics":  (29.99,  1499.99),
    "clothing":     (14.99,   299.99),
    "books":        ( 9.99,    59.99),
    "home-garden":  (12.99,   249.99),
}

# ── Category Configuration ────────────────────────────────────────────────────

CATEGORY_CONFIG = {
    "electronics": {
        "names":  ELECTRONICS_NAMES,
        "images": ELECTRONICS_IMAGES,
        "count":  25,
    },
    "clothing": {
        "names":  CLOTHING_NAMES,
        "images": CLOTHING_IMAGES,
        "count":  25,
    },
    "books": {
        "names":  BOOKS_NAMES,
        "images": BOOKS_IMAGES,
        "count":  25,
    },
    "home-garden": {
        "names":  HOME_GARDEN_NAMES,
        "images": HOME_GARDEN_IMAGES,
        "count":  25,
    },
}


def create_categories(db: SessionLocal) -> dict[str, Category]:
    """
    Create product categories.

    Args:
        db: SQLAlchemy session

    Returns:
        dict: Dictionary of created categories {slug: Category}
    """
    categories_data = [
        {"name": "Electronics",   "slug": "electronics"},
        {"name": "Clothing",      "slug": "clothing"},
        {"name": "Books",         "slug": "books"},
        {"name": "Home & Garden", "slug": "home-garden"},
    ]

    categories = {}
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.add(category)
        categories[cat_data["slug"]] = category

    db.commit()

    # Refresh all objects after commit so their IDs are populated
    for category in categories.values():
        db.refresh(category)

    return categories


def create_products(db: SessionLocal, categories: dict[str, Category]) -> None:
    """
    Generate 100 realistic products using Faker + curated name lists.

    Each category produces 25 products with:
    - Name: chosen from a curated list relevant to the category
    - Description: 2-sentence paragraph from Faker
    - Price: randomized within a realistic range for the category
    - Image: randomly selected from a category-specific image pool

    Args:
        db: SQLAlchemy session
        categories: Dictionary of {slug: Category} from create_categories()
    """
    total = 0

    for slug, config in CATEGORY_CONFIG.items():
        category = categories[slug]
        min_price, max_price = PRICE_RANGES[slug]
        names = config["names"].copy()

        # Shuffle the names so the order is different on each seed run
        random.shuffle(names)

        for i in range(config["count"]):
            # Cycle through names if count exceeds unique name pool size
            name = names[i % len(names)]

            product = Product(
                name=name,
                description=fake.paragraph(nb_sentences=2),
                price=round(random.uniform(min_price, max_price), 2),
                category_id=category.id,
                image_url=random.choice(config["images"]),
            )

            db.add(product)
            total += 1

    db.commit()
    return total


def seed_database() -> None:
    """
    Main entry point for populating the database.
    Skips seeding if data already exists to prevent duplicates.
    """
    print("Starting database seeding...")

    db = SessionLocal()

    try:
        existing = db.query(Category).count()
        if existing > 0:
            print(f"Database already has {existing} categories. Skipping seed.")
            return

        print("Creating categories...")
        categories = create_categories(db)
        print(f"  ✓ {len(categories)} categories created")

        print("Creating products...")
        total = create_products(db, categories)
        print(f"  ✓ {total} products created")

        print("\nDatabase seeding completed successfully!")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()