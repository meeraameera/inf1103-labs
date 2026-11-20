from models.product import Product
from .order_line import OrderLine
from discounts.discount_strategy import DiscountStrategy
from discounts.no_discount import NoDiscount


class Order:
    def __init__(
            self, 
            order_id: str,
            discount: DiscountStrategy | None = None
        ) -> None:

        self .order_id: str = order_id
        self.order_lines: list[OrderLine] = []

        if discount is None:
            self.discount: DiscountStrategy = NoDiscount()
        else:
            self.discount = discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, index: int) -> OrderLine | None:
        if 0 <= index < len(self.order_lines):
            return self.order_lines.pop(index)
        
        return None

    def calculate_total(self) -> float:
        total = sum(
            line.calculate_subtotal()
            for line in self.order_lines
        )

        return self.discount.apply(total)

    def display_order(self) -> None:
        print(f"\n========== Order {self.order_id} ==========")

        if not self.order_lines:
            print("This order has no items.")
            return

        for order_line in self.order_lines:
            order_line.display_information()
        
        print("---------------------------------------")
        print(f"Order Total: ${self.calculate_total():.2f}")
