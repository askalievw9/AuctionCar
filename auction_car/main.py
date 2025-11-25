import fastapi, redis, uvicorn
from auction_car.api.endpoints import auth, bid, car, feedback, auction, social_auth
from auction_car.db.database import SessionLocal
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from sqladmin import ModelView
from starlette.middleware.sessions import SessionMiddleware
from auction_car.config import SECRET_KEY
from auction_car.admin.setup import *


async def init_redis():
    return redis.Redis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


auction_car = fastapi.FastAPI(lifespan=lifespan)
auction_car.add_middleware(SessionMiddleware, secret_key='SECRET_KEY')
setup_admin(auction_car)


auction_car.include_router(auth.auth_router)
auction_car.include_router(bid.bid_router)
auction_car.include_router(car.car_router)
auction_car.include_router(feedback.feedback_router)
auction_car.include_router(auction.auction_router)
auction_car.include_router(social_auth.social_auth)

if __name__ == "__main__":
    uvicorn.run(auction_car, host="127.0.0.1", port=8000)

