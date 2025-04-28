from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Double
from sqlalchemy.orm import relationship
import sqlite3
import Account
import pandas as pd
import datetime
from base import Base

class Transaction(Base):
    __tablename__ = 'Transactions'
    TransactionID = Column(Integer, primary_key=True)
    AccountID = Column(Integer, ForeignKey('Accounts.AccountID'))
    Transaction_Category = Column(String)
    Timestamp = Column(DateTime)
    Quantity = Column(Double)
    account = relationship('Account', back_populates='transaction')

