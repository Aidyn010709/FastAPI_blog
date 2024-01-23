from sqlalchemy.orm import Session
from ..models import products as models
from ..schemas.products import ProductCreate, ProductRead


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

def crud_get_product(db: Session, product_id: int):
    return db.query(models.product_table).filter(models.product_table.c.id == product_id).first()

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
