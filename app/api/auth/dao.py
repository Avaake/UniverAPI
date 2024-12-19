from app.dao.base import BaseDAO
from app.core import User


class AuthDAO(BaseDAO):
    model = User
