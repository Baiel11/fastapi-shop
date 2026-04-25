from app.database import SessionLocal, init_db
from app.models.category import Category
from app.models.product import Product

"""
Script for populating the database with test data.
Creates categories and products for application demonstration.
Uses placeholder images from unsplash.com.
"""

def create_categories(db: SessionLocal) -> dict[str, Category]:
    """
    Create product categories.

    Args:
        db: SQLAlchemy session

    Returns:
        dict: Dictionary of created categories {slug: Category}
    """
    categories_data = [
        {"name": "Electronics", "slug": "electronics"},
        {"name": "Clothing", "slug": "clothing"},
        {"name": "Books", "slug": "books"},
        {"name": "Home & Garden", "slug": "home-garden"},
    ]

    categories = {}
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.add(category)
        categories[cat_data["slug"]] = category

    db.commit()

    # Refresh objects after commit to get IDs
    for category in categories.values():
        db.refresh(category)

    return categories


def create_products(db: SessionLocal, categories: dict[str, Category]) -> None:
    """
    Create products in different categories.

    Args:
        db: SQLAlchemy session
        categories: Dictionary of categories
    """
    products_data = [
        # Electronics
        {
            "name": "Wireless Headphones",
            "description": "High-quality wireless headphones with noise cancellation. Battery life up to 30 hours.",
            "price": 299.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"
        },
        {
            "name": "Smart Watch Pro",
            "description": "Smartwatch with fitness tracking, heart rate monitor, and GPS. Water resistant up to 50m.",
            "price": 399.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400"
        },
        {
            "name": "Laptop Stand",
            "description": "Ergonomic aluminum laptop stand. Adjustable height and angle.",
            "price": 49.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400"
        },

        # Clothing
        {
            "name": "Running Shoes",
            "description": "Comfortable running shoes with cushioning and breathable material.",
            "price": 129.99,
            "category_id": categories["clothing"].id,
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
        },

        # Books
        {
            "name": "Python Programming Guide",
            "description": "Comprehensive guide to Python programming from basics to advanced topics.",
            "price": 45.99,
            "category_id": categories["books"].id,
            "image_url": "https://images.unsplash.com/photo-1589998059171-988d887df646?w=400"
        },

        # Home & Garden
        {
            "name": "Plant Pot Set",
            "description": "Set of ceramic plant pots with drainage holes and modern design.",
            "price": 34.99,
            "category_id": categories["home-garden"].id,
            "image_url": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400"
        },
    ]

    for product_data in products_data:
        product = Product(**product_data)
        db.add(product)

    db.commit()


def seed_database() -> None:
    """
    Main function for populating the database.
    Creates tables, categories, and products.
    """
    print("Starting database seeding...")

    init_db()
    print("Database tables created")

    db = SessionLocal()

    try:
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            print("Database already contains data. Skipping seed.")
            return

        print("Creating categories...")
        categories = create_categories(db)
        print(f"Created {len(categories)} categories")

        print("Creating products...")
        create_products(db, categories)

        print("Database seeding completed successfully")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()