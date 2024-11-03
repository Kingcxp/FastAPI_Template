from fastapi import APIRouter
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from .database import database


@asynccontextmanager
async def init_db(_: APIRouter) -> AsyncGenerator[None, None]:
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    yield


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    lifespan=init_db
)
__router__ = router


from . import auth
