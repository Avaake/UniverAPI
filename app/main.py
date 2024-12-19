from contextlib import asynccontextmanager
from app.core import db_helper
from fastapi import FastAPI
from app.api import api_router
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
