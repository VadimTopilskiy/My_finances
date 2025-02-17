import httpx
from typing import Dict

import config






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

async def current_exchange_rate():
    rates = {
        "RUB": 100.0,
        "EUR": 1.12,
        "USD": 1.13,
        "CNY": 7.6
    }

    eur_to_rub = rates["RUB"]

    return rates, eur_to_rub


async def convert_currency(balance_rub: float, rates: Dict[str, float], eur_to_rub: float) -> Dict[str, float]:
    converted_balances = {}

    for currency, rate in rates.items():
        converted_balances[currency] = round(balance_rub * (rate / eur_to_rub), 2)
    del converted_balances["RUB"]
    return converted_balances
