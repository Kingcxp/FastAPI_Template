from pydantic import BaseModel


class UserBase(BaseModel):
    """
    用户信息基础单元
    """
    name: str
    email: str
    token: str


class UserCreate(UserBase):
    """
    创建用户信息时所需要提供的内容
    """
    pass


class User(UserBase):
    """
    获取用户信息时获得的内容
    """
    uid: int

    class Config:
        from_attributes = True
