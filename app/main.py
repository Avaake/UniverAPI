from contextlib import asynccontextmanager
from app.core import db_helper
from fastapi import FastAPI, Request
from app.api import api_router
from app.core import configurate_logger
import uvicorn

import time

log = configurate_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    log.info(
        '"{} {} - {}" - {:.3f}s',
        request.method,
        request.url,
        response.status_code,
        duration,
    )

    return response


app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
