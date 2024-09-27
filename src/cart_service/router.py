from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.user_service.models import User
from src.auth_service.ouath import get_current_user, get_session
from .service import CartItemService, CartItemResponse


cart_item_service = APIRouter(tags=['CartItem'])


@cart_item_service.post('/add-product-to-cart/{product_id}/')
async def add_product_to_cart(product_id: int, session: AsyncSession  = Depends(get_session), current_user: User = Depends(get_current_user)):
    service = CartItemService(session=session)
    return await service.adding_product_to_cartitem(product_id=product_id, current_user=current_user)


@cart_item_service.get('/get-all-products-form-cart/', response_model=list[CartItemResponse])
async def get_all_products_from_cartimte(session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    service = CartItemService(session=session)
    return await service.get_products_from_cartitem(current_user=current_user)


@cart_item_service.delete('/delete-product-from-cart/')
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    service = CartItemService(session=session)
    return await service.delete_product_from_cart(product_id=product_id, current_user=current_user)
