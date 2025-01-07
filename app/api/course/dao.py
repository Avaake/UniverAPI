from app.dao.base import BaseDAO
from app.core import Course


class CourseDAO(BaseDAO):
    model = Course
