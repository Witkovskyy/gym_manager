from sqlalchemy.orm import sessionmaker
from db_setup import engine, Membership
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()

with open("memberships.txt","r", encoding="utf-8") as file:
    for line in file:
        data = line.strip().split(",")

        membership = Membership(
            membership_id = int(data[0]),
            membership_name = data[1],
            membership_duration_in_days = int(data[2]),
            price = int(data[3])
        )

        try:
            session.add(membership)
        except:
            session.rollback()
            raise
        else:
            session.commit()





# Zapisujemy dane w bazie
session.commit()
session.close()
print("Dane zaimportowane pomyślnie!")