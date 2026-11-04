import os
import json

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped


FILE_NAME = "inventory.json"


def load_inventory():
    inventory = Inventory()

    if not os.path.exists(FILE_NAME):
        return inventory

    try:
        with open(FILE_NAME, "r") as file:
            products_data = json.load(file)

        for item in products_data:
            product_type = item.get("type")

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
                    item["download_size"]
                )

            else:
                print(
                    f"Skipping {item.get('id', 'unknown')}: "
                    "missing or invalid product type."
                )
                continue

            inventory.add_product(product)

        print("Inventory loaded successfully.")

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Error loading inventory: {error}")

    return inventory

def save_inventory(inventory):
    products_data = []

    for product in inventory.get_products():
        product_data = {
            "id": product.product_id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
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

def add_product(inventory):
    print("\n========== Add Product ==========")

    product_type = input(
        "Enter product type (physical/digital): "
    ).strip().lower()

    if product_type not in ["physical", "digital"]:
        print("Invalid product type.")
        return

    product_id = input("Enter product ID: ").strip()

    if not product_id:
        print("Product ID cannot be empty.")
        return  

    if inventory.search_product(product_id) is not None:
        print("A product with this ID already exists.")
        return

    name = input("Enter product name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Enter product price: "))
        stock = int(input("Enter product stock: "))

        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
            return

        if product_type == "physical":
            weight = float(input("Enter product weight (kg): "))

            if weight < 0:
                print("Weight cannot be negative.")
                return

            product = PhysicalProduct(
                product_id, name, price, stock, weight
            )

        else:
            download_size = float(
                input("Enter download size (MB): ")
            )

            if download_size < 0:
                print("Download size cannot be negative.")
                return

            product = DigitalProduct(
                product_id, name, price, stock, download_size
            )

        if inventory.add_product(product):
            print("Product added successfully!")

    except ValueError:
        print("Invalid input. Please enter nthe correct data type.")

def update_stock(inventory):
    print("\n========== Update Stock ==========")

    product_id = input("Enter Product ID: ").strip()
    
    product = inventory.search_product(product_id)

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

def search_product(inventory):
    print("\n========== Search Product ==========")

    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    product.display_information()

    print("\nFulfilment Information:")
    print(product.get_fulfilment_info())

    if isinstance(product, CanBeShipped):
        print(
            f"Shipping Cost: "
            f"${product.calculate_shipping_cost():.2f}"
        )

def main():
    inventory = load_inventory()

    while True:
        print("\n========== Inventory Management System ==========")
        print("1. Display All Products")
        print("2. Add New Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

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

        else:
            print("Invalid option. Please select 1-6.")


if __name__ == "__main__":
    main()