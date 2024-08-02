from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from src.models import UserModel
from src.schemas.user import CreateUserSchema, IdUserSchema, UpdateUserSchema
from src.schemas.wrapper import BaseWrapper, CreatedUserWrapper
from src.services.user import UserService
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix='/user')


@router.get('/')
async def get_user(user_id: UUID4, uow: UnitOfWork = Depends(UnitOfWork)):
    user: UserModel | None = await UserService.get_by_query_one_or_none(uow=uow, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return CreatedUserWrapper(payload=user.to_pydantic_schema())


@router.put('/')
async def update_user(new_info: UpdateUserSchema, uow: UnitOfWork = Depends(UnitOfWork)):
    new_info: dict = new_info.model_dump()
    user_id = new_info.pop('id')
    updated_user: UserModel | None = await UserService.update_one_by_id(uow=uow, _id=user_id, values=new_info)
    if not updated_user:
        raise HTTPException(status_code=404, detail='User not found')
    return CreatedUserWrapper(payload=updated_user.to_pydantic_schema())


@router.post('/')
async def create_user(user: CreateUserSchema, uow: UnitOfWork = Depends(UnitOfWork)):
    created_user: UserModel = await UserService.add_one_and_get_obj(uow=uow, **user.model_dump())
    return CreatedUserWrapper(payload=created_user.to_pydantic_schema())


@router.delete('/')
async def delete_user(user_id: IdUserSchema, uow: UnitOfWork = Depends(UnitOfWork)):
    if await UserService.get_by_query_one_or_none(uow=uow, **user_id.model_dump()):
        await UserService.delete_by_query(uow=uow, **user_id.model_dump())
        return BaseWrapper()
    raise HTTPException(status_code=404, detail='User not found')
