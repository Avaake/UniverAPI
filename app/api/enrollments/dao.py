from app.dao.base import BaseDAO
from app.core import Enrollment


class EnrollmentDAO(BaseDAO):
    model = Enrollment
