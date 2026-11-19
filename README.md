# Inventory Management System

## 1. Project Overview
The Inventory Management System is a Python-based desktop application designed to manage products, monitor stock levels, maintain inventory records and generate inventory reports.

The system uses an SQLite database to store and manage product information and stock transactions.

## 2. Project Objectives
- Manage product information.
- Monitor stock availability.
- Record stock additions and reductions.
- Identify low-stock products.
- Maintain inventory transaction history.
- Generate inventory reports.

## 3. Technologies Used
- Programming Language: Python
- User Interface: CustomTkinter
- Database: SQLite
- Database Connectivity: Python sqlite3
- Development Environment: Visual Studio Code
- Version Control: GitHub

## 4. Main Features

### Dashboard
- Total products
- Total stock quantity
- Low-stock products
- Total inventory value

### Product Management
- Add products
- Update product details
- Delete products
- Search products

### Stock Management
- Add stock
- Reduce stock
- Monitor stock quantities
- Low-stock alerts

### Inventory Reports
- Product reports
- Stock reports
- Inventory value reports
- Transaction history

## 5. Database
The application uses SQLite to store product details, categories and stock transactions.

## 6. Project Structure
The project is organised into separate modules for the user interface, database connectivity, product management, stock management and reporting.

## 7. Installation
Install the required dependencies:

`pip install -r requirements.txt`

## 8. How to Run
Run the main application:

`python src/main.py`

## 9. Future Improvements
- Export reports to PDF and Excel.
- Barcode scanning.
- User login and authentication.
- Supplier management.
