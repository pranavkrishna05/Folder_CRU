from typing import Optional, List
from backend.models.shopping_cart import ShoppingCart
from backend.models.cart_item import CartItem

class CartRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_cart_by_user_id(self, user_id: int) -> Optional[dict]:
        query = "SELECT * FROM shopping_carts WHERE user_id = :user_id"
        result = self.db_session.execute(query, {"user_id": user_id}).fetchone()
        return dict(result) if result else None

    def create_cart(self, user_id: int) -> int:
        query = """
        INSERT INTO shopping_carts (user_id, total_price, created_at, updated_at) 
        VALUES (:user_id, 0.0, datetime('now'), datetime('now'))"""
        result = self.db_session.execute(query, {"user_id": user_id})
        self.db_session.commit()
        return result.lastrowid

    def get_items_in_cart(self, cart_id: int) -> List[dict]:
        query = "SELECT * FROM cart_items WHERE cart_id = :cart_id"
        result = self.db_session.execute(query, {"cart_id": cart_id}).fetchall()
        return [dict(row) for row in result]

    def add_item_to_cart(self, cart_id: int, product_id: int, quantity: int) -> int:
        query = """
        INSERT INTO cart_items (cart_id, product_id, quantity, created_at, updated_at) 
        VALUES (:cart_id, :product_id, :quantity, datetime('now'), datetime('now'))"""
        result = self.db_session.execute(query, {"cart_id": cart_id, "product_id": product_id, "quantity": quantity})
        self.db_session.commit()
        return result.lastrowid

    def update_cart_item(self, item_id: int, quantity: int) -> None:
        query = """
        UPDATE cart_items 
        SET quantity = :quantity, updated_at = datetime('now') 
        WHERE id = :item_id"""
        self.db_session.execute(query, {"quantity": quantity, "item_id": item_id})
        self.db_session.commit()

    def remove_item_from_cart(self, item_id: int) -> Optional[float]:
        query = "SELECT cart_id, product_id, quantity FROM cart_items WHERE id = :item_id"
        result = self.db_session.execute(query, {"item_id": item_id}).fetchone()
        if not result:
            return None
        
        item = dict(result)
        self.db_session.execute("DELETE FROM cart_items WHERE id = :item_id", {"item_id": item_id})
        self.db_session.commit()

        query = "SELECT price FROM products WHERE id = :product_id"
        result = self.db_session.execute(query, {"product_id": item['product_id']}).fetchone()
        product_price = result['price'] if result else 0.0

        return product_price * item['quantity']

    def update_cart_total_price(self, cart_id: int, total_price: float) -> None:
        query = """
        UPDATE shopping_carts 
        SET total_price = :total_price, updated_at = datetime('now') 
        WHERE id = :cart_id"""
        self.db_session.execute(query, {"total_price": total_price, "cart_id": cart_id})
        self.db_session.commit()