
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
    
    def select_account(self, session, account_id):
        try:
            account = session.query(Account).filter(Account.id == self.accounts[account_id].id).one()
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
    
    def add_account(self, session):
        session.add(self)
        session.commit()

    def delete_account(self, session):
        session.delete(self)
        session.commit()

    # Needed because errors occur from SQLAlchemy's lazy loading method when trying to load 
    # transactions from two different accounts using just account.transactions
    def get_all_transactions(self, session):
        try:
            transaction = session.query(Transaction).filter(Transaction.account_id == self.id).all()
            return transaction
        except:
            return None

    def select_transaction(self, session, transaction_id):
        try:
            transaction = session.query(Transaction).filter(Transaction.id == self.transactions[transaction_id].id,
                                                            Transaction.account_id == self.id).one()
            return transaction
        except:
            return None
        
    def select_transactions_by_category(self, session, category):
        try:
            transactions = session.query(Transaction).filter(Transaction.category == category,
                                                             Transaction.account_id == self.id).all()
            return transactions
        except:
            return None

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    category = Column(String)
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