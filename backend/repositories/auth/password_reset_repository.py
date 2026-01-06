from typing import Optional

class PasswordResetRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_reset_by_token(self, token: str) -> Optional[dict]:
        query = "SELECT * FROM password_resets WHERE token = :token"
        result = self.db_session.execute(query, {"token": token}).fetchone()
        return dict(result) if result else None

    def create_reset_token(self, user_id: int, token: str) -> int:
        query = """
        INSERT INTO password_resets (user_id, token, expires_at) 
        VALUES (:user_id, :token, datetime('now', '+24 hours'))"""
        result = self.db_session.execute(query, {"user_id": user_id, "token": token})
        self.db_session.commit()
        return result.lastrowid

    def delete_reset_token(self, token: str) -> None:
        query = "DELETE FROM password_resets WHERE token = :token"
        self.db_session.execute(query, {"token": token})
        self.db_session.commit()