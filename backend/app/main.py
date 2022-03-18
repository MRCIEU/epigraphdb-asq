from typing import Dict

import aioredis
from common_processing.utils import check_component_status
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.middleware.cors import CORSMiddleware

from app.settings import config

from .apis import (
    assoc_results,
    claim_parsing,
    data,
    ent_harmonization,
    literature_results,
    scores,
    triple_results,
    utils,
)

TITLE = "Annotated Semantic Query"

app = FastAPI(title=TITLE, docs_url="/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        "redis://redis", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/ping", response_model=bool)
def ping(dependencies: bool = True) -> bool:
    if not dependencies:
        return True
    else:
        status: Dict[str, bool] = check_component_status(
            config=config, verbose=True
        )
        res = sum([_ for _ in status.values()]) == len(status.values())
        return res


app.include_router(utils.router, tags=["utils"])
app.include_router(claim_parsing.router, tags=["main: claim parsing"])
app.include_router(ent_harmonization.router, tags=["main: ent_harmonization"])
app.include_router(triple_results.router, tags=["main: triple results"])
app.include_router(
    literature_results.router, tags=["main: literature results"]
)
app.include_router(assoc_results.router, tags=["main: association results"])
app.include_router(data.router, tags=["main: data endpoints"])
app.include_router(scores.router, tags=["main: scores endpoints"])
