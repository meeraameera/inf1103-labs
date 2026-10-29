import os
import json
from random import choice

from product import Product
from inventory import Inventory


def load_inventory():
    inventory = Inventory()

    if os.path.exists("inventory.json"):
        print("inventory.json found.")

        with open("inventory.json", "r") as file:
            products = json.load(file)

        for item in products:
            product = Product(
                item["id"], 
                item["name"], 
                item["price"], 
                item["stock"]
            )
            inventory.add_product(product)

        print("Inventory loaded successfully.")

    else:
        print("inventory.json not found. Starting with default inventory.")

        default_products = [
            Product("P001", "Laptop", 1200.00, 15),
            Product("P002", "Mouse", 25.50, 40),
            Product("P003", "Keyboard", 45.00, 25)
        ]

        for product in default_products:
            inventory.add_product(product)

    return inventory

def save_inventory(inventory):
    print("Saving inventory...")

    products = []

    for product in inventory.get_products():
        products.append({
            "id": product.product_id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        })

    with open("inventory.json", "w") as file:
        json.dump(products, file, indent=4)

    print("Inventory saved successfully to inventory.json.")

def display_all(inventory):
    print("\nCurrent Inventory")
    inventory.display_all()

def add_product(inventory):
    print("\nAdd New Product")

    prod_id = input("Product ID: ")
    name = input("Product Name: ")

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        if price < 0 or stock < 0:
            print("Price and stock must be non-negative.")
            return

    except ValueError:
        print("Invalid input for price or stock. Please enter numeric values.")
        return

    product = Product(prod_id, name, price, stock)
    inventory.add_product(product)

    print("Product added successfully!")

def update_stock(inventory):
    print("\nUpdate Stock")

    prod_id = input("Enter Product ID: ")
    product = inventory.search_product(prod_id)

    if product is None:
        print("Product not found.")
        return

    print(
        f"Product Found:\n"
        f"Name: {product.name}\n"
        f"Current Stock: {product.stock}"
    )

    try:
        new_stock = int(input("New Stock Quantity: "))

        if new_stock < 0:
            print("Stock quantity must be non-negative.")
            return

    except ValueError:
        print("Invalid input for stock. Please enter a numeric value.")
        return

    product.update_stock(new_stock)
    print("Stock updated successfully!")

def search_product(inventory):
    print("\nSearch Product")

    prod_id = input("Enter Product ID: ")
    product = inventory.search_product(prod_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 40)
    product.display_information()
    print("-" * 40)

def main():
    inventory = load_inventory()

    while True:
        print("\nINVENTORY MANAGEMENT SYSTEM")
        print("MENU")
        print("1. Display All Products")
        print("2. Add New Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save and Exit")
        print("6. Exit")

        option = input("Enter option: ")

        if option == "1":
            display_all(inventory)

        elif option == "2":
            add_product(inventory)

        elif option == "3":
            update_stock(inventory)

        elif option == "4":
            search_product(inventory)

        elif option == "5":
            save_inventory(inventory)

        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()