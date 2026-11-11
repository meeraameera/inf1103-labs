from inventory import Inventory
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order
from supplier import Supplier

supplier = Supplier(
    "SUP001",
    "Tech Supplies Pte Ltd",
    "tech@example.com"
)

laptop = PhysicalProduct(
    "P001",
    "Laptop",
    1200.00,
    15,
    2.5,
    supplier
)

ebook = DigitalProduct(
    "P001",
    "Python Programming Ebook",
    25.00,
    50,
    15.5,
    supplier
)

# ==========================================
# TEST 1: ASSOCIATION
# ==========================================
print("\n========== TEST 1: ASSOCIATION ==========")

print ("Supplier through Laptop:")
laptop.supplier.display_information()

print("\nSupplier through Ebook:")
ebook.supplier.display_information()

# Deleting the original supplier variable
del supplier

# Products should still access the Supplier
print("\nAfter deleting original supplier variable:")
print(laptop.supplier.name)
print(ebook.supplier.name)

# ==========================================
# TEST 2: AGGREGATION
# ==========================================
print("\n========== TEST 2: AGGREGATION ==========")

inventory_a = Inventory()
inventory_b = Inventory()

# Product exists before being added to Inventory
keyboard = PhysicalProduct(
    "P002",
    "Keyboard",
    45.00,
    25,
    0.8,
    laptop.supplier
)

print("CReated product:", keyboard.name)

# Add product to Inventory A
inventory_a.add_product(keyboard)

print("\nInventory A:")
inventory_a.display_all()

# Remove product from Inventory A
removed_product = inventory_a.remove_product("P002")

print("\nAfter removing from Inventory A:")
print("Removed product still exists:", removed_product is keyboard)

# Add product to Inventory B
inventory_b.add_product(keyboard)

print("\nInventory B:")
inventory_b.display_all()

# Confirm it is the same object
print("Same Product object:", inventory_b.find_product("P002") is keyboard)

# ==========================================
# TEST 3: COMPOSITION
# ==========================================
print("\n========== TEST 3: COMPOSITION ==========")

order_a = Order("ORD001")
order_b = Order("ORD002")

# Add the same Product to two different Orders
order_a.add_order_line(laptop, 2)
order_b.add_order_line(laptop, 3)

print("\nOrder A:")
order_a.display_order()

print("\nOrder B:")
order_b.display_order()

# Compare the Product objects
print(
    "\nSame Product object:",
    order_a.order_lines[0].product
    is order_b.order_lines[0].product
)

# Compare the OrderLine objects
print(
    "\nSame OrderLine object:",
    order_a.order_lines[0]
    is order_b.order_lines[0]
)

# Remove an OrderLine from Order A
removed_line = order_a.remove_order_line(0)

print(
    "\nProduct still exists after removing OrderLine:",
    removed_line.product is laptop
)

print("Product name:", laptop.name)

# ==========================================
# TEST 4: LISKOV SUBSTITUTION PRINCIPLE
# ==========================================
print("\n========== TEST 4: LISKOV SUBSTITUTION PRINCIPLE ==========")

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())

show_product_details(laptop)
show_product_details(ebook)

# Both subclasses should support update_stock()
laptop.update_stock(10)
ebook.update_stock(30)

print("\nLaptop stock:", laptop.stock)
print("Ebook stock:", ebook.stock)

# ==========================================
# TEST 5: POLYMORPHISM
# ==========================================
print("\n========== TEST 5: POLYMORPHISM ==========")

inventory = Inventory()

inventory.add_product(laptop)
inventory.add_product(ebook)

for product in inventory.products:
    product.display_information()
    print(product.get_fulfilment_info())
    print("---------------------------------------")

print("\nAll relationship tests completed.")
