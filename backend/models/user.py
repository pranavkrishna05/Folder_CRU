from datetime import datetime

class User:
    id: int
    username: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: int, username: str, email: str, password: str, created_at: datetime, updated_at: datetime) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self) -> str:
        return f"<User {self.username}>"