from typing import Optional
import logging
import re
from backend.models.user import User
from backend.repositories.auth.user_repository import UserRepository
from backend.repositories.auth.session_repository import SessionRepository
from backend.models.session import Session
import secrets

class UserService:
    def __init__(self, user_repository: UserRepository, session_repository: SessionRepository):
        self.user_repository = user_repository
        self.session_repository = session_repository
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
        if not user_data:
            self.logger.error("Invalid email: %s", email)
            return None
        if user_data["is_locked"]:
            self.logger.error("Account is locked: %s", email)
            return None
        if user_data["password"] != password:
            self.user_repository.increment_login_attempts(user_data["id"])
            if user_data["login_attempts"] + 1 >= 5:
                self.user_repository.lock_user(user_data["id"])
                self.logger.error("Account locked due to too many invalid attempts: %s", email)
            return None

        self.user_repository.reset_login_attempts(user_data["id"])
        self.user_repository.update_last_login(user_data["id"])
        self.logger.info("User authenticated with email: %s", email)
        return User(**user_data)

    def create_session(self, user: User) -> Session:
        token = secrets.token_urlsafe(32)
        session_id = self.session_repository.create_session(user.id, token)
        session_data = self.session_repository.get_session_by_token(token)
        return Session(**session_data)

    def validate_session(self, token: str) -> bool:
        session_data = self.session_repository.get_session_by_token(token)
        if not session_data:
            return False
        session = Session(**session_data)
        return not session.is_expired()

    def terminate_session(self, token: str) -> None:
        self.session_repository.delete_session(token)