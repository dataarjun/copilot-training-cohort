import unittest
from unittest.mock import Mock
from app.models.product import Product
from app.services.product_service import ProductService

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock()
        self.product_service = ProductService(db=self.mock_db)
        
    def test_create_product(self):
        # Create Product instance directly
        test_product = Product(
            name="Test Product",
            description="Test Description",
            price=99.99,
            quantity=10
        )
        
        # Configure mock
        self.mock_db.session.add.return_value = None
        self.mock_db.session.commit.return_value = None
        
        result = self.product_service.create_product(test_product)
        self.assertTrue(result)
        self.mock_db.session.add.assert_called_once()
        self.mock_db.session.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()