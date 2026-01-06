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
    
    try:
        product_service.update_product(product_id, name, description, price, category_id)
        return jsonify({"message": "Product updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@products_bp.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    confirm = request.args.get('confirm')
    if not confirm or confirm.lower() != 'true':
        return jsonify({"error": "Deletion confirmation required"}), 400

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

@products_bp.route('/search', methods=['GET'])
def search_products():
    search_term = request.args.get('q')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    if not search_term:
        return jsonify({"error": "Search term is required"}), 400

    product_repository = ProductRepository(g.db)
    category_repository = CategoryRepository(g.db)
    product_service = ProductService(product_repository, category_repository)

    products = product_service.search_products(search_term, limit, offset)
    return jsonify([{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category_id": product.category_id,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat()
    } for product in products]), 200

@products_bp.route('/categories', methods=['GET'])
def get_all_categories():
    category_repository = CategoryRepository(g.db)
    categories = category_repository.get_all_categories()
    return jsonify(categories), 200

@products_bp.route('/categories/add', methods=['POST'])
def add_category():
    data = request.get_json()
    name = data.get('name')
    parent_id = data.get('parent_id')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    category_repository = CategoryRepository(g.db)

    try:
        category_id = category_repository.create_category(name, parent_id)
        return jsonify({"category_id": category_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@products_bp.route('/categories/update/<int:category_id>', methods=['PATCH'])
def update_category(category_id):
    data = request.get_json()
    name = data.get('name')
    parent_id = data.get('parent_id')

    category_repository = CategoryRepository(g.db)
    try:
        category_repository.update_category(category_id, name, parent_id)
        return jsonify({"message": "Category updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@products_bp.route('/categories/delete/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category_repository = CategoryRepository(g.db)
    try:
        category_repository.delete_category(category_id)
        return jsonify({"message": "Category deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400