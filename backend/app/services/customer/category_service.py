from sqlalchemy.ext.asyncio import AsyncSession
from ...repositories.category_repository import CategoryRepository
from ...schemas.customer.category import CategoryCreate, CategoryResponse
from ...core.exceptions import NotFoundException
class CategoryService:
    def __init__(self, db: AsyncSession):
        self.category_repo = CategoryRepository(db)
    
    async def get_all_categories(self) -> list[CategoryResponse]:
        categories = await self.category_repo.get_all()
        return [CategoryResponse.model_validate(cat) for cat in categories]
    
    async def get_category_by_id(self, category_id: int) -> CategoryResponse:
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise NotFoundException(detail=f'Category with id {category_id} not found')
        return CategoryResponse.model_validate(category)
    
    async def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        category = await self.category_repo.create(category_data)
        return CategoryResponse.model_validate(category)

    async def update_category(self, category_id: int, category_data: CategoryCreate) -> CategoryResponse:
        category = await self.category_repo.update(category_id, category_data)
        if not category:
            raise NotFoundException(detail=f'Category with id {category_id} not found')
        return CategoryResponse.model_validate(category)

    async def delete_category(self, category_id: int) -> None:
        deleted = await self.category_repo.delete(category_id)
        if not deleted:
            raise NotFoundException(detail=f'Category with id {category_id} not found')