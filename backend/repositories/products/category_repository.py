from typing import Optional

class CategoryRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_category_by_id(self, category_id: int) -> Optional[dict]:
        query = "SELECT * FROM categories WHERE id = :category_id"
        result = self.db_session.execute(query, {"category_id": category_id}).fetchone()
        return dict(result) if result else None

    def get_all_categories(self) -> list[dict]:
        query = "SELECT * FROM categories"
        result = self.db_session.execute(query).fetchall()
        return [dict(row) for row in result]

    def create_category(self, name: str) -> int:
        query = """
        INSERT INTO categories (name, created_at, updated_at) 
        VALUES (:name, datetime('now'), datetime('now'))"""
        result = self.db_session.execute(query, {"name": name})
        self.db_session.commit()
        return result.lastrowid

    def update_category(self, category_id: int, name: str) -> None:
        query = """
        UPDATE categories 
        SET name = :name, updated_at = datetime('now') 
        WHERE id = :category_id"""
        self.db_session.execute(query, {"name": name, "category_id": category_id})
        self.db_session.commit()

    def delete_category(self, category_id: int) -> None:
        query = "DELETE FROM categories WHERE id = :category_id"
        self.db_session.execute(query, {"category_id": category_id})
        self.db_session.commit()