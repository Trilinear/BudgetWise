from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///Databases/budgetwise.db')
testing_engine = create_engine('sqlite:///Databases/test.db')
Session = sessionmaker(bind=engine)
Testing_Session = sessionmaker(bind=testing_engine)

def init_db():
    from datamodel import Base
    Base.metadata.create_all(bind=engine)
    return Session()

def get_session():
    return Session()

def init_db_unit_test():
    from datamodel import Base
    Base.metadata.create_all(bind=testing_engine)
    return Testing_Session()

def get_unit_test_session():
    return Testing_Session()