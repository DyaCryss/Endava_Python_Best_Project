from typing import Annotated
from fastapi.params import Depends
from fastapi import APIRouter
from pydantic import BaseModel, Field
from .util import verify_api_key, redis_client
import loguru


# Requests
class FiboRequest(BaseModel):
    number: Annotated[int, Field(description="Retrieve n-th number from fibo series")]


# Response
class FiboResponse(BaseModel):
    cached: Annotated[
        bool, Field(description="If it has been retrieved from cache or not")
    ]
    answer: Annotated[int, Field(description="The n-th number of fibo series")]
    api_key: Annotated[str, Field("The given API key")]


# API related
router = APIRouter(
    prefix="/fibo",
    tags=["fibo"],
    responses={404: {"description": "Not found"}},
)


# helper functions
@router.get("/")
async def get_root_fibo():
    return "good fibo"


# to empty all the cache
@router.delete("/")
async def delete_cache():
    loguru.logger.info("Emptying cache for fibo")
    keys = await redis_client.keys("fibo")
    for key in keys:
        await redis_client.delete(key)


@router.post("/", tags=["fibo"], summary="Populate up to n-th number in fibo series")
async def populate(payload: FiboRequest, api_key=Depends(verify_api_key)):
    n = payload.number
    f1 = 1
    f2 = 1
    await redis_client.set("fibo(1)", 1)
    for i in range(2, n):
        c = f1 + f2
        f1 = f2
        f2 = c
        await redis_client.set(f"fibo({i})", c)


# main function
@router.post(
    "/retrieve",
    response_model=FiboResponse,
    tags=["fibo"],
    summary="Retrieving the n-th number of fibo",
)
async def fibo_operation(payload: FiboRequest, api_key=Depends(verify_api_key)):
    # trying first to retrieve from redis
    cached_item = await redis_client.get(f"fibo({payload.number})")
    if cached_item:
        n = cached_item.decode("utf-8")
        loguru.logger.info(
            f"Retrieved from redis cache some result for fibo operation: {n}"
        )
        return FiboResponse(answer=n, cached=True, api_key=str(api_key))

    n = payload.number
    loguru.logger.info(f"Set to redis cache some result for fibo operation: {n}")

    f1 = 1
    f2 = 1
    result = 1
    for i in range(2, n):
        c = f1 + f2
        f1 = f2
        f2 = c
        await redis_client.set(f"fibo({i})", c)
        result = c

    await redis_client.set(f"fibo({n})", result)  # type: ignore

    return FiboResponse(answer=result, api_key=str(api_key), cached=False)
