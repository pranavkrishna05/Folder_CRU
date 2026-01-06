from flask import Blueprint, request, jsonify, g
from backend.repositories.auth.user_repository import UserRepository
from backend.repositories.auth.session_repository import SessionRepository
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
    user_service = UserService(user_repository, None)

    try:
        user_id = user_service.register_user(email, password)
        return jsonify({"user_id": user_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user_repository = UserRepository(g.db)
    session_repository = SessionRepository(g.db)
    user_service = UserService(user_repository, session_repository)

    user = user_service.authenticate_user(email, password)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    session = user_service.create_session(user)

    return jsonify({"token": session.token, "expires_at": session.expires_at.isoformat()}), 200

@auth_bp.route('/validate-session', methods=['POST'])
def validate_session():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({"error": "Token is required"}), 400

    session_repository = SessionRepository(g.db)
    user_service = UserService(None, session_repository)

    if user_service.validate_session(token):
        return jsonify({"message": "Session is valid"}), 200
    else:
        return jsonify({"error": "Invalid or expired session"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({"error": "Token is required"}), 400

    session_repository = SessionRepository(g.db)
    user_service = UserService(None, session_repository)

    user_service.terminate_session(token)
    return jsonify({"message": "Logged out successfully"}), 200