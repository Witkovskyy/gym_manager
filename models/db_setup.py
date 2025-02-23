from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

#Baza pod db
Base = declarative_base()

#Klienci
class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True)
    rodo = Column(String, nullable=False)
    underage = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    membership_type = Column(String, ForeignKey("memberships.membership_name"))
    membership_start = Column(Date, nullable=True)
    membership_expiry = Column(Date, nullable=True)
    last_visit = Column(Date, nullable=True)
    comments = Column(String, nullable=True)

    def __repr__(self) -> str:
        return(f"Client(id={self.client_id},first name={self.first_name}, last name={self.last_name}," 
                f"membership type={self.membership_type},"
                f"membership start={self.membership_start.strftime('%d-%m-%Y')},"
                f"membership expiry={self.membership_expiry.strftime('%d-%m-%Y')})" )
    
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
engine = create_engine("sqlite:///gym_manager.db", echo=False)

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