# products-app-python

This is a Python application that supports CRUD operations on a product entity and exposes them as REST endpoints.

## Project Structure

```
products-app-python
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   └── product.py
│   ├── routes
│   │   └── product_routes.py
│   ├── services
│   │   └── product_service.py
│   └── database
│       └── db.py
├── tests
│   └── test_product.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/products-app-python.git
```

2. Navigate to the project directory:

```
cd products-app-python
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Start the application:

```
$env:PYTHONPATH = "."
$env:PYTHONPATH = "."
python app/main.py
```

2. The application will be running at `http://localhost:5000`.

## API Endpoints

The following REST endpoints are available for the product entity:

- `GET /products`: Get all products
- `GET /products/{id}`: Get a specific product by ID
- `POST /products`: Create a new product
- `PUT /products/{id}`: Update an existing product
- `DELETE /products/{id}`: Delete a product

## Testing

To run the unit tests for the product entity, execute the following command:

```
python -m unittest discover tests
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.