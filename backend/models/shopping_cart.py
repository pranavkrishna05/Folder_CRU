from datetime import datetime

class ShoppingCart:
    id: int
    user_id: int
    total_price: float
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: int, user_id: int, total_price: float, created_at: datetime, updated_at: datetime) -> None:
        self.id = id
        self.user_id = user_id
        self.total_price = total_price
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self) -> str:
        return f"<ShoppingCart {self.id} for user {self.user_id}>"

    def update_total_price(self, item_price: float, quantity: int, add: bool = True):
        if add:
            self.total_price += item_price * quantity
        else:
            self.total_price -= item_price * quantity
        self.updated_at = datetime.utcnow()