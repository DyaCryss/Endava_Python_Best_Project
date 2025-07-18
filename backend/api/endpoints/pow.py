from typing import Annotated, Union
from fastapi.params import Depends
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fastapi import HTTPException
from .util import verify_api_key, redis_client
import loguru

supported_types = ["int", "float", "complex"]


# Requests
class PowRequest(BaseModel):
    a: Annotated[Union[int, float, complex], Field(description="First number")]
    b: Annotated[Union[int, float, complex], Field(description="Second number")]


# Response
class PowResponse(BaseModel):
    cached: Annotated[
        bool, Field(description="If it has been retrieved from cache or not")
    ]
    answer: Annotated[
        Union[int, float, complex], Field(description="The exponentiation result")
    ]
    api_key: Annotated[str, Field("The given API key")]


# API related
router = APIRouter(
    prefix="/pow",
    tags=["power"],
    responses={404: {"description": "Not found"}},
)


# helper functions
@router.get("/")
async def get_supported_types():
    loguru.logger.info("Getting all supported types")
    return supported_types


# to empty all the cache
@router.delete("/")
async def delete_cache():
    loguru.logger.info("Emptying cache for pow")
    keys = await redis_client.keys("pow")
    deleted = []
    for key in keys:
        deleted.append(redis_client.get(key))
        await redis_client.delete(key)
    return deleted


# main function
@router.post(
    "/{operand_type}",
    response_model=PowResponse,
    tags=["power"],
    summary="Exponentiation operation",
)
async def pow_operation(
    operand_type: str, payload: PowRequest, api_key=Depends(verify_api_key)
):
    if operand_type not in supported_types:
        loguru.logger.warning("Got an unsupported operand type")
        raise HTTPException(status_code=400, detail="Unsupported operand type")

    cached_item = await redis_client.get(f"pow({payload.a},{payload.b})")

    if cached_item:
        result = cached_item.decode("utf-8")
        if operand_type == "int":
            result = int(result)
        elif operand_type == "float":
            result = float(result)
        elif operand_type == "complex":
            result = complex(result)

        loguru.logger.info(
            f"Retrieved from redis cache some result for pow operation: {result}"
        )
        return PowResponse(answer=result, cached=True, api_key=str(api_key))

    try:
        if operand_type == "int":
            result = int(payload.a) ** int(payload.b)  # type: ignore
        elif operand_type == "float":
            result = float(payload.a) ** float(payload.b)  # type: ignore
        elif operand_type == "complex":
            result = complex(payload.a) ** complex(payload.b)  # type: ignore
        else:
            result = -1
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Computation error: {str(e)}")

    loguru.logger.info(f"Set to redis cache some result for pow operation: {result}")
    await redis_client.set(f"pow({payload.a},{payload.b})", result)  # type: ignore

    return PowResponse(answer=result, api_key=str(api_key), cached=False)
