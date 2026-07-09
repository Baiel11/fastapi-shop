from sqlalchemy.orm import Session
from ..repositories.product_repository import ProductRepository
from ..repositories.category_repository import CategoryRepository
from ..schemas.product import ProductResponse, ProductCreate
from ..schemas.pagination import PaginatedResponse, PaginationParams
from ..core.exceptions import NotFoundException, BadRequestException

class ProductService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)
    
    def get_all_products(self, params: PaginationParams) -> PaginatedResponse[ProductResponse]:
        total = self.product_repository.count_all()
        products = self.product_repository.get_all(
            offset=params.offset,
            limit=params.size
        )
        items = [ProductResponse.model_validate(prod) for prod in products]
        pages = (total + params.size - 1) // params.size if total > 0 else 1
        return PaginatedResponse[ProductResponse](
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )
    
    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundException(detail=f'Product with id {product_id} not found')
        return ProductResponse.model_validate(product)
    
    def get_products_by_category(self, category_id: int, params: PaginationParams) -> PaginatedResponse[ProductResponse]:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise NotFoundException(detail=f'Category with id {category_id} not found')
        total = self.product_repository.count_by_category(category_id)
        products = self.product_repository.get_by_category(
            category_id=category_id,
            offset=params.offset,
            limit=params.size
        )
        items = [ProductResponse.model_validate(prod) for prod in products]
        pages = (total + params.size - 1) // params.size if total > 0 else 1

        return PaginatedResponse[ProductResponse](
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )
    
    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        category = self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise BadRequestException(detail=f'Category with id {product_data.category_id} does not exist')
        product = self.product_repository.create(product_data)
        return ProductResponse.model_validate(product)