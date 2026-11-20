import os
import json
import csv

from models.inventory import Inventory
from models.physical_product import PhysicalProduct
from models.digital_product import DigitalProduct
from shipping.can_be_shipped import CanBeShipped
from models.supplier import Supplier
from models.product import Product
from orders.order import Order

from factories.product_factory import ProductFactory
from discounts.no_discount import NoDiscount
from discounts.percentage_discount import PercentageDiscount
from discounts.bulk_discount import BulkDiscount
from discounts.student_discount import StudentDiscount


FILE_NAME = os.path.join(os.path.dirname(__file__), "data", "inventory.json")
CSV_FILE = os.path.join(os.path.dirname(__file__), "data", "products.csv")


def get_positive_float(prompt: str) -> float:
    """Keep asking until the user enters a positiv number."""

    while True:
        try:
            value = float(input(prompt))

            if value <= 0:
                print("Please enter a number greater than zero.")
                continue

            return value
        
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")

def get_non_negative_int(prompt: str) -> int:
    """Keep asking until the user enters a non-negative integer."""

    while True:
        try:
            value = int(input(prompt))

            if value < 0:
                print("Please enter a non-negative number.")
                continue

            return value
        
        except ValueError:
            print("Please enter a valid number.")

def create_supplier() -> Supplier:
    print("\n========== Create Supplier ==========")

    supplier_id = input("Enter Supplier ID: ").strip()
    name = input("Enter Supplier Name: ").strip()
    email = input("Enter Contact Email: ").strip()

    if not supplier_id or not name or not email:
        raise ValueError("Supplier details cannot be empty.")

    return Supplier(supplier_id, name, email)

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from CSV using ProductFactory."""

    loaded = 0

    try:
        file = open(path, newline="", encoding="utf-8")

    except FileNotFoundError:
        print(f"Products file not found: {path}")

    else:
        with file:
            reader = csv. reader(file)

            # Skip the header row
            next(reader, None)

            for row_number, row in enumerate(reader, start=2):
                try:
                    if len(row) != 5:
                        raise ValueError("Incorrect number of columns.")

                    product_type, product_id, name, price_text, stock_text = row

                    price = float(price_text)
                    stock_quantity = int(stock_text)

                    product = ProductFactory.create(
                        product_type=product_type.strip().lower(),
                        product_id=product_id.strip(),
                        name=name.strip(),
                        price=price,
                        stock_quantity=stock_quantity,
                        supplier=supplier,
                        weight=1.0 if product_type.strip().lower() == "physical" else None,
                        download_size=10.0 if product_type.strip().lower() == "digital" else None
                    )

                    inventory.add_product(product)
                    loaded += 1

                except ValueError as error:
                    print(f"Row {row_number} skipped: {error}")

        print(f"{loaded} products loaded.")

    finally:
        print("Load attempt finished.")

def save_inventory(inventory: Inventory) -> None:
    """Save products to the existing JSON inventory file."""

    data = []

    for product in inventory.get_products():
        product_data = {
            "id": product.product_id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "supplier": {
                "supplier_id": product.supplier.supplier_id,
                "name": product.supplier.name,
                "contact_email": product.supplier.contact_email
            }
        }

        if isinstance(product, PhysicalProduct):
            product_data["type"] = "physical"
            product_data["weight"] = product.weight

        elif isinstance(product, DigitalProduct):
            product_data["type"] = "digital"
            product_data["download_size"] = product.download_size

        data.append(product_data)

    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Inventory saved successfully.")

    except OSError as error:
        print(f"Unable to save inventory: {error}")


def load_inventory() -> Inventory:
    """Load the existing JSON inventory, if available."""

    inventory = Inventory()

    if not os.path.exists(FILE_NAME):
        return inventory

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        suppliers = {}

        for item in data:
            supplier_data = item["supplier"]
            supplier_id = supplier_data["supplier_id"]

            if supplier_id not in suppliers:
                suppliers[supplier_id] = Supplier(
                    supplier_id,
                    supplier_data["name"],
                    supplier_data["contact_email"]
                )

            supplier = suppliers[supplier_id]
            product_type = item["type"]

            if product_type == "physical":
                product = ProductFactory.create(
                    "physical",
                    item["id"], 
                    item["name"], 
                    float(item["price"]), 
                    int(item["stock"]),
                    supplier, 
                    weight=float(item["weight"]),
                )

            elif product_type == "digital":
                product = ProductFactory.create(
                    "digital",
                    item["id"], 
                    item["name"], 
                    float(item["price"]), 
                    int(item["stock"]), 
                    supplier,
                    download_size=float(item["download_size"]),
                )

            else:
                raise ValueError(f"Unknown product type: {product_type}")

            inventory.add_product(product)

    except FileNotFoundError:
        print("Inventory file not found. Starting with an empty inventory.")

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Unable to load inventory data: {error}")
        return Inventory()

    return inventory

def add_product(inventory: Inventory) -> None:
    print("\n========== Add Product ==========")

    print("1. Physical Product")
    print("2. Digital Product")

    choice = input("Choose product type: ").strip()

    if choice == "1":
        product_type = "physical"
    elif choice == "2":
        product_type = "digital"
    else:
        print("Invalid product type.")
        return

    product_id = input("Enter Product ID: ").strip()
    name = input("Enter Product Name: ").strip()

    if not product_id or not name:
        print("Product ID and name cannot be empty.")
        return

    price = get_positive_float("Enter Price: $")
    stock = get_non_negative_int("Enter Stock Quantity: ")

    try:
        supplier = create_supplier()

        if product_type == "physical":
            weight = get_positive_float("Enter Weight (kg): ")

            product = ProductFactory.create(
                product_type,
                product_id,
                name,
                price,
                stock,
                supplier,
                weight=weight
            )

        else:
            download_size = get_positive_float("Enter Download Size (MB): ")

            product = ProductFactory.create(
                product_type,
                product_id,
                name,
                price,
                stock,
                supplier,
                download_size=download_size
            )

        inventory.add_product(product)
        print("Product added successfully.")

    except ValueError as error:
        print(f"Unable to add product: {error}")

def update_stock(inventory: Inventory) -> None:
    print("\n========== Update Stock ==========")

    product_id = input("Enter Product ID: ").strip()
    
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    quantity = get_non_negative_int("Enter new stock quantity: ")

    try:
        product.update_stock(quantity)
        print("Stock updated successfully.")

    except ValueError as error:
        print(error)

def search_product(inventory: Inventory) -> None:
    print("\n========== Search Product ==========")

    product_id = input("Enter Product ID: ").strip()
    
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    product.display_information()
    print(product.get_fulfilment_info())

    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")

def remove_product(inventory: Inventory) -> None:
    product_id = input("Enter Product ID to remove: ").strip()
    
    product = inventory.remove_product(product_id)

    if product is None:
        print("Product not found.")
    else:
        print("Product removed successfully.")

def create_order(inventory: Inventory) -> None:
    print("\n========== Create Order ==========")

    order_id = input("Enter Order ID: ").strip()
    
    if not order_id:
        print("Order ID cannot be empty.")
        return

    order = Order(order_id)

    while True:
        product_id = input(
            "Enter Product ID (or 'done' to finish): "
        ).strip()

        if product_id.lower() == "done":
            break

        product = inventory.find_product(product_id)

        if product is None:
            print("Product not found.")
            continue

        try:
            quantity = int(input("Enter Quantity: "))
            order.add_order_line(product, quantity)

        except ValueError as error:
            print(f"Invalid quantity: {error}")

    print("\nChoose Discount:")
    print("1. No Discount")
    print("2. 10% Percentage Discount")
    print("3. Bulk Discount ($20 off orders of $200 or more)")
    print("4. Student Discount (5%)")

    discount_choice = input("Enter choice: ").strip()

    try:
        if discount_choice == "1":
            order.set_discount(NoDiscount())

        elif discount_choice == "2":
            order.set_discount(PercentageDiscount(10))

        elif discount_choice == "3":
            order.set_discount(BulkDiscount(200, 20))

        elif discount_choice == "4":
            order.set_discount(StudentDiscount())

        else:
            print("Invalid choice. No discount will be applied.")
            order.set_discount(NoDiscount())

        order.display_order()

    except ValueError as error:
        print(f"Unable to apply discount: {error}")
    

def main() -> None:
    inventory = load_inventory()

    print("\n========== Inventory Management System ==========")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("7. Remove Product")
    print("8. Create Order")
    print("9. Load Products from CSV")

    while True:
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            add_product(inventory)

        elif choice == "3":
            update_stock(inventory)

        elif choice == "4":
            search_product(inventory)

        elif choice == "5":
            save_inventory(inventory)

        elif choice == "6":
            save_inventory(inventory)
            print("Exiting Inventory Management System.")
            break

        elif choice == "7":
            remove_product(inventory)

        elif choice == "8":
            create_order(inventory)

        elif choice == "9":
            supplier = create_supplier()
            load_products(CSV_FILE, inventory, supplier)

        else:
            print("Invalid option. Please select 1-8.")


if __name__ == "__main__":
    main()
