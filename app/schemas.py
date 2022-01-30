from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic.networks import EmailStr


class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id : int
    username: str
    email: EmailStr

    class Config():
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config():
        orm_mode = True


# class PostUpdate(PostBase):
#     pass

class UserAuth(BaseModel):
    id : int
    username : str
    email : str


class Post(PostBase):
    id: int
    created_at: datetime

    class Config():
        orm_mode = True


class UserCreate(BaseModel):
    username : str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username : str
    password: str

    class Config():
        orm_mode = True
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

