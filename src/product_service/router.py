from fastapi import Depends, Form, File, UploadFile, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.user_service.models import User
from .service import ProductService, ProductCategory, ProductResponse
from src.config.database import get_session
from src.auth_service.ouath import get_current_user


product_service = APIRouter(tags=["Product"])


@product_service.post("/create-product/")
async def create_product(
    product_category: ProductCategory,
    product_title: str = Form(...),
    price: int = Form(...),
    product_photo: UploadFile = File(...),
    description: str = Form(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(session=session)
    return await service.create_product(
        price=price,
        product_photo=product_photo,
        category=product_category,
        product_title=product_title,
        description=description,
    )


@product_service.get("/get-all-products/", response_model=list[ProductResponse])
async def get_all_products(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(session=session)
    return await service.get_all_products(current_user=current_user)


@product_service.get("/get-product/", response_model=ProductResponse)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(session=session)
    return await service.get_product(product_id=product_id, current_user=current_user)


@product_service.get("/get-product-by-category/", response_model=list[ProductResponse])
async def get_products_by_category(
    category: ProductCategory,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(session=session)
    product_category = category.value
    return await service.get_product_by_category(
        category=product_category, current_user=current_user
    )


@product_service.delete("/delete-product/")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(session=db)

    return await service.delete_product(
        product_id=product_id, current_user=current_user
    )


@product_service.patch("/update-product/")
async def update_product(
    product_id: int,
    category: ProductCategory,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    product_title: str = Form(),
    price: int = Form(),
    description: str = Form(),
    is_exist: bool = Form(),
):
    service = ProductService(session=session)
    return await service.update_product(
        price=price,
        product_id=product_id,
        product_title=product_title,
        is_exist=is_exist,
        category=category.value,
        description=description,
        currrent_user=current_user,
    )


