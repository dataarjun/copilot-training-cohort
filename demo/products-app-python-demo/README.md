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

## Testing with Postman

To test the API endpoints using Postman, follow these optional steps:

1. Download and install Postman from [here](https://www.postman.com/downloads/) or use the [Postman web version](https://www.postman.com/).

2. Open Postman and import the `Copilot.postman_collection.json` file:

    - Click on the `Import` button in the top left corner.
    - Select the `Copilot.postman_collection.json` file from your file system.

3. Once imported, you will see a collection named `Copilot` in your Postman workspace. You can now use the predefined requests to test the API endpoints.

Alternatively, you can use the Postman web version and import the collection directly from the URL if it's hosted online.

## Testing

To run the unit tests for the product entity, execute the following command:

```
python -m unittest discover tests
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.