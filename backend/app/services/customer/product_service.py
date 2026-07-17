from sqlalchemy.ext.asyncio import AsyncSession
from ...repositories.product_repository import ProductRepository
from ...repositories.category_repository import CategoryRepository
from ...schemas.customer.product import ProductResponse, ProductCreate
from ...schemas.customer.pagination import PaginatedResponse, PaginationParams
from ...core.exceptions import NotFoundException, BadRequestException

class ProductService:
    def __init__(self, db: AsyncSession):
        self.product_repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)

    async def get_all_products(self, params: PaginationParams) -> PaginatedResponse[ProductResponse]:
        total = await self.product_repo.count_all()
        products = await self.product_repo.get_all(offset=params.offset, limit=params.size)
        items = [ProductResponse.model_validate(p) for p in products]
        pages = (total + params.size - 1) // params.size if total > 0 else 1
        return PaginatedResponse(
            items=items, total=total, page=params.page, size=params.size, pages=pages
        )
    
    async def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException(detail=f'Product with id {product_id} not found')
        return ProductResponse.model_validate(product)
    
    async def get_products_by_category(self, category_id: int, params: PaginationParams) -> PaginatedResponse[ProductResponse]:
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise NotFoundException(detail=f'Category with id {category_id} not found')
        total = await self.product_repo.count_by_category(category_id)
        products = await self.product_repo.get_by_category(
            category_id=category_id,
            offset=params.offset,
            limit=params.size
        )
        items = [ProductResponse.model_validate(prod) for prod in products]
        pages = (total + params.size - 1) // params.size if total > 0 else 1
        return PaginatedResponse[ProductResponse](
            items=items, total=total, page=params.page, size=params.size, pages=pages
        )
    
    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        category = await self.category_repo.get_by_id(product_data.category_id)
        if not category:
            raise BadRequestException(detail=f'Category with id {product_data.category_id} does not exist')
        product = await self.product_repo.create(product_data)
        return ProductResponse.model_validate(product)

    async def update_product(self, product_id: int, product_data: ProductCreate) -> ProductResponse:
        category = await self.category_repo.get_by_id(product_data.category_id)
        if not category:
            raise BadRequestException(detail=f'Category with id {product_data.category_id} does not exist')
        product = await self.product_repo.update(product_id, product_data)
        if not product:
            raise NotFoundException(detail=f'Product with id {product_id} not found')
        return ProductResponse.model_validate(product)

    async def delete_product(self, product_id: int) -> None:
        deleted = await self.product_repo.soft_delete(product_id)
        if not deleted:
            raise NotFoundException(detail=f'Product with id {product_id} not found')