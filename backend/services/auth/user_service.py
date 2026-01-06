from typing import Optional
import logging
import re
from backend.models.user import User
from backend.repositories.auth.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.logger = logging.getLogger(__name__)

    def validate_password(self, password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[#@%&!]", password):
            return False
        return True

    def register_user(self, email: str, password: str) -> int:
        if not self.validate_password(password):
            self.logger.error("Password does not meet security criteria")
            raise ValueError("Password does not meet security criteria")

        existing_user = self.user_repository.get_user_by_email(email)
        if existing_user:
            self.logger.error("Email %s is already registered", email)
            raise ValueError("Email is already registered")

        user_id = self.user_repository.create_user(email, password)
        self.logger.info("User registered with email: %s", email)
        return user_id

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user_data = self.user_repository.get_user_by_email(email)
        if user_data and user_data["password"] == password:
            self.logger.info("User authenticated with email: %s", email)
            return User(**user_data)
        self.logger.error("Authentication failed for email: %s", email)
        return None