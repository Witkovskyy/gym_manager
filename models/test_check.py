from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from db_setup import engine, Client


Session = sessionmaker(bind=engine)
session = Session()

statement = select(Client)

for client in session.scalars(statement):
    print(client)