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


def generate_report(total_units, failed_attempts):
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


# Main program
inventory = 0
failed_entries = 0

while True:
    stock = get_valid_input()

    if stock == "quit":
        break

    if stock is None:
        failed_entries += 1
        continue

    inventory = process_delivery(inventory, stock)
    tax = calculate_tax(stock)

generate_report(inventory, failed_entries)