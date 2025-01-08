import uvicorn
from fastapi import FastAPI
from api import routers

app = FastAPI()
app.include_router(routers)

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)

