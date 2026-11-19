
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from reports import (
    get_dashboard_summary,
    get_product_report,
    get_stock_report,
    get_transaction_report
)
from products import (
    add_product,
    get_all_products,
    search_products,
    update_product,
    delete_product
)
from stock import (
    stock_in,
    stock_out,
    get_stock_transactions,
    get_low_stock_products
)

class InventoryApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Inventory Management System")
        self.geometry("1200x750")
        self.minsize(950, 600)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Main layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Application title
        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="INVENTORY\nMANAGEMENT",
            font=("Arial", 21, "bold")
        )
        self.logo.pack(pady=(35, 40), padx=15)

        # Navigation buttons
        self.create_navigation_button("Dashboard", "dashboard")
        self.create_navigation_button("Products", "products")
        self.create_navigation_button("Stock Management", "stock")
        self.create_navigation_button("Reports", "reports")

        # Main content area
        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#F4F6FA"
        )
        self.content.grid(row=0, column=1, sticky="nsew")

        self.show_page("dashboard")

    def create_navigation_button(self, text, page):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=45,
            anchor="w",
            font=("Arial", 14),
            command=lambda: self.show_page(page)
        )
        button.pack(fill="x", padx=15, pady=7)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_page(self, page):
        self.clear_content()

        if page == "dashboard":
            self.show_dashboard()

        elif page == "products":
            self.show_products()

        elif page == "stock":
            self.show_stock()

        elif page == "reports":
            self.show_reports()

        else:
            title = page.replace("_", " ").title()

            heading = ctk.CTkLabel(
                self.content,
                text=title,
                font=("Arial", 28, "bold")
            )
            heading.pack(anchor="w", padx=35, pady=(35, 15))

            message = ctk.CTkLabel(
                self.content,
                text="This section will be developed next.",
                font=("Arial", 15)
            )
            message.pack(anchor="w", padx=35, pady=10)

    def show_products(self):
        heading = ctk.CTkLabel(
            self.content,
            text="Products",
            font=("Arial", 30, "bold"),
            text_color="#172033"
        )
        heading.pack(anchor="w", padx=35, pady=(35, 5))

        subtitle = ctk.CTkLabel(
            self.content,
            text="Manage your inventory products",
            font=("Arial", 14),
            text_color="#667085"
        )
        subtitle.pack(anchor="w", padx=35, pady=(0, 25))

        form_frame = ctk.CTkFrame(self.content, fg_color="white")
        form_frame.pack(fill="x", padx=35, pady=10)

        self.product_name = ctk.CTkEntry(
            form_frame,
            placeholder_text="Product Name",
            width=200
        )
        self.product_name.pack(side="left", padx=10, pady=15)

        self.product_price = ctk.CTkEntry(
            form_frame,
            placeholder_text="Price",
            width=130
        )
        self.product_price.pack(side="left", padx=10, pady=15)

        self.product_quantity = ctk.CTkEntry(
            form_frame,
            placeholder_text="Initial Quantity",
            width=150
        )
        self.product_quantity.pack(side="left", padx=10, pady=15)

        add_button = ctk.CTkButton(
            form_frame,
            text="Add Product",
            height=35,
            command=self.add_product_action
        )
        add_button.pack(side="left", padx=10, pady=15)

        update_button = ctk.CTkButton(
            form_frame,
            text="Update Product",
            height=35,
            command=self.update_product_action
        )
        update_button.pack(side="left", padx=10, pady=15)

        delete_button = ctk.CTkButton(
            form_frame,
            text="Delete Product",
            height=35,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.delete_product_action
        )
        delete_button.pack(side="left", padx=10, pady=15)

        table_frame = ctk.CTkFrame(self.content, fg_color="white")
        table_frame.pack(fill="both", expand=True, padx=35, pady=15)

        columns = (
            "ID",
            "Name",
            "Category",
            "Price",
            "Quantity",
            "Reorder Level"
        )

        self.product_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        for column in columns:
            self.product_table.heading(column, text=column)
            self.product_table.column(column, width=120, anchor="center")

        self.product_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.load_products()

        self.product_table.bind(
            "<Double-1>",
            self.select_product
        )

        self.search_entry = ctk.CTkEntry(
            self.content,
            placeholder_text="Search products by name...",
            width=300
        )
        self.search_entry.pack(anchor="w", padx=35, pady=10)

        search_button = ctk.CTkButton(
            self.content,
            text="Search",
            command=self.search_product_action
        )
        search_button.pack(anchor="w", padx=35, pady=5)

    def load_products(self):

        for item in self.product_table.get_children():
            self.product_table.delete(item)

        products = get_all_products()

        for product in products:
            self.product_table.insert(
                "",
                "end",
                values=product
            )

    def show_stock(self):

        heading = ctk.CTkLabel(
            self.content,
            text="Stock Management",
            font=("Arial", 30, "bold"),
            text_color="#172033"
        )
        heading.pack(anchor="w", padx=35, pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self.content,
            text="Manage stock movements and monitor inventory",
            font=("Arial", 14),
            text_color="#667085"
        )
        subtitle.pack(anchor="w", padx=35, pady=(0, 15))

        form_frame = ctk.CTkFrame(
            self.content,
            fg_color="white"
        )
        form_frame.pack(fill="x", padx=35, pady=10)

        self.stock_product_id = ctk.CTkEntry(
            form_frame,
            placeholder_text="Product ID",
            width=150
        )
        self.stock_product_id.pack(side="left", padx=10, pady=15)

        self.stock_quantity = ctk.CTkEntry(
            form_frame,
            placeholder_text="Quantity",
            width=150
        )
        self.stock_quantity.pack(side="left", padx=10, pady=15)

        self.stock_note = ctk.CTkEntry(
            form_frame,
            placeholder_text="Note (optional)",
            width=200
        )
        self.stock_note.pack(side="left", padx=10, pady=15)

        stock_in_button = ctk.CTkButton(
            form_frame,
            text="Stock In",
            command=self.stock_in_action
        )
        stock_in_button.pack(side="left", padx=10, pady=15)

        stock_out_button = ctk.CTkButton(
            form_frame,
            text="Stock Out",
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.stock_out_action
        )
        stock_out_button.pack(side="left", padx=10, pady=15)

        low_stock_button = ctk.CTkButton(
            form_frame,
            text="Low Stock Items",
            fg_color="#D97706",
            hover_color="#B45309",
            command=self.show_low_stock
        )
        low_stock_button.pack(side="left", padx=10, pady=15)

        history_heading = ctk.CTkLabel(
            self.content,
            text="Stock Transaction History",
            font=("Arial", 20, "bold")
        )
        history_heading.pack(anchor="w", padx=35, pady=(15, 5))

        columns = (
            "ID",
            "Product",
            "Type",
            "Quantity",
            "Note",
            "Date"
        )

        self.stock_table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings",
            height=10
        )

        for column in columns:
            self.stock_table.heading(column, text=column)
            self.stock_table.column(
                column,
                width=130,
                anchor="center"
            )

        self.stock_table.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        self.load_stock_data()


    def show_reports(self):

        heading = ctk.CTkLabel(
            self.content,
            text="Reports",
            font=("Arial", 30, "bold"),
            text_color="#172033"
        )
        heading.pack(anchor="w", padx=35, pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self.content,
            text="View inventory and business reports",
            font=("Arial", 14),
            text_color="#667085"
        )
        subtitle.pack(anchor="w", padx=35, pady=(0, 20))

        button_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        button_frame.pack(anchor="w", padx=35, pady=10)

        ctk.CTkButton(
            button_frame,
            text="Product Report",
            command=self.show_product_report
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Stock Report",
            command=self.show_stock_report
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Transaction Report",
            command=self.show_transaction_report
        ).pack(side="left", padx=5)

        self.report_table = ttk.Treeview(
            self.content,
            show="headings",
            height=18
        )

        self.report_table.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=15
        )

    def show_product_report(self):

        self.report_table.delete(
            *self.report_table.get_children()
        )

        columns = (
            "ID", "Name", "Category",
            "Price", "Quantity", "Total Value"
        )

        self.report_table["columns"] = columns

        for column in columns:
            self.report_table.heading(column, text=column)
            self.report_table.column(
                column, width=130, anchor="center"
            )

        report = get_product_report()

        for item in report:
            self.report_table.insert("", "end", values=item)

    def show_stock_report(self):

        self.report_table.delete(
            *self.report_table.get_children()
        )

        columns = (
            "ID", "Name", "Quantity",
            "Reorder Level", "Status"
        )

        self.report_table["columns"] = columns

        for column in columns:
            self.report_table.heading(column, text=column)
            self.report_table.column(
                column, width=150, anchor="center"
            )

        report = get_stock_report()

        for item in report:
            self.report_table.insert("", "end", values=item)

    def show_transaction_report(self):

        self.report_table.delete(
            *self.report_table.get_children()
        )

        columns = (
            "ID", "Product", "Type",
            "Quantity", "Note", "Date"
        )

        self.report_table["columns"] = columns

        for column in columns:
            self.report_table.heading(column, text=column)
            self.report_table.column(
                column, width=150, anchor="center"
            )

        report = get_transaction_report()

        for item in report:
            self.report_table.insert("", "end", values=item)

    def show_dashboard(self):
        heading = ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=("Arial", 30, "bold"),
            text_color="#172033"
        )
        heading.pack(anchor="w", padx=35, pady=(35, 5))

        subtitle = ctk.CTkLabel(
            self.content,
            text="Inventory overview and business summary",
            font=("Arial", 14),
            text_color="#667085"
        )
        subtitle.pack(anchor="w", padx=35, pady=(0, 25))

        summary = get_dashboard_summary()

        cards_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        cards_frame.pack(fill="x", padx=25, pady=10)

        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        cards = [
            ("Total Products", summary["total_products"]),
            ("Total Stock", summary["total_stock"]),
            ("Inventory Value", f"Rs. {summary['inventory_value']:,.2f}"),
            ("Low Stock Items", summary["low_stock_count"])
        ]

        for index, (title, value) in enumerate(cards):
            card = ctk.CTkFrame(
                cards_frame,
                corner_radius=12,
                fg_color="white"
            )
            card.grid(row=0, column=index, padx=8, pady=8, sticky="nsew")

            label = ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 13),
                text_color="#667085"
            )
            label.pack(anchor="w", padx=15, pady=(20, 10))

            number = ctk.CTkLabel(
                card,
                text=str(value),
                font=("Arial", 22, "bold"),
                text_color="#172033"
            )
            number.pack(anchor="w", padx=15, pady=(0, 20))

        welcome = ctk.CTkLabel(
            self.content,
            text="Welcome to your Inventory Management System!",
            font=("Arial", 18, "bold"),
            text_color="#172033"
        )
        welcome.pack(anchor="w", padx=35, pady=(35, 10))

        description = ctk.CTkLabel(
            self.content,
            text="Use the navigation menu to manage products, stock and reports.",
            font=("Arial", 14),
            text_color="#667085"
        )
        description.pack(anchor="w", padx=35)

    def stock_in_action(self):

        product_id = self.stock_product_id.get().strip()
        quantity = self.stock_quantity.get().strip()
        note = self.stock_note.get().strip() or "Stock received"

        try:
            product_id = int(product_id)
            quantity = int(quantity)

            success, message = stock_in(
                product_id,
                quantity,
                note
            )

            if success:
                messagebox.showinfo("Success", message)
                self.load_stock_data()
                self.stock_quantity.delete(0, "end")
                self.stock_note.delete(0, "end")
            else:
                messagebox.showerror("Error", message)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter valid Product ID and Quantity."
            )

    def stock_out_action(self):

        product_id = self.stock_product_id.get().strip()
        quantity = self.stock_quantity.get().strip()
        note = self.stock_note.get().strip() or "Stock issued"

        try:
            product_id = int(product_id)
            quantity = int(quantity)

            success, message = stock_out(
                product_id,
                quantity,
                note
            )

            if success:
                messagebox.showinfo("Success", message)
                self.load_stock_data()
                self.stock_quantity.delete(0, "end")
                self.stock_note.delete(0, "end")
            else:
                messagebox.showerror("Error", message)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter valid Product ID and Quantity."
            )

    def load_stock_data(self):

        for item in self.stock_table.get_children():
            self.stock_table.delete(item)

        transactions = get_stock_transactions()

        for transaction in transactions:
            self.stock_table.insert(
                "",
                "end",
                values=transaction
            )

    def show_low_stock(self):

        low_stock = get_low_stock_products()

        if not low_stock:
            messagebox.showinfo(
                "Low Stock",
                "There are no low-stock products."
            )
            return

        message = "LOW STOCK PRODUCTS\n\n"

        for product in low_stock:
            message += (
                f"Product: {product[1]}\n"
                f"Current Quantity: {product[3]}\n"
                f"Reorder Level: {product[4]}\n\n"
            )

        messagebox.showwarning(
            "Low Stock Alert",
            message
        )

    def add_product_action(self):

        name = self.product_name.get().strip()
        price = self.product_price.get().strip()
        quantity = self.product_quantity.get().strip()

        if not name or not price or not quantity:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields."
            )
            return

        try:
            price = float(price)
            quantity = int(quantity)

            if price < 0 or quantity < 0:
                raise ValueError

            add_product(name, None, price, quantity)

            messagebox.showinfo(
                "Success",
                "Product added successfully!"
            )

            self.product_name.delete(0, "end")
            self.product_price.delete(0, "end")
            self.product_quantity.delete(0, "end")

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid price and whole-number quantity."
            )

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def search_product_action(self):

        keyword = self.search_entry.get().strip()

        for item in self.product_table.get_children():
            self.product_table.delete(item)

        products = search_products(keyword)

        for product in products:
            self.product_table.insert(
                "",
                "end",
                values=product
            )

    def select_product(self, event):

        selected_item = self.product_table.selection()

        if not selected_item:
            return

        product = self.product_table.item(
            selected_item[0],
            "values"
        )

        self.selected_product_id = product[0]

        self.product_name.delete(0, "end")
        self.product_name.insert(0, product[1])

        self.product_price.delete(0, "end")
        self.product_price.insert(0, product[3])

        self.product_quantity.delete(0, "end")
        self.product_quantity.insert(0, product[4])

    def update_product_action(self):

        if not hasattr(self, "selected_product_id"):
            messagebox.showwarning(
                "No Product Selected",
                "Please double-click a product first."
            )
            return

        name = self.product_name.get().strip()
        price = self.product_price.get().strip()

        if not name or not price:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the product name and price."
            )
            return

        try:
            price = float(price)

            if price < 0:
                raise ValueError

            updated = update_product(
                self.selected_product_id,
                name,
                None,
                price,
                5
            )

            if updated:
                messagebox.showinfo(
                    "Success",
                    "Product updated successfully!"
                )

                self.load_products()
                del self.selected_product_id

            else:
                messagebox.showerror(
                    "Error",
                    "Product not found."
                )

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid price."
            )

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def delete_product_action(self):

        if not hasattr(self, "selected_product_id"):
            messagebox.showwarning(
                "No Product Selected",
                "Please double-click a product first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this product?"
        )

        if confirm:
            deleted = delete_product(self.selected_product_id)

            if deleted:
                messagebox.showinfo(
                    "Success",
                    "Product deleted successfully!"
                )

                self.load_products()
                del self.selected_product_id

                self.product_name.delete(0, "end")
                self.product_price.delete(0, "end")
                self.product_quantity.delete(0, "end")

            else:
                messagebox.showerror(
                    "Error",
                    "Product could not be deleted."
                )