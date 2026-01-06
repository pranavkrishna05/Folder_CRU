from datetime import datetime, timedelta

class Session:
    id: int
    user_id: int
    token: str
    expires_at: datetime

    def __init__(self, id: int, user_id: int, token: str, expires_at: Optional[datetime] = None) -> None:
        self.id = id
        self.user_id = user_id
        self.token = token
        self.expires_at = expires_at or datetime.utcnow() + timedelta(hours=1)

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

    def __repr__(self) -> str:
        return f"<Session {self.id} for User {self.user_id}>"