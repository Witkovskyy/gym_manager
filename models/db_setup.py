from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from pathlib import Path
from PyQt6.QtCore import QDate
from datetime import date, timedelta

#Baza pod db
Base = declarative_base()

#Klienci
class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True, autoincrement=True)
    rodo = Column(String, nullable=False, default="Tak")
    underage = Column(String, nullable=False, default="Nie")
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    membership_type = Column(String, ForeignKey("memberships.membership_name"))
    membership_start = Column(Date, nullable=False, default=date.today())
    membership_expiry = Column(Date, nullable=False,default=date.today()+timedelta(days=30))
    last_visit = Column(Date, nullable=False,default=date.today())
    comments = Column(String, nullable=True)

    def __init__(self, is_rodo, is_underage, first_name, last_name, membership_type, start_date, expiry_date, comments=None):
        self.is_rodo = is_rodo
        self.is_underage = is_underage
        self.first_name = first_name
        self.last_name = last_name
        self.membership_type = membership_type
        self.start_date = start_date
        self.expiry_date = expiry_date
        self.comments = comments

    def __repr__(self) -> str:
        return(f"Client(id={self.client_id},first name={self.first_name}, last name={self.last_name}," 
                f"membership type={self.membership_type},"
                # f"membership start={self.membership_start.strftime('%d-%m-%Y')},"
                # f"membership expiry={self.membership_expiry.strftime('%d-%m-%Y')})" 
                f"membership start={self.membership_start}, "
                f"membership expiry={self.membership_expiry} "
                f"last_visit={self.last_visit} "
                f"comment={self.comments}"
                )
    
#Karnety
class Membership(Base):
    __tablename__ = "memberships"
    membership_id = Column(Integer, nullable=False)
    membership_name = Column(String, primary_key=True)
    membership_duration_in_days = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    

    def __repr__(self) -> str:
        return(f"Membership(id={self.membership_id}, name={self.membership_name},duration={self.membership_duration_in_days}, price={self.price})")

#Produkty
class Products(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)
    product_quantity = Column(Integer, nullable=False)
    products_sold = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return(f"Products(id={self.product_id}, name={self.product_name}, price={self.product_price}, quantity={self.product_quantity})")


# Inicjalizacja bazy
base_dir = Path(__file__).resolve().parent.parent
db_path = base_dir / "gym_manager.db"
engine = create_engine(f"sqlite:///{db_path}")

#Tworzenie tabel
Base.metadata.create_all(engine)

#Sesja
Session = sessionmaker(bind=engine)
session = Session()

session.commit()
session.close()




# context manager
# with Session(engine) as session:
#     session.begin()
#     try:
#         session.add(object_1)
#         session.add(object_2)
#     except:
#         session.rollback()
#         raise
#     else:
#         session.commit()