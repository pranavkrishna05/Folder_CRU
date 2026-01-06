from typing import Optional, List

class CategoryRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_category_by_id(self, category_id: int) -> Optional[dict]:
        query = "SELECT * FROM categories WHERE id = :category_id"
        result = self.db_session.execute(query, {"category_id": category_id}).fetchone()
        return dict(result) if result else None

    def get_all_categories(self) -> List[dict]:
        query = "SELECT * FROM categories"
        result = self.db_session.execute(query).fetchall()
        return [dict(row) for row in result]

    def create_category(self, name: str, parent_id: Optional[int] = None) -> int:
        query = """
        INSERT INTO categories (name, parent_id, created_at, updated_at) 
        VALUES (:name, :parent_id, datetime('now'), datetime('now'))"""
        result = self.db_session.execute(query, {"name": name, "parent_id": parent_id})
        self.db_session.commit()
        return result.lastrowid

    def update_category(self, category_id: int, name: Optional[str], parent_id: Optional[int]) -> None:
        update_fields = []
        params = {"category_id": category_id}
        if name is not None:
            update_fields.append("name = :name")
            params["name"] = name
        if parent_id is not None:
            update_fields.append("parent_id = :parent_id")
            params["parent_id"] = parent_id

        if update_fields:
            query = f"""
            UPDATE categories 
            SET {', '.join(update_fields)}, updated_at = datetime('now') 
            WHERE id = :category_id"""
            self.db_session.execute(query, params)
            self.db_session.commit()

    def delete_category(self, category_id: int) -> None:
        query = "DELETE FROM categories WHERE id = :category_id"
        self.db_session.execute(query, {"category_id": category_id})
        self.db_session.commit()