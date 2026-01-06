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
        cart_total_price = 0.0
    else:
        cart_id = cart['id']
        cart_total_price = cart['total_price']

    product = product_repository.get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    item_price = product['price']
    cart_total_price += item_price * quantity
    cart_repository.add_item_to_cart(cart_id, product_id, quantity)
    cart_repository.update_cart_total_price(cart_id, cart_total_price)

    return jsonify({"message": "Product added to cart"}), 201

@cart_bp.route('/update/<int:item_id>', methods=['PATCH'])
def update_cart_item(item_id):
    data = request.get_json()
    quantity = data.get('quantity')
    
    if quantity is None or quantity <= 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    cart_repository = CartRepository(g.db)
    item = cart_repository.get_cart_item_by_id(item_id)
    if not item:
        return jsonify({"error": "Cart item not found"}), 404
    
    cart_id = item['cart_id']
    product_id = item['product_id']
    old_quantity = item['quantity']
    
    product_repository = ProductRepository(g.db)
    product = product_repository.get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    item_price = product['price']
    new_total_price = item_price * (quantity - old_quantity)
    
    cart_repository.update_cart_item(item_id, quantity)
    cart = cart_repository.get_cart_by_user_id(cart_id)
    cart_repository.update_cart_total_price(cart_id, cart['total_price'] + new_total_price)
    
    return jsonify({"message": "Cart item quantity updated successfully"}), 200

@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
def remove_cart_item(item_id):
    confirm = request.args.get('confirm')
    if not confirm or confirm.lower() != 'true':
        return jsonify({"error": "Removal confirmation required"}), 400

    cart_repository = CartRepository(g.db)
    item_total_price = cart_repository.remove_item_from_cart(item_id)

    if item_total_price is not None:
        cart_id = request.args.get('cart_id')
        cart = cart_repository.get_cart_by_user_id(cart_id)
        new_total_price = cart['total_price'] - item_total_price
        cart_repository.update_cart_total_price(cart_id, new_total_price)
        return jsonify({"message": "Cart item removed successfully"}), 200
    else:
        return jsonify({"error": "Cart item not found"}), 404

@cart_bp.route('/<int:user_id>', methods=['GET'])
def get_cart_items(user_id):
    cart_repository = CartRepository(g.db)
    cart = cart_repository.get_cart_by_user_id(user_id)
    
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    items = cart_repository.get_items_in_cart(cart['id'])
    return jsonify({"items": items, "total_price": cart['total_price']}), 200