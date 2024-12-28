from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    EmailStr,
    field_validator,
    computed_field,
)
from typing import Annotated, Optional, Literal
import re

from app.api.roles.schemas import RoleSchemaRead


class UserBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: Annotated[
        str, Field(min_length=4, max_length=50, description="First name")
    ]
    last_name: Annotated[
        str, Field(min_length=4, max_length=50, description="Last name")
    ]
    email: Annotated[EmailStr, Field(max_length=100, description="Email address")]
    phone_number: Annotated[
        str, Field(min_length=5, max_length=20, description="Phone number")
    ]

    @staticmethod
    @field_validator("phone_number")
    def validate_phone_number(value: str):
        if not re.match(r"^\+\d{5,15}$", value):
            raise ValueError("Phone number must be entered in the format: +999999999")
        return value


class UserReadSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role_id: int


class UserReadListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    users: list[UserReadSchema]


class UserUpdateSchema(UserBaseSchema):
    first_name: Annotated[
        Optional[str], Field(min_length=4, max_length=50, description="First name")
    ] = None
    last_name: Annotated[
        Optional[str], Field(min_length=4, max_length=50, description="Last name")
    ] = None
    email: Annotated[
        Optional[EmailStr], Field(max_length=100, description="Email address")
    ] = None
    phone_number: Annotated[
        Optional[str], Field(min_length=5, max_length=20, description="Phone number")
    ] = None


class UserRoleIDSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    role_id: Annotated[int, Field(ge=0, description="User ID")]
