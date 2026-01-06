from typing import Optional

class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        query = "SELECT * FROM users WHERE id = :user_id"
        result = self.db_session.execute(query, {"user_id": user_id}).fetchone()
        return dict(result) if result else None

    def get_user_by_email(self, email: str) -> Optional[dict]:
        query = "SELECT * FROM users WHERE email = :email"
        result = self.db_session.execute(query, {"email": email}).fetchone()
        return dict(result) if result else None

    def create_user(self, email: str, password: str) -> int:
        query = """
        INSERT INTO users (email, password, created_at, updated_at, login_attempts, is_locked, last_login_at, name, preferences) 
        VALUES (:email, :password, datetime('now'), datetime('now'), 0, 0, NULL, NULL, NULL)"""
        result = self.db_session.execute(query, {"email": email, "password": password})
        self.db_session.commit()
        return result.lastrowid

    def update_user_password(self, user_id: int, password: str) -> None:
        query = """
        UPDATE users 
        SET password = :password, updated_at = datetime('now') 
        WHERE id = :user_id"""
        self.db_session.execute(query, {"password": password, "user_id": user_id})
        self.db_session.commit()

    def increment_login_attempts(self, user_id: int) -> None:
        query = """
        UPDATE users 
        SET login_attempts = login_attempts + 1, updated_at = datetime('now') 
        WHERE id = :user_id"""
        self.db_session.execute(query, {"user_id": user_id})
        self.db_session.commit()

    def reset_login_attempts(self, user_id: int) -> None:
        query = """
        UPDATE users 
        SET login_attempts = 0, updated_at = datetime('now') 
        WHERE id = :user_id"""
        self.db_session.execute(query, {"user_id": user_id})
        self.db_session.commit()

    def lock_user(self, user_id: int) -> None:
        query = """
        UPDATE users 
        SET is_locked = 1, updated_at = datetime('now') 
        WHERE id = :user_id"""
        self.db_session.execute(query, {"user_id": user_id})
        self.db_session.commit()

    def update_last_login(self, user_id: int) -> None:
        query = """
        UPDATE users 
        SET last_login_at = datetime('now'), updated_at = datetime('now') 
        WHERE id = :user_id"""
        self.db_session.execute(query, {"user_id": user_id})
        self.db_session.commit()

    def update_user_profile(self, user_id: int, name: Optional[str], preferences: Optional[str]) -> None:
        query = """
        UPDATE users 
        SET name = :name, preferences = :preferences, updated_at = datetime('now') 
        WHERE id = :user_id"""
        self.db_session.execute(query, {"name": name, "preferences": preferences, "user_id": user_id})
        self.db_session.commit()