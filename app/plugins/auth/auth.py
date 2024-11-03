import os
import time

from math import ceil
from random import randint
from functools import reduce
from pydantic import BaseModel
from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from . import router
from .database import get_db, crud, schemas
from ..utils.email import send_mail
from ...manager import console


@router.get("/id")
async def require_id(request: Request) -> JSONResponse:
    """
    返回 session 中存储的用户标识
    """
    uid = request.session.get("uid")
    if uid is not None:
        return JSONResponse(content={
            "uid": uid
        }, status_code=status.HTTP_200_OK)
    return JSONResponse(content={
        "msg": "您尚未登录！"
    }, status_code=status.HTTP_400_BAD_REQUEST)


class VerifyItem(BaseModel):
    # 邮箱地址
    email: str


@router.post("/verify")
async def verify_email(item: VerifyItem, request: Request) -> JSONResponse:
    """
    生成验证码并发送到指定邮箱
    将验证码存储在 session 中
    """
    timeout: float = 30.0
    captcha: str = reduce(lambda x, y: x + y, [str(randint(0, 9)) for _ in range(6)])
    if (last_time := request.session.get("last_captcha_time")) is not None and (time_left := timeout - (time.time() - last_time)) > 0.0:
        return JSONResponse(content={
            "time_left": ceil(time_left),
            "msg": f"请在 {ceil(time_left)} 秒后再发送验证码！"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    if await send_mail(
        target=item.email, sender_name="sender",
        title="验证码", msg=f"验证码：{captcha}，用于邮箱验证，请勿转发。如非本人操作，请忽略本短信。"
    ):
        request.session["captcha"] = captcha
        request.session["last_captcha_time"] = time.time()
        request.session["email"] = item.email
        return JSONResponse(content={}, status_code=status.HTTP_200_OK)
    return JSONResponse(content={
        "msg": "发送失败！请检查邮箱是否输入正确！"
    }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/deprecate")
async def deprecate(request: Request) -> JSONResponse:
    """
    立即销毁 session 中的验证码
    """
    try:
        request.session.pop("captcha")
        request.session.pop("last_captcha_time")
        request.session.pop("email")
    except Exception:
        console.print_exception(show_locals=True)
        pass
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)



@router.post("/register")
async def register(item: schemas.UserCreate, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """
    尝试注册用户
    """
    if await crud.get_user_by_name(db, item.name) is not None:
        return JSONResponse(content={
            "msg": "用户名已存在！"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    new_user = await crud.create_user(db, item)
    if new_user is None:
        return JSONResponse(content={
            "msg": "创建用户失败！请重试或联系管理员！"
        }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


@router.get("/logout")
async def logout(request: Request) -> JSONResponse:
    """
    登出，清空 session 中的信息
    """
    uid = request.session.get("uid")
    if uid is None:
        return JSONResponse(content={
            "msg": "您并未登录！"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    request.session.clear()
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


class LoginItem(BaseModel):
    # 对应数据表中的name
    name: str
    # 双层加密后的密码
    token: str
    # 双层加密时加入的盐
    salt: str


@router.post("/login")
async def login(item: LoginItem, request: Request, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """
    登录，在 session 中保存登录信息
    """
    try_fetch = await crud.get_user_by_name(db, item.name)
    fetch_token = None
    if try_fetch is not None:
        fetch_token = try_fetch.token
    else:
        return JSONResponse(content={
            "msg": "用户名不存在！"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    if crud.encrypter(str(fetch_token), item.salt) != item.token:
        return JSONResponse(content={
            "msg": "密码错误！"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    request.session["uid"] = try_fetch.uid
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


@router.get("/userdata/{which}")
async def fetch_userdata(which: str, request: Request, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """
    获取已登录用户的信息

    通过路由传入字符串，表示需要获取的内容名称，总共有如下几种：
    uid:        uid
    name:       name
    email:      email
    identity:   itentity
    teamname:   teamname
    contact:    contact
    leaders:    leaders
    members:    members
    award:      award
    all:        除 token 和 award 外全部字段
    """
    if (uid := request.session.get("uid")) is None:
        return JSONResponse(content={
            "msg": "您尚未登录！"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    fetch_result = await crud.get_user(db, uid)
    if fetch_result is None:
        return JSONResponse({
            "msg": "用户不存在！"
        }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    match which:
        case "uid":
            return JSONResponse(content={
                "uid": fetch_result.uid
            }, status_code=status.HTTP_200_OK)
        case "name":
            return JSONResponse(content={
                "name": fetch_result.name
            }, status_code=status.HTTP_200_OK)
        case "email":
            return JSONResponse(content={
                "email": fetch_result.email
            }, status_code=status.HTTP_200_OK)
        case "all":
            return JSONResponse(content={
                "uid": fetch_result.uid,
                "name": fetch_result.name,
                "email": fetch_result.email,
            }, status_code=status.HTTP_200_OK)
        case _:
            return JSONResponse(content={
                "msg": "未找到该存储字段！"
            }, status_code=status.HTTP_400_BAD_REQUEST)
