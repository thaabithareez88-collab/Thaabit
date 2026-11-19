
from database import create_tables
from ui import InventoryApp


if __name__ == "__main__":

    create_tables()

    app = InventoryApp()

    app.mainloop()
