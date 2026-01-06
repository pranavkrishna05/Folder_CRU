from flask import Blueprint, request, jsonify, g
from backend.repositories.cart.cart_repository import CartRepository
from backend.repositories.products.product_repository import ProductRepository

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not user_id or not product_id or not quantity:
        return jsonify({"error": "User ID, product ID, and quantity are required"}), 400

    cart_repository = CartRepository(g.db)
    product_repository = ProductRepository(g.db)
    cart = cart_repository.get_cart_by_user_id(user_id)
    
    if not cart:
        cart_id = cart_repository.create_cart(user_id)
    else:
        cart_id = cart['id']

    cart_item = cart_repository.add_item_to_cart(cart_id, product_id, quantity)
    return jsonify({"cart_item_id": cart_item}), 201

@cart_bp.route('/update/<int:item_id>', methods=['PATCH'])
def update_cart_item(item_id):
    data = request.get_json()
    quantity = data.get('quantity')

    if not quantity:
        return jsonify({"error": "Quantity is required"}), 400

    cart_repository = CartRepository(g.db)
    cart_repository.update_cart_item(item_id, quantity)
    return jsonify({"message": "Cart item updated successfully"}), 200

@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
def remove_cart_item(item_id):
    cart_repository = CartRepository(g.db)
    cart_repository.remove_item_from_cart(item_id)
    return jsonify({"message": "Cart item removed successfully"}), 200

@cart_bp.route('/<int:user_id>', methods=['GET'])
def get_cart_items(user_id):
    cart_repository = CartRepository(g.db)
    cart = cart_repository.get_cart_by_user_id(user_id)
    
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    items = cart_repository.get_items_in_cart(cart['id'])
    return jsonify(items), 200