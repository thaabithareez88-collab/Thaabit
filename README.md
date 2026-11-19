
# Inventory Management System

A Python-based desktop application for managing products, inventory, stock movements and reports.

## Features

### Dashboard
- Total product count
- Total stock quantity
- Inventory value
- Low-stock item count

### Product Management
- Add products
- Search products
- Update product details
- Delete products

### Stock Management
- Record stock received (Stock In)
- Record stock issued (Stock Out)
- View stock transaction history
- Identify low-stock products
- Prevent stock removal when quantity is insufficient

### Reports
- Product Report
- Stock Report
- Transaction Report

## Technologies Used

- Python
- CustomTkinter
- SQLite
- Pandas
- Matplotlib

## Project Structure

```text
Inventory-Management-System/
│
├── assets/
├── database/
├── src/
│   ├── database.py
│   ├── main.py
│   ├── products.py
│   ├── reports.py
│   ├── stock.py
│   ├── ui.py
│   ├── test_products.py
│   ├── test_stock.py
│   └── test_reports.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

1. Clone or download this repository.
2. Install Python.
3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

Run the following command from the project root:

```bash
python src/main.py
```

## Database

The application uses SQLite to store inventory and transaction information.

The database is created locally when the application initializes.

## Project Status

Version 1.0 – Core inventory management features implemented and tested.
