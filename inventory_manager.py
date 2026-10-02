import os
import json

def load_inventory():
    if os.path.exists("inventory.json"):
        print("inventory.json found.")
        print("Inventory loaded successfully.")
        with open("inventory.json", "r") as file:
            return json.load(file)
    else:
        print("inventory.json not found. Starting with default inventory.")
        return [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
        ]
    
inventory = load_inventory()

def save_inventory():
    print("Saving inventory...")
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)
    print("Inventory saved successfully to inventory.json.")

def display_all():
    print("\nCurrent Inventory")
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")

def add_product():
    print("\nAdd New Product")
    prod_id = input("Product ID: ")
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))
    
    inventory.append({"id": prod_id, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")

def update_stock():
    print("\nUpdate Stock")
    prod_id = input("Enter Product ID: ")
    found = False
    for item in inventory:
        if item["id"] == prod_id:
            found = True
            print(f"Product Found:\nName: {item['name']}\nCurrent Stock: {item['stock']}")
            new_stock = int(input("New Stock Quantity: "))
            item["stock"] = new_stock
            print("Stock updated successfully!")
            break
    if not found:
        print("Product not found.")

def search_product():
    print("\nSearch Product")
    prod_id = input("Enter Product ID: ")
    found = False
    for item in inventory:
        if item["id"] == prod_id:
            found = True
            print("\nProduct Found")
            print("-" * 40)
            print(f"ID: {item['id']}\nName: {item['name']}\nPrice: ${item['price']:.2f}\nStock: {item['stock']}")
            print("-" * 40)
            break
    if not found:
        print("\nProduct not found.")

def main():
    while True:
        print("\nINVENTORY MANAGEMENT SYSTEM")
        print("MENU")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        
        option = input("Enter option: ")
        
        if option == "1":
            display_all()
        elif option == "2":
            add_product()
        elif option == "3":
            update_stock()
        elif option == "4":
            search_product()
        elif option == "5":
            save_inventory()
        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory()
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()