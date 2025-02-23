from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True)
    rodo = Column(String, nullable=False)
    underage = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    membership_type = Column(String, nullable=False)
    membership_start = Column(Date, nullable=True)
    membership_expiry = Column(Date, nullable=True)
    last_visit = Column(Date, nullable=True)
    comments = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"Client(id={self.client_id!r},first name={self.first_name!r}, last name={self.last_name!r})"

# Inicjalizacja bazy
engine = create_engine("sqlite:///gym_manager.db", echo=True)

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