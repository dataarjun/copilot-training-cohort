# In app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'  # Update this with your database URI

    db.init_app(app)

    with app.app_context():
        from app.models.product import Product
        db.create_all()  # This will create the database tables for all your models
        app.logger.info('Database tables created')

    # Register product routes
    from app.routes.product_routes import product_routes
    app.register_blueprint(product_routes)

    return app