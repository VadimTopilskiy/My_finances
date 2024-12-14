import uvicorn
from fastapi import FastAPI
from core.config import settings
from fastapi_my_finances.api import router as api_router
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))



app = FastAPI()
app.include_router(
    api_router,
    prefix=settings.api.prefix,
)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
