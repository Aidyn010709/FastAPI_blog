from fastapi import FastAPI
from product.routers.products import product_router
from database import SQLALCHEMY_DATABASE_URL
import asyncpg


app = FastAPI(
    title="Amazon"
)

@app.on_event("startup")
async def startup_db_client():
    app.state.pool = await asyncpg.create_pool(SQLALCHEMY_DATABASE_URL)

@app.on_event("shutdown")
async def shutdown_db_client():
    await app.state.pool.close()

app.include_router(product_router)
