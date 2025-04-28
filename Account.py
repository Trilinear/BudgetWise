
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import sqlite3
import pandas as pd
from datetime import datetime
from base import Base

class Account(Base):
    __tablename__ = 'Accounts'
    AccountID = Column(Integer, primary_key=True)
    Name = Column(String)
    # TBD on what to do with this unless we just get rid of them and read categories from the ones that have transactions tied to them
    # Transaction_Category = Column(String)
    transaction = relationship('Transaction', back_populates='account')