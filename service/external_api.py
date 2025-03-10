import pickle
from redis_file import get_redis
import httpx
from typing import Dict, Any, Callable
import functools
import config
import json


# async def current_exchange_rate(base_currency: str = "EUR") -> (Dict[str, float], float):
#     params = {
#         "access_key": config.API_KEY,
#         "base": base_currency,
#         "symbols": "RUB,EUR,USD,CNY"
#     }
#
#     async with httpx.AsyncClient() as client:
#         response = await client.get(config.FIXER_API_URL, params=params)
#         if response.status_code == 200:
#             data = response.json()
#             if data.get("success"):
#                 # Логига для бесплатной подписки fixer.io
#                 rates = data.get("rates", {})
#                 eur_to_rub = rates.get("RUB")
#                 # Логига для бесплатной подписки fixer.io
#                 return data.get("rates", {}), eur_to_rub
#
#             else:
#                 raise ValueError(f"Fixer API error: {data.get('error')}")
#         else:
#             response.raise_for_status()


def cache_result(custom_key: str, ttl: int = 60):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            redis_conn = await get_redis()
            cached_result = await redis_conn.get(custom_key)
            if cached_result is not None:
                return pickle.loads(cached_result)
            result = await func(*args, **kwargs)
            await redis_conn.set(custom_key, pickle.dumps(result), ex=ttl)
            return result

        return wrapper

    return decorator


@cache_result(custom_key="rates:latest", ttl=300)
async def current_exchange_rate():
    rates = {
        "RUB": 100.0,
        "EUR": 1.1,
        "USD": 1.11,
        "CNY": 7.4
    }

    eur_to_rub = rates["RUB"]

    return rates, eur_to_rub


async def convert_currency(balance_rub: float, rates: Dict[str, float], eur_to_rub: float) -> Dict[str, float]:
    converted_balances = {}

    for currency, rate in rates.items():
        converted_balances[currency] = round(balance_rub * (rate / eur_to_rub), 2)
    del converted_balances["RUB"]
    return converted_balances
