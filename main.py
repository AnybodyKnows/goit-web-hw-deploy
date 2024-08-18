import os
from ipaddress import ip_address
from typing import Callable

import uvicorn
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request, status
from sqlalchemy import text
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware

from src.database.db import get_db
from src.routes import contacts, auth, users

import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from src.conf.config import config


app = FastAPI()

banned_ips = [ip_address("192.168.1.1"), ip_address("192.168.1.2")]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.middleware("http")
# async def ban_ips(request: Request, call_next: Callable):
#     ip = ip_address(request.client.host)
#     if ip in banned_ips:
#         return JSONResponse(
#             status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"}
#         )
#     response = await call_next(request)
#     return response


BASE_DIR = Path(__file__).parent
directory = BASE_DIR.joinpath("src").joinpath("static")

app.mount("/static", StaticFiles(directory=directory), name="static")

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        db=0,
        password=config.REDIS_PASSWORD,
    )
    await FastAPILimiter.init(r)


templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "name": "Contact application",
            "head_name": "This is Face for Contacts Application",
        },
    )


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    Health Check API.
    This API checks if the database is running and accessible.

    params:
    db: SQLAlchemy AsyncSession: The database session to be used for the query.

    Returns:
        dict: A dictionary with a message indicating the health status.
        If the database is not accessible, it will return an error message.
    """
    try:
        # Make request

        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:

            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
#     TODO: something to do here


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), log_level="info")
