from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, APIRouter, Depends
from src.user_service.hash import Hash
from src.user_service import models
from sqlalchemy import select
from .token import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import get_session

auth_service = APIRouter(tags=['Auth'])


@auth_service.post('/login/')
async def login(session: AsyncSession = Depends(get_session),  request: OAuth2PasswordRequestForm = Depends()):
    user_result = await session.execute(
        select(models.User).filter(models.User.username == request.username)
    )

    user = user_result.scalars().first()

    if not user:
        raise HTTPException(detail={"error": "Invalid Creadion"}, status_code=402)

    if not Hash.verify(request.password, user.password):
        raise HTTPException(detail=f"In Correct", status_code=402)

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}