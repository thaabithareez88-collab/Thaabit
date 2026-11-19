
from database import connect_database


def add_product(name, category_id, price, quantity, reorder_level=5):
    """Add a new product to the database."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products
        (name, category_id, price, quantity, reorder_level)
        VALUES (?, ?, ?, ?, ?)
    """, (name, category_id, price, quantity, reorder_level))

    product_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return product_id


def get_all_products():
    """Return all products."""

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            products.product_id,
            products.name,
            categories.category_name,
            products.price,
            products.quantity,
            products.reorder_level
        FROM products
        LEFT JOIN categories
        ON products.category_id = categories.category_id
        ORDER BY products.product_id DESC
    """)

    products = cursor.fetchall()

    connection.close()

    return products


def search_products(keyword):
    """Search products by name."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_id, name, category_id, price, quantity
        FROM products
        WHERE name LIKE ?
        ORDER BY product_id DESC
    """, (f"%{keyword}%",))

    products = cursor.fetchall()

    connection.close()

    return products


def update_product(product_id, name, category_id, price, reorder_level):
    """Update product details."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE products
        SET name = ?,
            category_id = ?,
            price = ?,
            reorder_level = ?
        WHERE product_id = ?
    """, (name, category_id, price, reorder_level, product_id))

    connection.commit()
    updated = cursor.rowcount > 0
    connection.close()

    return updated


def delete_product(product_id):
    """Delete a product."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM products
        WHERE product_id = ?
    """, (product_id,))

    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()

    return deleted
