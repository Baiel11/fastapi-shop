from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.cart_repository import CartRepository
from ..repositories.product_repository import ProductRepository
from ..schemas.cart import CartItem as SchemaCartItem, CartResponse
from ..core.exceptions import NotFoundException
class CartService:
    def __init__(self, db: AsyncSession):
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)

    async def get_cart(self, user_id: int) -> CartResponse:
        db_items = await self.cart_repo.get_user_cart(user_id)

        cart_items = []
        total_price = 0.0
        total_items = 0

        for item in db_items:
            product = item.product
            subtotal = product.price * item.quantity

            schema_item = SchemaCartItem(
                product_id=product.id,
                name=product.name,
                price=product.price,
                quantity=item.quantity,
                subtotal=subtotal,
                image_url=product.image_url
            )

            cart_items.append(schema_item)
            total_price += subtotal
            total_items += item.quantity
        
        return CartResponse(items=cart_items, total=total_price, items_count=total_items)
    
    async def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> CartResponse:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException(detail="Product with id {product_id} not found")
        
        await self.cart_repo.add_or_update_item(user_id, product_id, quantity)
        return await self.get_cart(user_id)
    
    async def update_cart_item(self, user_id: int, product_id: int, quantity: int) -> CartResponse:
        updated = await self.cart_repo.update_item_quantity(user_id, product_id, quantity)
        if not updated:
            raise NotFoundException(detail=f"Product with id {product_id} not found in cart")
        return await self.get_cart(user_id)
    
    async def remove_from_cart(self, user_id: int, product_id: int) -> CartResponse:
        removed = await self.cart_repo.remove_item(user_id, product_id)
        if not removed:
            raise NotFoundException(detail=f"Product with id {product_id} not found in cart")
        return await self.get_cart(user_id)