from datetime import datetime
from typing import Optional

class User:
    id: int
    email: str
    password: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: int, email: str, password: str, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self) -> str:
        return f"<User {self.email}>"