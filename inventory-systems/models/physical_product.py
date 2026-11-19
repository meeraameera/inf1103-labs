from .product import Product
from .supplier import Supplier
from shipping.can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(
            self, 
            product_id: str, 
            name: str, 
            price: float, 
            stock: int, 
            weight: float, 
            supplier: Supplier
    ) -> None:
        
        super().__init__(product_id, name, price, stock, supplier)

        if weight <= 0:
            raise ValueError("Product wieght must be greater than zero.")
        
        self.__weight: float = weight

    @property
    def weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.__weight * 5.0
    