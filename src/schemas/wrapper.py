from pydantic import BaseModel

from src.schemas.user import UserSchema


class BaseWrapper(BaseModel):
    status: int = 200
    error: bool = False


class CreatedUserWrapper(BaseWrapper):
    status: int = 201
    payload: UserSchema


class UpdatedUserWrapper(BaseWrapper):
    payload: UserSchema
