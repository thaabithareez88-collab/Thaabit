import customtkinter as ctk
from database import create_tables

class InventoryApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        create_tables()

        self.title("Inventory Management System")
        self.geometry("900x600")

        title = ctk.CTkLabel(
            self,
            text="Inventory Management System",
            font=("Arial", 25, "bold")
        )
        title.pack(pady=30)

        welcome = ctk.CTkLabel(
            self,
            text="Welcome to Inventory Management"
        )
        welcome.pack(pady=10)

        self.mainloop if False else None
