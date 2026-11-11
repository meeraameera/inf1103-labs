from product import Product


class OrderLine:
    def __init__(
            self, 
            product: Product, 
            quantity: int
    ) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_information(self) -> None:
        print(
            f"Product Name: {self.product.name} | "
            f"Quantity: {self.quantity} | "
            f"Subtotal: ${self.calculate_subtotal():.2f}"
        )
    