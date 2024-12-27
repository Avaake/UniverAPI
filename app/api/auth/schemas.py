from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
    Field,
    model_validator,
)
from typing import Annotated, Self
from app.api.auth.utis import get_password_hash
from app.api.users.schemas import UserBaseSchema


class EmailSchema(BaseModel):
    email: Annotated[EmailStr, Field(description="Email address")]
    model_config = ConfigDict(from_attributes=True)


class AuthAddSchema(UserBaseSchema):
    password: Annotated[
        str, Field(min_length=5, max_length=100, description="Password of the user.")
    ]


class AuthRegistrationSchema(AuthAddSchema):
    confirm_password: Annotated[
        str, Field(min_length=5, max_length=100, description="Password of the user.")
    ]

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Пароли не совпадают")
        self.password = get_password_hash(self.password)
        return self


class AuthLoginSchema(EmailSchema):
    password: Annotated[
        str, Field(min_length=5, max_length=100, description="Password of the user.")
    ]
