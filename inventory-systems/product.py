from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    def __init__(
            self, 
            product_id: str, 
            name: str, 
            price: float, 
            stock: int, 
            supplier: Supplier
    ) -> None:
        self.__product_id: str = product_id
        self.__name:str = name
        self.__price: float = price
        self.__stock: int = stock
        self.supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        
        self.__stock += quantity

    def display_information(self) -> None:
        print(
            f"Product ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

        print(f"Supplier: {self.supplier.name}")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass
    