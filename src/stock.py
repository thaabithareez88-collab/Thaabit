
from database import connect_database


def stock_in(product_id, quantity, note="Stock received"):
    """Increase product stock and record the transaction."""

    if quantity <= 0:
        return False, "Quantity must be greater than zero."

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT product_id FROM products WHERE product_id = ?",
            (product_id,)
        )

        if cursor.fetchone() is None:
            return False, "Product not found."

        cursor.execute("""
            UPDATE products
            SET quantity = quantity + ?
            WHERE product_id = ?
        """, (quantity, product_id))

        cursor.execute("""
            INSERT INTO stock_transactions
            (product_id, transaction_type, quantity, note)
            VALUES (?, 'IN', ?, ?)
        """, (product_id, quantity, note))

        connection.commit()
        return True, "Stock added successfully."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


def stock_out(product_id, quantity, note="Stock issued"):
    """Decrease product stock and record the transaction."""

    if quantity <= 0:
        return False, "Quantity must be greater than zero."

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT quantity FROM products
            WHERE product_id = ?
        """, (product_id,))

        result = cursor.fetchone()

        if result is None:
            return False, "Product not found."

        current_quantity = result[0]

        if quantity > current_quantity:
            return False, "Insufficient stock."

        cursor.execute("""
            UPDATE products
            SET quantity = quantity - ?
            WHERE product_id = ?
        """, (quantity, product_id))

        cursor.execute("""
            INSERT INTO stock_transactions
            (product_id, transaction_type, quantity, note)
            VALUES (?, 'OUT', ?, ?)
        """, (product_id, quantity, note))

        connection.commit()
        return True, "Stock removed successfully."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


def get_stock_transactions():
    """Get complete stock transaction history."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            stock_transactions.transaction_id,
            products.name,
            stock_transactions.transaction_type,
            stock_transactions.quantity,
            stock_transactions.note,
            stock_transactions.transaction_date
        FROM stock_transactions
        JOIN products
        ON stock_transactions.product_id = products.product_id
        ORDER BY stock_transactions.transaction_id DESC
    """)

    transactions = cursor.fetchall()
    connection.close()

    return transactions


def get_low_stock_products():
    """Get products at or below their reorder level."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_id, name, price, quantity, reorder_level
        FROM products
        WHERE quantity <= reorder_level
        ORDER BY quantity ASC
    """)

    products = cursor.fetchall()
    connection.close()

    return products
