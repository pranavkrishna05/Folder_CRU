from datetime import datetime
from typing import Optional

class User:
    id: int
    email: str
    password: str
    created_at: datetime
    updated_at: datetime
    login_attempts: int
    is_locked: bool
    last_login_at: Optional[datetime]

    def __init__(self, id: int, email: str, password: str, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None, login_attempts: int = 0, is_locked: bool = False, last_login_at: Optional[datetime] = None) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.login_attempts = login_attempts
        self.is_locked = is_locked
        self.last_login_at = last_login_at

    def __repr__(self) -> str:
        return f"<User {self.email}>"