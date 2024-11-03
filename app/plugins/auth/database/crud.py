import hashlib

from random import randint
from functools import reduce
from base64 import b64encode
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Iterable, Optional
from sqlalchemy import select, update

from . import models, schemas


def encrypter(victim: str, salt: str) -> str:
    """返回将 victim 和 salt 连接后使用 sha256 加密出的字符串

    Args:
        victim (str): 主字符串
        salt (str): 字符串加盐

    Returns:
        str: 加密结果
    """
    encrypted = hashlib.sha256(victim.encode("utf-8"))
    encrypted.update(salt.encode("utf-8"))
    return encrypted.hexdigest()


def generate_password(length: int, keyring: str = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM") -> str:
    """生成一个随机密码

    Args:
        length (int): 密码长度
        keyring (str): 密码字符的所有备选项

    Returns:
        str: 生成的密码
    """
    return reduce(
        lambda x, y: x + y,
        [keyring[randint(0, len(keyring) - 1)] for _ in range(length)]
    )


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    """
    创建一个用户信息，提供的密码会自动加密，如果无法创建，返回 None
    """
    user.token = b64encode(user.token.encode("utf-8")).decode("utf-8")
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user(db: AsyncSession, uid: int) -> Optional[models.User]:
    """
    通过用户 id 获取用户信息
    """
    return (await db.execute(select(models.User).where(models.User.uid == uid))).scalars().first()


async def get_user_by_name(db: AsyncSession, name: str) -> Optional[models.User]:
    """
    通过用户名获取用户信息
    """
    return (await db.execute(select(models.User).where(models.User.name == name))).scalars().first()


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 25565) -> Iterable[models.User]:
    """
    获取所有的用户信息
    """
    return (await db.execute(select(models.User).offset(skip).limit(limit).order_by(models.User.uid))).scalars().all()


async def update_user_token(db: AsyncSession, uid: int, token: str) -> bool:
    """
    更新用户 token ，返回是否成功
    """
    await db.execute(update(models.User).where(models.User.uid == uid).values(token=token))
    await db.commit()
    await db.flush()
    return True


async def update_user_name(db: AsyncSession, uid: int, name: str) -> bool:
    """
    更新用户名，返回是否成功
    """
    await db.execute(update(models.User).where(models.User.uid == uid).values(name=name))
    await db.commit()
    await db.flush()
    return True


async def delete_user(db: AsyncSession, name: str) -> bool:
    """
    删除一个用户信息，返回是否成功
    """
    if (user := await get_user_by_name(db, name)) is None:
        return False
    await db.delete(user)
    await db.commit()
    await db.flush()
    return True
