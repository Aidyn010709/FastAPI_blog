from fastapi import FastAPI, Depends
from aioredis import create_redis_pool, Redis
from product.routers.products import product_router
from database import SQLALCHEMY_DATABASE_URL
import asyncpg

app = FastAPI(
    title="Amazon"
)

@app.on_event("startup")
async def startup_db_client():
    app.state.pool = await asyncpg.create_pool(SQLALCHEMY_DATABASE_URL)
    app.state.redis = await create_redis_pool('redis://localhost')

@app.on_event("shutdown")
async def shutdown_db_client():
    await app.state.pool.close()
    app.state.redis.close()
    await app.state.redis.wait_closed()

app.include_router(product_router)

async def get_redis(app: FastAPI = Depends()):
    return app.state.redis
