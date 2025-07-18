# endpoints/factorial.py
from typing import Annotated
from fastapi.params import Depends
from fastapi import APIRouter
from pydantic import BaseModel, Field
from .util import verify_api_key, redis_client
import loguru
from sqlalchemy.orm import Session
from ..db import get_db, Computation, DeletedItem


# Requests
class FactRequest(BaseModel):
    number: Annotated[
        int, Field(description="Retrieve n-th number from factorial series")
    ]


# Response
class FactResponse(BaseModel):
    cached: Annotated[
        bool, Field(description="If it has been retrieved from cache or not")
    ]
    answer: Annotated[int, Field(description="The n-th number of factorial series")]
    api_key: Annotated[str, Field("The given API key")]


# API related
router = APIRouter(
    prefix="/fact",
    tags=["fact"],
    responses={404: {"description": "Not found"}},
)


# helper functions
@router.get("/")
async def get_root_fact():
    return "good fact"


# to empty all the cache
@router.delete("/")
async def delete_cache(
    api_key=Depends(verify_api_key),
    db: Session = Depends(get_db),  # type: ignore
):
    loguru.logger.info("Emptying cache for fact")
    keys = await redis_client.keys("fact*")
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
                    operation="fact",
                    reason="API DELETE",
                )
            )
        await redis_client.delete(key)

    db.commit()
    return deleted


@router.post(
    "/", tags=["fact"], summary="Populate up to n-th number in factorial series"
)
async def populate(payload: FactRequest, api_key=Depends(verify_api_key)):
    n = payload.number
    f = 1
    await redis_client.set("fact(1)", 1)
    for i in range(2, n + 1):
        f *= i
        await redis_client.set(f"fact({i})", f)


# mai function
@router.post(
    "/retrieve",
    response_model=FactResponse,
    tags=["fact"],
    summary="Retrieving the n-th number of factorial",
)
async def fact_operation(
    payload: FactRequest,
    api_key=Depends(verify_api_key),
    db: Session = Depends(get_db),  # type: ignore
):
    # trying first to retrieve from redis
    cached_item = await redis_client.get(f"fact({payload.number})")
    if cached_item:
        n = cached_item.decode("utf-8")
        loguru.logger.info(
            f"Retrieved from redis cache some result for fact operation: {n}"
        )
        db.add(
            Computation(
                operation="fact",
                input=str(payload.number),
                result=str(n),
                cached=True,
                api_key=api_key,
            )
        )
        db.commit()

        return FactResponse(answer=int(n), cached=True, api_key=str(api_key))

    n = payload.number
    loguru.logger.info(f"Set to redis cache some result for fact operation: {n}")

    f = 1
    result = 1
    await redis_client.set(f"fact({1})", f)
    for i in range(2, n + 1):
        f *= i
        await redis_client.set(f"fact({i})", f)
        result = f

    await redis_client.set(f"fact({n})", result)  # type: ignore

    db.add(
        Computation(
            operation="fact",
            input=str(payload.number),
            result=str(result),
            cached=False,
            api_key=api_key,
        )
    )
    db.commit()

    return FactResponse(answer=result, api_key=str(api_key), cached=False)
