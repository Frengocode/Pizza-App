from .hash import Hash
from .models import User
from .scheme import SignUp
from src.config.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from .scheme import UserResponse


class UserService:
    def __init__(self, session = AsyncSession):
        self.session = session

    async def sign_up(self, request: SignUp):
        
        exist_username_query = await self.session.execute(

            select(User)
            .filter(User.username == request.username)

        )

        exist_username = exist_username_query.scalars().first()
        if exist_username:
            raise HTTPException(
                detail='Username All ready using',
                status_code=404
            )

        if len(request.username) < 5:
            raise HTTPException(
                detail='Username Is so short',
                status_code=403
            )
        
        hashed_password = Hash.bcrypt(request.password)
        

        user = User(

            username = request.username,
            password = hashed_password,

        )

        self.session.add(user)
        await self.session.commit()
        return {'detail': 'Account Created Succsesfully'}
    

    async def user_me(self, current_user: User):

        user_query = await self.session.execute(

            select(User)
            .filter(User.id == current_user.id)

        )

        user = user_query.scalars().first()

        response = UserResponse(

            id = user.id,
            username = user.username
        )

        return response