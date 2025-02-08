import unittest
from app.models.product import Product
from app.services.product_service import ProductService

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product_service = ProductService()

    def test_create_product(self):
        product_data = {
            "name": "Test Product",
            "description": "This is a test product",
            "price": 9.99,
            "quantity": 10
        }
        product = self.product_service.create_product(product_data)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "This is a test product")
        self.assertEqual(product.price, 9.99)
        self.assertEqual(product.quantity, 10)

    def test_get_product(self):
        product = self.product_service.get_product(1)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.id, 1)

    def test_update_product(self):
        product_data = {
            "name": "Updated Product",
            "description": "This is an updated product",
            "price": 19.99,
            "quantity": 5
        }
        product = self.product_service.update_product(1, product_data)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, "Updated Product")
        self.assertEqual(product.description, "This is an updated product")
        self.assertEqual(product.price, 19.99)
        self.assertEqual(product.quantity, 5)

    def test_delete_product(self):
        result = self.product_service.delete_product(1)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()