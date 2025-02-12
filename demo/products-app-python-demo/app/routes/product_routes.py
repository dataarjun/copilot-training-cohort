from flask import Blueprint, jsonify, request
from app.services.product_service import ProductService
from app import db  

product_routes = Blueprint('product_routes', __name__)
product_service = ProductService(db)

@product_routes.route('/products', methods=['GET'])
def get_all_products():
    products = product_service.get_all_products()
    return jsonify(products)

@product_routes.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = product_service.get_product(product_id)
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404

@product_routes.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = product_service.create_product(data)
    return jsonify(product), 201

@product_routes.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = product_service.update_product(product_id, data)
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404

@product_routes.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = product_service.delete_product(product_id)
    if result:
        return jsonify({'message': 'Product deleted'})
    else:
        return jsonify({'error': 'Product not found'}), 404