from pydantic import BaseModel
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


class BaseResponse(BaseModel):
    status: int = HTTP_200_OK
    error: bool = False


class BaseCreateResponse(BaseModel):
    status: int = HTTP_201_CREATED
    error: bool = False
