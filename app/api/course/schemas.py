from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional


class BaseCourseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Annotated[str, Field(min_length=5, max_length=70, description="Course name")]
    description: Annotated[
        str,
        Field(min_length=10, max_length=1000, description="Description of the course"),
    ]
    credit_hours: int
    user_id: Annotated[int, Field(description="Teacher ID")]


class CourseReadSchema(BaseCourseSchema):
    id: int


class CourseUpdateSchema(BaseCourseSchema):
    name: Annotated[
        Optional[str], Field(min_length=5, max_length=70, description="course name")
    ] = None
    description: Annotated[
        Optional[str], Field(min_length=10, max_length=1000, description="description")
    ] = None
    credit_hours: Annotated[Optional[int], Field(description="credit hours")] = None
    user_id: Annotated[Optional[int], Field(description="teacher id")] = None
