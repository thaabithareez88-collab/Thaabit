import sqlite3
import os

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "database",
    "inventory.db"
)

def connect_database():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)

def create_tables():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()
