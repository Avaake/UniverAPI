from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional


class SpecialityBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Annotated[
        str, Field(min_length=5, max_length=100, description="Speciality name")
    ]
    descriptions: Annotated[
        str, Field(min_length=10, max_length=1000, description="Speciality description")
    ]


class SpecialityReadSchema(SpecialityBaseSchema):
    id: int


class SpecialityUpdateSchema(SpecialityBaseSchema):
    name: Annotated[
        Optional[str],
        Field(min_length=5, max_length=100, description="Speciality name"),
    ] = None
    descriptions: Annotated[
        Optional[str],
        Field(min_length=10, max_length=1000, description="Speciality description"),
    ] = None
