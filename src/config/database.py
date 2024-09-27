from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URL = 'postgresql+asyncpg://username:password@localhost/PizzaApp'


engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(bind=engine, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
