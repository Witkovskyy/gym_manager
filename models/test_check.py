from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from db_setup import engine, Client


Session = sessionmaker(bind=engine)
session = Session()

statement = select(Client)

for client in session.scalars(statement):
    #formatted_date = client.membership_start.strftime("%d-%m-%Y")
    #  print(f"ID: {client.client_id}, Imię: {client.first_name}, Start karnetu: {formatted_date}")
    print(client)