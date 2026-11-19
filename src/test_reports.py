
from reports import (
    get_dashboard_summary,
    get_product_report,
    get_stock_report,
    get_transaction_report
)

# 1. Dashboard summary
print("DASHBOARD SUMMARY")
summary = get_dashboard_summary()

for key, value in summary.items():
    print(key, ":", value)


# 2. Product report
print("\nPRODUCT REPORT")

for product in get_product_report():
    print(product)


# 3. Stock report
print("\nSTOCK REPORT")

for product in get_stock_report():
    print(product)


# 4. Transaction report
print("\nTRANSACTION REPORT")

for transaction in get_transaction_report():
    print(transaction)
