from datetime import datetime

class Product:
    id: int
    name: str
    description: str
    price: float
    category_id: int
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: int, name: str, description: str, price: float, category_id: int, created_at: datetime, updated_at: datetime) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self) -> str:
        return f"<Product {self.name}>"