from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Annotated, Self, Optional


class GroupBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Annotated[str, Field(min_length=3, max_length=10, description="group name")]

    @model_validator(mode="after")
    def transform_name_to_uppercase(self) -> Self:
        self.name = self.name.upper()
        return self


class GroupReadSchema(GroupBaseSchema):
    id: int


class GroupUpdateSchema(GroupBaseSchema):
    name: Annotated[
        Optional[str], Field(min_length=3, max_length=10, description="group name")
    ] = None
