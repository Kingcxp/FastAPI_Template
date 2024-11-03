from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import database


class User(database.Base):
    """
    表: users

    字段:
        uid: 用户编号
        name: 用户名
        email: 联系人邮箱，唯一标识
        token: 密码
    """
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, unique=True)
    email = Column(String(256), unique=True)
    token = Column(String(1024), nullable=False)
