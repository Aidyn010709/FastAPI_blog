from databases import Database
from asyncpg.pool import Pool
from asyncpg import create_pool
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1@localhost:5432/fastapi_products"

database = Database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(bind=engine)



async def create_asyncpg_pool():
    return await create_pool(SQLALCHEMY_DATABASE_URL)

async def get_database_connection() -> Pool:
    pool = await create_asyncpg_pool()
    async with pool.acquire() as connection:
        yield connection

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()