
from products import (
    add_product,
    search_products,
    update_product,
    delete_product,
    get_all_products
)

# 1. Add a test product
product_id = add_product(
    name="Test Keyboard",
    category_id=None,
    price=3500,
    quantity=10,
    reorder_level=5
)

print("1. Product added:", product_id)


# 2. Search for the product
results = search_products("Test Keyboard")

print("\n2. Search results:")
for product in results:
    print(product)


# 3. Update the product
updated = update_product(
    product_id,
    "Test Keyboard",
    None,
    4000,
    8
)

print("\n3. Product updated:", updated)


# 4. Delete the test product
deleted = delete_product(product_id)

print("\n4. Product deleted:", deleted)


# 5. Verify deletion
remaining_products = get_all_products()

still_exists = any(
    product[0] == product_id
    for product in remaining_products
)

print("\n5. Product still exists:", still_exists)
