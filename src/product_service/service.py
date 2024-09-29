from fastapi import HTTPException, Form, File, UploadFile
from .models import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from .scheme import ProductCategory, ProductResponse
import os
import uuid
from src.user_service.models import User
from sqlalchemy.orm import selectinload

MEDIA_ROOT = "media/product_photo/"


class ProductService:
    def __init__(self, session=AsyncSession):
        self.session = session

    async def create_product(
        self,
        category: ProductCategory,
        description: str = Form(...),
        product_title: str = Form(...),
        price: int = Form(...),
        product_photo: UploadFile = File(...),
    ):

        category = category.value
        file_size = await product_photo.read()
        if len(file_size) <= 10:
            raise HTTPException(
                status_code=400, detail="File size must be greater than 10 bytes."
            )
        product_photo.filename = f"{uuid.uuid4()}.jpg"

        file_path = os.path.join(MEDIA_ROOT, product_photo.filename)
        with open(file_path, "wb") as f:
            f.write(file_size)

        product = Product(
            product_title=product_title,
            product_photo=product_photo.filename,
            price=price,
            product_category=category,
            description=description,
        )

        self.session.add(product)
        await self.session.commit()

        return {"message": "Created Succsesfully"}

    async def get_all_products(self, current_user: User):

        products_query = await self.session.execute(
            select(Product)
            .order_by(Product.created_at.desc())
            .options(selectinload(Product.orders))
            .filter(Product.is_exist != False)
        )

        products = products_query.scalars().all()
        if not products:
            return []

        response = [
            ProductResponse(
                id=product.id,
                price=product.price,
                category=product.product_category,
                product_title=product.product_title,
                product_photo=product.product_photo,
                created_at=product.created_at,
                is_exist=product.is_exist,
                description=product.description,
                number_of_orders=len(product.orders),
            )
            for product in products
        ]

        return response

    async def get_product(self, current_user: User, product_id: int):

        product_query = await self.session.execute(
            select(Product)
            .filter(Product.id == product_id)
            .filter(Product.is_exist != False)
        )

        product = product_query.scalars().first()
        if not product:
            raise HTTPException(detail="Not Found", status_code=404)

        response = ProductResponse(
            id=product.id,
            product_title=product.product_title,
            price=product.price,
            created_at=product.created_at,
            description=product.description,
            product_photo=product.product_photo,
            category=product.product_category,
            is_exist=product.is_exist,
        )

        return response

    async def get_product_by_category(
        self, current_user: User, category: ProductCategory
    ):

        product_category = category

        product_by_category_query = await self.session.execute(
            select(Product)
            .filter(Product.is_exist != False)
            .filter(Product.product_category == product_category)
            .order_by(Product.created_at.desc())
        )

        products = product_by_category_query.scalars().all()

        response = [
            ProductResponse(
                id=product.id,
                product_title=product.product_title,
                price=product.price,
                product_photo=product.product_photo,
                description=product.description,
                category=product.product_category,
                is_exist=product.is_exist,
                created_at=product.created_at,
            )
            for product in products
        ]

        return response

    async def delete_product(self, product_id: int, current_user: User):

        product_query = await self.session.execute(
            select(Product).filter(Product.id == product_id)
        )

        product = product_query.scalars().first()
        if not product:
            raise HTTPException(detail="Not Found", status_code=404)

        file_path = os.path.join(MEDIA_ROOT, str(product.product_photo))
        os.remove(file_path)

        await self.session.delete(product)
        await self.session.commit()
        return {"message": f"Product with id {product_id} deleted"}

    async def update_product(
        self,
        category: ProductCategory,
        currrent_user: User,
        product_id: int,
        price: int = Form(...),
        product_title: str = Form(...),
        description: str = Form(...),
        is_exist: bool = Form(...),
    ):

        product_query = await self.session.execute(
            select(Product).filter(Product.id == product_id)
        )

        product = product_query.scalars().first()
        if not product:
            raise HTTPException(detail="Not Found", status_code=404)

        product.product_title = product_title
        product.price = price
        product.description = description
        product.is_exist = is_exist
        product.category = category

        await self.session.commit()

        return {"Message": f"Product with id {product_id} Updated"}
