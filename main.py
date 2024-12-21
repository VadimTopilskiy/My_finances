import uvicorn
from fastapi import FastAPI, APIRouter
from api.handlers import user_router, main_api_router

app = FastAPI()
app.include_router(main_api_router)
main_api_router.include_router(user_router, prefix="/user", tags=["user"])

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
