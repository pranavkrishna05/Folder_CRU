from typing import Optional

class SessionRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_session_by_token(self, token: str) -> Optional[dict]:
        query = "SELECT * FROM sessions WHERE token = :token"
        result = self.db_session.execute(query, {"token": token}).fetchone()
        return dict(result) if result else None

    def create_session(self, user_id: int, token: str) -> int:
        query = """
        INSERT INTO sessions (user_id, token, expires_at) 
        VALUES (:user_id, :token, datetime('now', '+1 hour'))"""
        result = self.db_session.execute(query, {"user_id": user_id, "token": token})
        self.db_session.commit()
        return result.lastrowid

    def delete_session(self, token: str) -> None:
        query = "DELETE FROM sessions WHERE token = :token"
        self.db_session.execute(query, {"token": token})
        self.db_session.commit()