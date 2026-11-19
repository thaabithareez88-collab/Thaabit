
from database import connect_database


def get_dashboard_summary():
    """Get important inventory figures for the dashboard."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM products
    """)
    total_products = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(quantity), 0)
        FROM products
    """)
    total_stock = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(price * quantity), 0)
        FROM products
    """)
    inventory_value = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE quantity <= reorder_level
    """)
    low_stock_count = cursor.fetchone()[0]

    connection.close()

    return {
        "total_products": total_products,
        "total_stock": total_stock,
        "inventory_value": inventory_value,
        "low_stock_count": low_stock_count
    }


def get_product_report():
    """Get a complete product report."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            products.product_id,
            products.name,
            categories.category_name,
            products.price,
            products.quantity,
            products.price * products.quantity AS total_value
        FROM products
        LEFT JOIN categories
        ON products.category_id = categories.category_id
        ORDER BY products.name
    """)

    report = cursor.fetchall()
    connection.close()

    return report


def get_stock_report():
    """Get stock levels and reorder information."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            product_id,
            name,
            quantity,
            reorder_level,
            CASE
                WHEN quantity <= reorder_level THEN 'LOW STOCK'
                ELSE 'AVAILABLE'
            END AS stock_status
        FROM products
        ORDER BY quantity ASC
    """)

    report = cursor.fetchall()
    connection.close()

    return report


def get_transaction_report():
    """Get all stock transactions."""

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

    report = cursor.fetchall()
    connection.close()

    return report
