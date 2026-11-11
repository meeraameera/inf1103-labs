from product import Product


class Inventory:
    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        if self.find_product(product.product_id) is not None:
            raise TypeError("Product ID already exists in the inventory.")
        
        self.products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)

        if product is not None:
            self.products.remove(product)
            return product

        return None

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.product_id == product_id:
                return product
            
        return None

    def display_all(self) -> None:
        print("\n========== Current Inventory ==========")

        if not self.products:
            print("Inventory is empty.")
            return

        for product in self.products:
            product.display_information()
            print("---------------------------------------")

    def get_products(self) -> list[Product]:
        return self.products.copy()
    