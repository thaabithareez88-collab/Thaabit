
from products import add_product
from stock import (
    stock_in,
    stock_out,
    get_stock_transactions,
    get_low_stock_products
)

# Create a test product
product_id = add_product(
    name="Stock Test Product",
    category_id=None,
    price=1000,
    quantity=20,
    reorder_level=5
)

print("Product created. Initial stock: 20")

# Test stock in
result = stock_in(product_id, 10, "Purchased new stock")
print("\nStock In:", result)

# Test stock out
result = stock_out(product_id, 5, "Sold to customer")
print("Stock Out:", result)

# Test insufficient stock
result = stock_out(product_id, 100, "Test insufficient stock")
print("Insufficient Stock Test:", result)

# Display transaction history
print("\nTRANSACTION HISTORY")

for transaction in get_stock_transactions():
    print(transaction)

# Display low stock products
print("\nLOW STOCK PRODUCTS")

for product in get_low_stock_products():
    print(product)
