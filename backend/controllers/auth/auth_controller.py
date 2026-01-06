from flask import Blueprint, request, jsonify, g
from backend.repositories.auth.user_repository import UserRepository
from backend.services.auth.user_service import UserService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user_repository = UserRepository(g.db)
    user_service = UserService(user_repository)

    try:
        user_id = user_service.register_user(email, password)
        return jsonify({"user_id": user_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400