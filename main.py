import uvicorn
from fastapi import FastAPI, HTTPException
from api import routers
from fastapi import Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from service.auth import get_current_user_from_token
from service.external_api import convert_currency, current_exchange_rate
from service.transaction import _get_current_balance
import asyncio
from redis_file import get_redis
from redis_test import router as redis_router


app = FastAPI()
app.include_router(routers)
app.include_router(redis_router)

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)







@app.websocket("/ws")
async def balance_websocket(
        websocket: WebSocket,
        db: AsyncSession = Depends(get_db),
):
    await websocket.accept()
    redis_client = await get_redis()

    try:
        token = await websocket.receive_text()
        current_user = await get_current_user_from_token(token, db)
    except HTTPException:
        await websocket.close(code=1008)
        return

    user_id = current_user.id

    try:
        while True:

            balance_rub = await redis_client.get(f"balance:{user_id}")
            if balance_rub:
                balance_rub = float(balance_rub)
            else:
                balance_rub = await _get_current_balance(user_id, db)
                await redis_client.set(f"balance:{user_id}", balance_rub, ex=300)

            rates = await redis_client.get("cached_rates")
            if rates:
                rates, eur_to_rub = eval(rates)
            else:
                rates, eur_to_rub = await current_exchange_rate()
                await redis_client.set("cached_rates", str((rates, eur_to_rub)), ex=600)

            last_balance_rub = await _get_current_balance(user_id, db)
            last_rates, last_eur_to_rub = await current_exchange_rate()

            if rates != last_rates or balance_rub != last_balance_rub:
                await redis_client.set(f"balance:{user_id}", last_balance_rub, ex=300)
                await redis_client.set("cached_rates", str((last_rates, last_eur_to_rub)), ex=600)
                converted_balances = await convert_currency(balance_rub, rates, eur_to_rub)
                await websocket.send_json({"balance": converted_balances})

            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print(f"The user has disconnected from WebSocket")

    finally:
        await redis_client.close()
