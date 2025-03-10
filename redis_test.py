from fastapi import APIRouter
import redis.asyncio as aioredis

router = APIRouter(prefix="/test", tags=["Redis Test"])


async def get_redis():
    return aioredis.from_url("redis://localhost")


@router.post("/set/{key}")
async def set_value(key: str, value: str):
    redis = await get_redis()
    await redis.set(key, value, ex=60)
    await redis.close()
    return {"message": f"Key '{key}' set with value '{value}'"}


@router.get("/get/{key}")
async def get_value(key: str):
    redis = await get_redis()
    value = await redis.get(key)
    await redis.close()
    if value is None:
        return {"message": "Ключ не установлен"}
    return {"key": key, "value": value}
