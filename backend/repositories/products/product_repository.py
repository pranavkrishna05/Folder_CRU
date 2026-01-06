from typing import Optional

class ProductRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_product_by_id(self, product_id: int) -> Optional[dict]:
        query = "SELECT * FROM products WHERE id = :product_id AND is_active = 1"
        result = self.db_session.execute(query, {"product_id": product_id}).fetchone()
        return dict(result) if result else None

    def get_product_by_name(self, name: str) -> Optional[dict]:
        query = "SELECT * FROM products WHERE name = :name AND is_active = 1"
        result = self.db_session.execute(query, {"name": name}).fetchone()
        return dict(result) if result else None

    def get_all_products(self) -> list[dict]:
        query = "SELECT * FROM products WHERE is_active = 1"
        result = self.db_session.execute(query).fetchall()
        return [dict(row) for row in result]

    def create_product(self, name: str, description: str, price: float, category_id: int) -> int:
        query = """
        INSERT INTO products (name, description, price, category_id, created_at, updated_at, is_active) 
        VALUES (:name, :description, :price, :category_id, datetime('now'), datetime('now'), 1)"""
        result = self.db_session.execute(query, {"name": name, "description": description, "price": price, "category_id": category_id})
        self.db_session.commit()
        return result.lastrowid

    def update_product(self, product_id: int, name: Optional[str], description: Optional[str], price: Optional[float], category_id: Optional[int]) -> None:
        update_fields = []
        params = {"product_id": product_id}
        if name is not None:
            update_fields.append("name = :name")
            params["name"] = name
        if description is not None:
            update_fields.append("description = :description")
            params["description"] = description
        if price is not None:
            update_fields.append("price = :price")
            params["price"] = price
        if category_id is not None:
            update_fields.append("category_id = :category_id")
            params["category_id"] = category_id

        if update_fields:
            query = f"""
            UPDATE products 
            SET {', '.join(update_fields)}, updated_at = datetime('now') 
            WHERE id = :product_id AND is_active = 1"""
            self.db_session.execute(query, params)
            self.db_session.commit()

    def delete_product(self, product_id: int) -> None:
        query = "UPDATE products SET is_active = 0, updated_at = datetime('now') WHERE id = :product_id"
        self.db_session.execute(query, {"product_id": product_id})
        self.db_session.commit()