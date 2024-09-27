from fastapi import FastAPI
from src.user_service.router import user_service_router
from src.config.database import Base, engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.product_service.router import product_service
from src.auth_service.router import auth_service
from src.order_service.router import order_service
from src.cart_service.router import cart_item_service
from src.order_service.router import order_service
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(title='Pizza App')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажите конкретные домены, если это необходимо
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user_service_router)
app.include_router(product_service)
app.include_router(auth_service)
app.include_router(order_service)
app.include_router(cart_item_service)
app.include_router(order_service)


@app.on_event("startup")
async def on_startup():
    await create_tables()
