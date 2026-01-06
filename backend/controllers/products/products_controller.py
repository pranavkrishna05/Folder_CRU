from flask import Blueprint, request, jsonify, g
from backend.repositories.products.product_repository import ProductRepository
from backend.repositories.products.category_repository import CategoryRepository
from backend.services.products.product_service import ProductService

products_bp = Blueprint('products', __name__)

@products_bp.route('/add', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category_id = data.get('category_id')

    if not name or not description or not price or not category_id:
        return jsonify({"error": "Name, description, price, and category ID are required"}), 400

    product_repository = ProductRepository(g.db)
    category_repository = CategoryRepository(g.db)
    product_service = ProductService(product_repository, category_repository)

    try:
        product_id = product_service.add_product(name, description, price, category_id)
        return jsonify({"product_id": product_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@products_bp.route('/update/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category_id = data.get('category_id')

    product_repository = ProductRepository(g.db)
    category_repository = CategoryRepository(g.db)
    product_service = ProductService(product_repository, category_repository)
    product_service.update_product(product_id, name, description, price, category_id)

    return jsonify({"message": "Product updated successfully"}), 200

@products_bp.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product():
    product_repository = ProductRepository(g.db)
    category_repository = CategoryRepository(g.db)
    product_service = ProductService(product_repository, category_repository)

    product_service.delete_product(product_id)
    return jsonify({"message": "Product deleted successfully"}), 200

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    product_repository = ProductRepository(g.db)
    category_repository = CategoryRepository(g.db)
    product_service = ProductService(product_repository, category_repository)

    product = product_service.get_product_details(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category_id": product.category_id,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat()
    }), 200


@products_bp.route('/', methods=['GET'])
def get_all_products():
    product_repository = ProductRepository(g.db)
    category_repository = CategoryRepository(g.db)
    product_service = ProductService(product_repository, category_repository)

    products = product_service.get_all_products()
    return jsonify([{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category_id": product.category_id,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat()
    } for product in products]), 200