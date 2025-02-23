from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from db_setup import engine, Products
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()

with open("sample_products.txt", "r", encoding="utf-8") as file:
    for line in file:
        data = line.strip().split(",")

        product = Products(
            product_id = int(data[0]),
            product_name = data[1],
            product_price = float(data[2]),
            product_quantity = int(data[3]),
            products_sold = int(data[4])
        )
        stmt = select(Products).filter_by(product_name=product.product_name)

        product_obj = session.scalars(stmt).all()
        if product_obj == []:
            try:
                session.add(product)
            except:
                session.rollback()
                raise
            else:
                session.commit()
        else:
            continue
        




       

# Zapisujemy dane w bazie
session.commit()
session.close()
print("Dane zaimportowane pomyślnie!")