from fastapi import HTTPException
from .models import CartItem
from src.order_service.models import Order
from src.user_service.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .scheme import CartItemResponse, ProductResponse
from sqlalchemy.orm import selectinload
from src.product_service.models import Product


class CartItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def adding_product_to_cartitem(self, current_user: User, product_id: int):

        product_query = await self.session.execute(
            select(Product)
            .filter(Product.id == product_id)
            .filter(Product.is_exist != False)
        )

        product = product_query.scalars().first()
        if not product:
            raise HTTPException(detail="Not Found", status_code=404)

        exist_product_query = await self.session.execute(
            select(CartItem)
            .filter(CartItem.product_id == product.id)
            .filter(CartItem.user_id == current_user.id)
        )

        exist_product = exist_product_query.scalars().first()
        if exist_product:
            raise HTTPException(detail="This Product In CartItem", status_code=403)

        new_cartitem = CartItem(
            product_id=product.id,
            user_id=current_user.id,
        )

        self.session.add(new_cartitem)
        await self.session.commit()

    async def get_products_from_cartitem(self, current_user: User):

        cartitem_query = await self.session.execute(
            select(CartItem)
            .filter(CartItem.user_id == current_user.id)
            .filter(CartItem.is_ready_to_order != True)
            .options(selectinload(CartItem.product))
            .order_by(CartItem.created_at.desc())
        )

        carts = cartitem_query.scalars().all()

        response = [
            CartItemResponse(
                id=cart.id,
                product=(
                    ProductResponse(
                        id=cart.product.id,
                        category=cart.product.product_category,
                        created_at=cart.product.created_at,
                        product_photo=cart.product.product_photo,
                        product_title=cart.product.product_title,
                        is_exist=cart.product.is_exist,
                        description=cart.product.description,
                    )
                    if cart.product
                    else None
                ),
                is_ready_to_order=cart.is_ready_to_order,
                user_id=cart.user_id,
                created_at=cart.created_at,
                all_price=(
                    str(
                        sum(
                            cart.product.price
                            for cart in carts
                            if cart.product and cart.product.price is not None
                        )
                    )
                    if carts
                    else None
                ),
            )
            for cart in carts
        ]

        return response

    async def delete_product_from_cart(self, current_user: User, product_id: int):

        cart_item_query = await self.session.execute(
            select(CartItem)
            .filter(CartItem.id == product_id)
            .filter(CartItem.user_id == current_user.id)
        )

        cart_item = cart_item_query.scalars().first()
        if not cart_item:
            raise HTTPException(detail="Product Not Found", status_code=404)

        await self.session.delete(cart_item)
        await self.session.commit()

        return {"message": "Deleted Succsesfully"}
