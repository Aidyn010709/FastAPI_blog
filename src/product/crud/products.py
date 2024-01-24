from sqlalchemy.orm import Session
from ..models import products as models
from ..schemas.products import ProductCreate, ProductRead
from aioredis import Redis
from main import FastAPI , Depends


async def get_redis(app: FastAPI = Depends()):
    return app.state.redis


def crud_create_product(db: Session, product: ProductCreate) -> ProductRead:
    db_product = models.product_table.insert().values(
        title=product.title,
        image=product.image,
        price=product.price,
        description=product.description,
        date=product.date
    ).returning(models.product_table.c.id)

    product_id = db.execute(db_product).fetchone()[0]  # Извлекаем созданный ID

    db.commit()

    return ProductRead(id=product_id, **product.dict())

async def crud_get_product(db: Session, product_id: int, redis: Redis = Depends(get_redis)):
    product = await redis.get(f'product:{product_id}')
    if product is None:
        product = db.query(models.product_table).filter(models.product_table.c.id == product_id).first()
        await redis.set(f'product:{product_id}', product)
    return product

def crud_get_all_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.product_table).offset(skip).limit(limit).all()

def crud_update_product(db: Session, product_id: int, product: ProductCreate):
    db_product = models.product_table.update().\
        where(models.product_table.c.id == product_id).\
        values(
            title=product.title,
            image=product.image,
            price=product.price,
            description=product.description,
            date=product.date
        )
    db.execute(db_product)
    db.commit()
    return {'id': product_id}

def crud_delete_product(db: Session, product_id: int):
    db_product = models.product_table.delete().where(models.product_table.c.id == product_id)
    db.execute(db_product)
    db.commit()
    return {'id': product_id}
