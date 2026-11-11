import os
import json

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from supplier import Supplier
from product import Product
from order import Order


FILE_NAME = "inventory.json"


def load_inventory() -> Inventory:
    inventory = Inventory()

    if not os.path.exists(FILE_NAME):
        return inventory

    try:
        with open(FILE_NAME, "r") as file:
            products_data = json.load(file)

        suppliers: dict[str, Supplier] = {}

        for item in products_data:
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
                product = PhysicalProduct(
                    item["id"], 
                    item["name"], 
                    item["price"], 
                    item["stock"], 
                    item["weight"]
                )

            elif product_type == "digital":
                product = DigitalProduct(
                    item["id"], 
                    item["name"], 
                    item["price"], 
                    item["stock"], 
                    item["download_size"],
                    supplier
                )

            else:
                print(f"Unknown product type: {product_type}")
                continue

            inventory.add_product(product)

        print("Inventory loaded successfully.")

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Error loading inventory: {error}")

    return inventory

def save_inventory(inventory: Inventory) -> None:
    products_data = []

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

        products_data.append(product_data)

    with open(FILE_NAME, "w") as file:
        json.dump(products_data, file, indent=4)

    print("Inventory saved successfully.")

def create_supplier() -> Supplier:
    print("\n========== Supplier Details ==========")

    supplier_id = input("Enter supplier ID: ").strip()
    name = input("Enter supplier name: ").strip()
    email = input("Enter supplier email: ").strip()

    return Supplier(supplier_id, name, email)

def add_product(inventory: Inventory) -> None:
    print("\n========== Add Product ==========")

    product_type = input(
        "Enter product type (physical/digital): "
    ).strip().lower()

    if product_type not in ["physical", "digital"]:
        print("Invalid product type.")
        return

    product_id = input("Enter product ID: ").strip()
    name = input("Enter product name: ").strip()

    if not product_id or not name:
        print("Product ID and name cannot be empty.")
        return  

    if inventory.find_product(product_id) is not None:
        print("A product with this ID already exists.")
        return

    try:
        price = float(input("Enter product price: "))
        stock = int(input("Enter product stock: "))

        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
            return

        supplier = create_supplier()

        if product_type == "physical":
            weight = float(input("Enter product weight (kg): "))

            if weight < 0:
                print("Weight cannot be negative.")
                return

            product = PhysicalProduct(
                product_id, 
                name, 
                price, 
                stock, 
                weight,
                supplier
            )

        else:
            download_size = float(
                input("Enter download size (MB): ")
            )

            if download_size < 0:
                print("Download size cannot be negative.")
                return

            product = DigitalProduct(
                product_id, 
                name, 
                price, 
                stock, 
                download_size,
                supplier
            )

        inventory.add_product(product)
        print("Product added successfully!")

    except ValueError as error:
        print(f"Invalid input: {error}")

def update_stock(inventory: Inventory) -> None:
    print("\n========== Update Stock ==========")

    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    try:
        quantity = int(input("Enter new stock quantity: "))

        if quantity < 0:
            print("Stock cannot benegative.")
            return

        product.update_stock(quantity)

        print("Stock updated successfully.")

    except ValueError:
        print("Please enter a valid whole number.")

def search_product(inventory: Inventory) -> None:
    print("\n========== Search Product ==========")

    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    product.display_information()

    print("\nFulfilment Information:")
    print(product.get_fulfilment_info())

    if isinstance(product, CanBeShipped):
        print(
            f"Shipping Cost: "
            f"${product.calculate_shipping_cost():.2f}"
        )

def remove_product(inventory: Inventory) -> None:
    print("\n========== Remove Product ==========")

    product_id = input("Enter Product ID: ").strip()
    product = inventory.remove_product(product_id)

    if product is None:
        print("Product not found.")
    else:
        print(f"{product.name} removed from inventory.")

def create_order(inventory: Inventory) -> None:
    print("\n========== Create Order ==========")

    order_id = input("Enter order ID: ").strip()

    if not order_id:
        print("Order ID cannot be empty")
        return

    order = Order(order_id)

    while True:
        product_id = input("Enter a product ID (or 'done' to finish): ").strip()

        if product_id.lower == "done":
            break

        product = inventory.find_product(product_id)

        if product is None:
            print("Product not found.")
            continue

        try:
            quantity = int(input("Enter quantity: "))
            order.add_order_line(product, quantity)
            print("Product added to order.")

        except ValueError as error:
            print(f"Invalid input: {error}")

    order.display_order()

def main() -> None:
    inventory = load_inventory()

    while True:
        print("\n========== Inventory Management System ==========")
        print("1. Display All Products")
        print("2. Add New Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("7. Remove Product")
        print("8. Create Order")

        choice = input("Enter your choice (1-8): ").strip()

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

        else:
            print("Invalid option. Please select 1-8.")


if __name__ == "__main__":
    main()
