from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///budgetwise.db')
Session = sessionmaker(bind=engine)

def init_db():
    from datamodel import Base
    Base.metadata.create_all(bind=engine)
    return Session()

def get_session():
    return Session()