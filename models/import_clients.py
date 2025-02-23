from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from db_setup import engine, Client
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()

with open("sample_data_clients.txt", "r", encoding="utf-8") as file:
    for line in file:
        data = line.strip().split(",")
        
        client = Client(
            client_id=int(data[0]),
            rodo=data[1],
            underage=data[2],
            first_name=data[3],
            last_name=data[4],
            membership_type=data[5],
            membership_start=datetime.strptime(data[6], "%Y-%m-%d").date(),
            membership_expiry=datetime.strptime(data[7], "%Y-%m-%d").date(),
            last_visit=datetime.strptime(data[8], "%Y-%m-%d").date(),
            comments=data[9]
        )
        stmt = select(Client).filter_by(client_id=client.client_id)

        client_obj = session.scalars(stmt).all()
        if client_obj == []:
            try:
                session.add(client)
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