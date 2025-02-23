from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import date

def check_membership_valid(client):
    today = date.today()
    return client.membership_expiry >= today