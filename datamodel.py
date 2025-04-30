
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    accounts = relationship('Account', back_populates='user')

    def fetch_accounts(self, session):
        return session.query(Account).filter(Account.user_id == self.id).all()
    
    def select_account(self, session, account_id):
        try:
            account = session.query(Account).filter(Account.id == account_id).one()
            if (account.user_id == self.id):
                return account
            else:
                return None
        except:
            return None
    

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')

    def fetch_transactions(self, session):
        return session.query(Transaction).filter(Transaction.account_id == self.id).all()
    
    def select_transaction(self, session, transaction_id):
        try:
            transaction = session.query(Transaction).filter(Transaction.id == transaction_id).one()
            if transaction.account_id == self.id:
                return transaction
            else:
                return None
        except:
            return None

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    description = Column(String)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    date = Column(DateTime)
    account = relationship('Account', back_populates='transactions')

    def add_transaction(self, session):
        session.add(self)
        session.commit()

    def delete_transaction(self, session):
        session.delete(self)
        session.commit()