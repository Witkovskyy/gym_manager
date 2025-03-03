from sqlalchemy import select
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
        stmt = select(Membership).filter_by(membership_id=membership.membership_id)

        membership_obj = session.scalars(stmt).all()
        if membership_obj == []:
            try:
                session.add(membership)
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