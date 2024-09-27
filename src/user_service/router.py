from fastapi import APIRouter, Depends
from .service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import get_session
from .scheme import SignUp
from .scheme import UserResponse
from src.auth_service.ouath import get_current_user
from src.user_service.models import User


user_service_router = APIRouter(tags=['User'])

@user_service_router.post('/sign-up/')
async def sign_up(request: SignUp, session: AsyncSession = Depends(get_session)):
    service = UserService(session=session)
    return await service.sign_up(request=request)


@user_service_router.get('/user-me/', response_model=UserResponse)
async def user_me(session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    servise = UserService(session=session)
    return await servise.user_me(current_user=current_user)