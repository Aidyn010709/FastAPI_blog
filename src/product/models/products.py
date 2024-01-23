import sqlalchemy

metadata = sqlalchemy.MetaData()

product_table = sqlalchemy.Table(
    'products',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True),
    sqlalchemy.Column("title", sqlalchemy.String, index=True),
    sqlalchemy.Column("image", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Float),
    sqlalchemy.Column("description", sqlalchemy.Text()),
    sqlalchemy.Column('date', sqlalchemy.DateTime)
)