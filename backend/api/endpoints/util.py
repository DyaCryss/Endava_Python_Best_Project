from fastapi import HTTPException
import aioredis
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security

API_KEY_NAME = "name"
API_KEY = "key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate API KEY")
    return api_key


redis_client = aioredis.Redis(host="localhost", port=6379, db=0)
