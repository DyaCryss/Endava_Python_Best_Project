# endpoints/fibo.py
from typing import Annotated
from fastapi.params import Depends
from fastapi import APIRouter
from pydantic import BaseModel, Field
from .util import verify_api_key, redis_client
import loguru
from sqlalchemy.orm import Session
from ..db import get_db, Computation, DeletedItem
# TODO: adding a deleted items table


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
async def delete_cache(
    api_key=Depends(verify_api_key),
    db: Session = Depends(get_db),  # type: ignore
):
    loguru.logger.info("Emptying cache for fibo")
    keys = await redis_client.keys("fibo*")
    deleted = []
    for key in keys:
        value = await redis_client.get(key)
        loguru.logger.info(value)
        if value:
            decoded_value = value.decode("utf-8")
            deleted.append({key: decoded_value})

            db.add(
                DeletedItem(
                    key=key.decode("utf-8") if isinstance(key, bytes) else str(key),
                    value=decoded_value,
                    operation="fibo",
                    reason="API DELETE",
                )
            )
        await redis_client.delete(key)

    db.commit()
    return deleted


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
async def fibo_operation(
    payload: FiboRequest,
    api_key=Depends(verify_api_key),
    db: Session = Depends(get_db),  # type: ignore
):
    # trying first to retrieve from redis
    cached_item = await redis_client.get(f"fibo({payload.number})")
    if cached_item:
        factorial = cached_item.decode("utf-8")
        loguru.logger.info(
            f"Retrieved from redis cache some result for fibo operation: {factorial}"
        )
        key = f"fibo({payload.number})"

        db.add(
            Computation(
                operation="fibo",
                input=key,
                result=str(factorial),
                cached=True,
                api_key=api_key,
            )
        )
        db.commit()

        return FiboResponse(answer=factorial, cached=True, api_key=str(api_key))

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

    key = f"fibo({n})"
    await redis_client.set(key, result)  # type: ignore

    db.add(
        Computation(
            operation="fibo",
            input=key,
            result=str(result),
            cached=True,
            api_key=api_key,
        )
    )
    db.commit()

    return FiboResponse(answer=result, api_key=str(api_key), cached=False)
