from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
    computed_field,
)
from typing import Annotated, Self
import re
from app.api.auth.utis import get_password_hash


class EmailSchema(BaseModel):
    email: Annotated[EmailStr, Field(description="Email address")]
    model_config = ConfigDict(from_attributes=True)


class AuthAddSchema(BaseModel):
    first_name: Annotated[
        str,
        Field(min_length=4, max_length=50, description="The first name of the user."),
    ]
    last_name: Annotated[
        str,
        Field(min_length=4, max_length=50, description="The last name of the user."),
    ]
    email: Annotated[EmailStr, Field(description="Email address")]
    phone_number: Annotated[
        str,
        Field(min_length=5, max_length=15, description="The phone number of the user."),
    ]
    password: Annotated[
        str, Field(min_length=5, max_length=100, description="Password of the user.")
    ]

    @staticmethod
    @field_validator("phone_number")
    def validate_phone_number(value: str):
        if not re.match(r"^\+\d{5,15}$", value):
            raise ValueError("Phone number must be entered in the format: +999999999")
        return value


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


class RoleSchema(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class AuthUserReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: Annotated[
        str,
        Field(min_length=4, max_length=50, description="The first name of the user."),
    ]
    last_name: Annotated[
        str,
        Field(min_length=4, max_length=50, description="The last name of the user."),
    ]
    email: Annotated[EmailStr, Field(description="Email address")]
    phone_number: Annotated[
        str,
        Field(min_length=5, max_length=15, description="The phone number of the user."),
    ]

    role: RoleSchema = Field(exclude=True)

    @computed_field
    def role_name(self) -> str:
        return self.role.name

    @computed_field
    def role_id(self) -> int:
        return self.role.id
