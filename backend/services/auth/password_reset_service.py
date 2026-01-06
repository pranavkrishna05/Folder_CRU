from typing import Optional
import logging
import secrets
from backend.repositories.auth.password_reset_repository import PasswordResetRepository
from backend.repositories.auth.user_repository import UserRepository
from backend.models.password_reset import PasswordReset

class PasswordResetService:
    def __init__(self, password_reset_repository: PasswordResetRepository, user_repository: UserRepository):
        self.password_reset_repository = password_reset_repository
        self.user_repository = user_repository
        self.logger = logging.getLogger(__name__)

    def request_password_reset(self, email: str) -> str:
        user = self.user_repository.get_user_by_email(email)
        if not user:
            self.logger.error("No user found with email: %s", email)
            raise ValueError("No user found with this email")

        token = secrets.token_urlsafe(32)
        self.password_reset_repository.create_reset_token(user["id"], token)
        self.logger.info("Password reset token created for user: %s", email)

        # Here we would normally send an email with the reset link containing the token
        # For example: send_email(user.email, "Password Reset Request", f"Use this link to reset your password: {url_for('auth.reset_password', token=token, _external=True)}")
        return token

    def validate_reset_token(self, token: str) -> Optional[PasswordReset]:
        reset_data = self.password_reset_repository.get_reset_by_token(token)
        if not reset_data:
            self.logger.error("Invalid token: %s", token)
            return None

        reset = PasswordReset(**reset_data)
        if reset.is_expired():
            self.logger.error("Token expired: %s", token)
            self.password_reset_repository.delete_reset_token(token)
            return None

        return reset

    def reset_password(self, token: str, new_password: str) -> None:
        reset = self.validate_reset_token(token)
        if not reset:
            raise ValueError("Invalid or expired token")

        if len(new_password) < 8:
            raise ValueError("New password does not meet security criteria")

        self.user_repository.update_user_password(reset.user_id, new_password)
        self.password_reset_repository.delete_reset_token(token)
        self.logger.info("Password reset successfully for user_id: %d", reset.user_id)