from typing import Optional
import logging
from backend.repositories.products.product_repository import ProductRepository
from backend.repositories.products.category_repository import CategoryRepository
from backend.models.product import Product

class ProductService:
    def __init__(self, product_repository: ProductRepository, category_repository: CategoryRepository):
        self.product_repository = product_repository
        self.category_repository = category_repository
        self.logger = logging.getLogger(__name__)

    def validate_product_data(self, name: str, description: str, price: float) -> bool:
        if not name:
            return False
        if not description:
            return False
        if price <= 0:
            return False
        return True

    def add_product(self, name: str, description: str, price: float, category_id: int) -> int:
        if not self.validate_product_data(name, description, price):
            self.logger.error("Invalid product data")
            raise ValueError("Product name, description, and price must be valid")

        existing_product = self.product_repository.get_product_by_name(name)
        if existing_product:
            self.logger.error("Product name %s already exists", name)
            raise ValueError("Product name already exists")

        product_id = self.product_repository.create_product(name, description, price, category_id)
        self.logger.info("Product added with ID: %d, name: %s", product_id, name)
        return product_id

    def update_product(self, product_id: int, name: Optional[str], description: Optional[str], price: Optional[float], category_id: Optional[int]) -> None:
        self.product_repository.update_product(product_id, name, description, price, category_id)
        self.logger.info("Product updated with ID: %d", product_id)

    def delete_product(self, product_id: int) -> None:
        self.product_repository.delete_product(product_id)
        self.logger.info("Product deleted with ID: %d", product_id)

    def get_product_details(self, product_id: int) -> Optional[Product]:
        product_data = self.product_repository.get_product_by_id(product_id)
        if not product_data:
            self.logger.error("Product not found with ID: %d", product_id)
            return None
        return Product(**product_data)

    def get_all_products(self) -> list[Product]:
        products_data = self.product_repository.get_all_products()
        return [Product(**data) for data in products_data]