from datetime import datetime

class CartItem:
    id: int
    cart_id: int
    product_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: int, cart_id: int, product_id: int, quantity: int, created_at: datetime, updated_at: datetime) -> None:
        self.id = id
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self) -> str:
        return f"<CartItem {self.quantity} of product {self.product_id} in cart {self.cart_id}>"