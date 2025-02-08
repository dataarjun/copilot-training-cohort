from app.models.product import Product

class ProductService:
    def __init__(self, db):
        self.db = db

    def create_product(self, product_data):
        product = Product(name=product_data['name'], description=product_data['description'], price=product_data['price'], quantity=product_data['quantity'])
        self.db.session.add(product)
        self.db.session.commit()
        return product.to_dict()

    def get_product(self, product_id):
        product = Product.query.get(product_id)
        return product.to_dict() if product else None

    def update_product(self, product_id, product_data):
        product = Product.query.get(product_id)
        if product:
            if 'name' in product_data:
                product.name = product_data['name']
            if 'description' in product_data:
                product.description = product_data['description']
            if 'price' in product_data:
                product.price = product_data['price']
            if 'quantity' in product_data:
                product.quantity = product_data['quantity']
            self.db.session.commit()
        return product.to_dict() if product else None
    
    def delete_product(self, product_id):
        product = Product.query.get(product_id)
        if product:
            self.db.session.delete(product)
            self.db.session.commit()
        return product.to_dict() if product else None

    def get_all_products(self):
        return [product.to_dict() for product in Product.query.all()]