# Product Service Unit Tests

This project contains unit tests for the `ProductService` class, which is responsible for managing products in the application.

## Prerequisites

- Python 3.x
- `unittest` module (comes with Python standard library)
- `unittest.mock` module (comes with Python standard library)

## Test Structure

The tests are located in the `test_product.py` file.

### Test Class: `TestProduct`

This class contains unit tests for the `ProductService` class.

#### `setUp` Method

The `setUp` method initializes the following before each test:
- `self.mock_db`: A mock database object.
- `self.product_service`: An instance of `ProductService` initialized with the mock database.

#### `test_create_product` Method

This method tests the `create_product` method of the `ProductService` class:
1. Creates a `Product` instance with specific attributes.
2. Configures the mock database's `session.add` and `session.commit` methods to return `None`.
3. Calls the `create_product` method with the `Product` instance.
4. Asserts that the result is `True`.
5. Asserts that `session.add` and `session.commit` were called exactly once.

## Running the Tests

To run the tests, execute the following command in the terminal:

```bash
python -m unittest test_product.py