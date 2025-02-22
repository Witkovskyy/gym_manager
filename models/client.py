from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    membership_type = Column(String, nullable=False)
    membership_start = Column(Date, nullable=True)
    membership_expiry = Column(Date, nullable=True)
    last_visit = Column(Date, nullable=True)
    comments = Column(String, nullable=True)

# Inicjalizacja bazy
engine = create_engine("sqlite:///gym_manager.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()