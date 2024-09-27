from pydantic import BaseModel

class SignUp(BaseModel):

    username: str
    password: str



class UserResponse(BaseModel):
    id: int
    username: str