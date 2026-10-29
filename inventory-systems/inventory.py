from product import Product


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to the inventory.")

        self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.product_id == product_id:
                return product
            
        return None

    def display_all(self):
        print("\nCurrent Inventory")

        if not self.__products:
            print("Inventory is empty.")
            return

        for product in self.__products:
            product.display_information()

    def get_products(self):
        return self.__products.copy()