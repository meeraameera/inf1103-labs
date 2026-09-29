def get_valid_input():
    stock = input("Enter stock quantity or 'Quit' to stop: ")

    if stock.lower() == "quit":
        return "quit"

    if not stock.isdigit():
        print("ERROR: Invalid input. Please enter a valid whole number.")
        return None

    stock = int(stock)

    if stock < 0:
        print("ERROR: Negative stock values are not allowed.")
        return None

    return stock


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def load_inventory():
    try:
        file = open("inventory.txt", "r")
        lines = file.readlines()
        file.close()

        total = int(lines[0])
        history = []

        for line in lines[1:]:
            history.append(int(line))

        return total, history

    except FileNotFoundError:
        print("ERROR: Inventory file not found. Starting with empty inventory.")
        return 0, []


def save_inventory(total, history):
    file = open("inventory.txt", "w")
    file.write(str(total) + "\n")

    for amount in history:
        file.write(str(amount) + "\n")

    file.close()

    print("Inventory successfully saved to inventory.txt")


def generate_report(total_units, failed_attempts):
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


# Main program
inventory, history = load_inventory()
failed_entries = 0

print("Current Inventory:", inventory)
print("Transaction History:", history)

while True:
    stock = get_valid_input()

    if stock == "quit":
        break

    if stock is None:
        failed_entries += 1
        continue

    inventory = process_delivery(inventory, stock)
    tax = calculate_tax(stock)

    history.append(stock)

save_inventory(inventory, history)
generate_report(inventory, failed_entries)

