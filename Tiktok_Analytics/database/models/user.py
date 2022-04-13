from fastapi_users import models
from fastapi_users.db import TortoiseBaseUserModel
from tortoise.contrib.pydantic import PydanticModel


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserModel(TortoiseBaseUserModel):
    pass


class UserDB(User, models.BaseUserDB, PydanticModel):
    """User representation in DB
    """
    _saved_in_db = True

    async def from_tortoise_orm(user: any):
        """ this just to fix the from_tortoise_orm not found
        Args:
            user (any): [description]
        Returns:
            [type]: [description]
        """

        return user
    class Config:
        orm_mode = True
        orig_model = UserModel