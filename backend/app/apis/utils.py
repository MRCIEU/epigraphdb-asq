import time

from fastapi import APIRouter
from fastapi_cache.decorator import cache

router = APIRouter()


@router.get("/utils/non-cached", response_model=bool)
async def non_cached(arg: int = 0) -> bool:
    time.sleep(2)
    return True


@router.get("/utils/cached", response_model=bool)
@cache()
async def cached(arg: int = 0) -> bool:
    time.sleep(2)
    return True
