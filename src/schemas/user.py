from pydantic import BaseModel, Field, UUID4


class IdUserSchema(BaseModel):
    id: UUID4


class CreateUserSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    middle_name: str | None = Field(max_length=50, default=None)


class UserSchema(IdUserSchema, CreateUserSchema):
    pass


class UpdateUserSchema(IdUserSchema):
    first_name: str | None = Field(max_length=50, default=None)
    last_name: str | None = Field(max_length=50, default=None)
    middle_name: str | None = Field(max_length=50, default=None)
