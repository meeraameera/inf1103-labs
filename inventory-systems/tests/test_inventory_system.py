
import unittest

from models.supplier import Supplier
from models.product import Product
from models.physical_product import PhysicalProduct
from models.digital_product import DigitalProduct
from models.inventory import Inventory
from orders.order import Order

from discounts.no_discount import NoDiscount
from discounts.percentage_discount import PercentageDiscount
from discounts.bulk_discount import BulkDiscount
from discounts.student_discount import StudentDiscount
from factories.product_factory import ProductFactory


class TestInventorySystem(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier(
            "SUP001",
            "Tech Supplies",
            "tech@example.com"
        )

        self.physical = PhysicalProduct(
            "P001",
            "Laptop",
            100.00,
            10,
            2.0,
            self.supplier
        )

        self.digital = DigitalProduct(
            "D001",
            "Ebook",
            50.00,
            20,
            15.0,
            self.supplier
        )

    def test_no_discount(self):
        order = Order("O001", NoDiscount())
        order.add_order_line(self.physical, 2)

        self.assertEqual(order.calculate_total(), 200.00)

    def test_percentage_discount(self):
        order = Order("O002", PercentageDiscount(10))
        order.add_order_line(self.physical, 2)

        self.assertEqual(order.calculate_total(), 180.00)

    def test_bulk_discount(self):
        order = Order("O003", BulkDiscount(200, 20))
        order.add_order_line(self.physical, 2)

        self.assertEqual(order.calculate_total(), 180.00)

    def test_bulk_discount_below_threshold(self):
        order = Order("O004", BulkDiscount(200, 20))
        order.add_order_line(self.physical, 1)

        self.assertEqual(order.calculate_total(), 100.00)

    def test_student_discount(self):
        order = Order("O005", StudentDiscount())
        order.add_order_line(self.physical, 2)

        self.assertEqual(order.calculate_total(), 190.00)

    def test_change_discount(self):
        order = Order("O006", BulkDiscount(200, 20))
        order.add_order_line(self.physical, 2)
        order.add_order_line(self.digital, 1)

        # Original total = $250
        self.assertEqual(order.calculate_total(), 230.00)

        order.set_discount(PercentageDiscount(10))

        self.assertEqual(order.calculate_total(), 225.00)

    def test_factory_physical_product(self):
        product = ProductFactory.create(
            "physical",
            "P002",
            "Desk",
            80.00,
            5,
            self.supplier,
            weight=4.0
        )

        self.assertIsInstance(product, PhysicalProduct)

    def test_factory_digital_product(self):
        product = ProductFactory.create(
            "digital",
            "D002",
            "Software",
            30.00,
            10,
            self.supplier,
            download_size=25.0
        )

        self.assertIsInstance(product, DigitalProduct)

    def test_factory_unknown_type(self):
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "service",
                "S001",
                "Installation",
                30.00,
                5,
                self.supplier
            )

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            PhysicalProduct(
                "P003",
                "Invalid Product",
                0,
                5,
                2.0,
                self.supplier
            )

    def test_negative_stock(self):
        with self.assertRaises(ValueError):
            PhysicalProduct(
                "P004",
                "Invalid Product",
                50.00,
                -1,
                2.0,
                self.supplier
            )

    def test_invalid_order_quantity(self):
        order = Order("O007")

        with self.assertRaises(ValueError):
            order.add_order_line(self.physical, 0)

    def test_inventory_add_and_find(self):
        inventory = Inventory()
        inventory.add_product(self.physical)

        found = inventory.find_product("P001")

        self.assertIs(found, self.physical)

    def test_digital_product_is_product(self):
        self.assertIsInstance(self.digital, Product)


if __name__ == "__main__":
    unittest.main()
