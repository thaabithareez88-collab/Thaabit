
import sqlite3
from pathlib import Path

# Get the main project folder
PROJECT_FOLDER = Path(__file__).resolve().parent.parent

# Database file location
DATABASE_PATH = PROJECT_FOLDER / "database" / "inventory.db"


def connect_database():
    """Connect to the database."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    """Create the database tables."""

    connection = connect_database()
    cursor = connection.cursor()

    # Categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        )
    """)

    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER,
            price REAL NOT NULL CHECK(price >= 0),
            quantity INTEGER NOT NULL DEFAULT 0 CHECK(quantity >= 0),
            reorder_level INTEGER NOT NULL DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id)
                REFERENCES categories(category_id)
                ON DELETE SET NULL
        )
    """)

    # Stock transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL
                CHECK(transaction_type IN ('IN', 'OUT')),
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            note TEXT,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully!")
    print(f"Database location: {DATABASE_PATH}")
