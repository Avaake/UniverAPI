from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional


class BaseRoleSchema(BaseModel):
    name: Annotated[str, Field(min_length=4, max_length=30, description="role's name")]
    model_config = ConfigDict(from_attributes=True)


class RoleSchemaRead(BaseRoleSchema):
    id: int
