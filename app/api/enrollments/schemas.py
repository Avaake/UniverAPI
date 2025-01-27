from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional


class BaseEnrollmentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: Annotated[int, Field(ge=1, description="student id.")]
    group_id: Annotated[int, Field(ge=1, description="student group identifier.")]
    speciality_id: Annotated[
        int, Field(ge=1, description="identifier of the student's speciality.")
    ]
    academic_year: Annotated[
        int, Field(ge=1, le=7, description="student's academic year 1-7.")
    ]


class EnrollmentUpdateSchema(BaseEnrollmentSchema):
    user_id: Annotated[Optional[int], Field(ge=1, description="student id.")] = None
    group_id: Annotated[
        Optional[int], Field(ge=1, description="student group identifier.")
    ] = None
    speciality_id: Annotated[
        Optional[int],
        Field(ge=1, description="identifier of the student's speciality."),
    ] = None
    academic_year: Annotated[
        Optional[int],
        Field(ge=1, le=7, description="student's academic year 1-7."),
    ] = None
