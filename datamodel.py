
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
    categories = relationship('Category', back_populates='account')
    
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

    def select_transaction(self, session, transaction_index):
        try:
            transaction = session.query(Transaction).filter(Transaction.id == self.transactions[transaction_index].id,
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
    
    def get_all_categories(self, session):
        try:
            categories = session.query(Category).filter(Category.account_id == self.id).all()
            return categories
        except:
            return None

    def select_category(self, session, category_index):
        try:
            category = session.query(Category).filter(Category.id == self.categories[category_index].id,
                                                            Category.account_id == self.id).one()
            return category
        except:
            return None

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    category = Column(String, ForeignKey('categories.name'))
    description = Column(String)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    date = Column(DateTime)
    account = relationship('Account', back_populates='transactions')
    category_relationship = relationship('Category', back_populates='transactions')

    def add_transaction(self, session):
        session.add(self)
        session.commit()

    def delete_transaction(self, session):
        session.delete(self)
        session.commit()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship('Account', back_populates='categories')
    transactions = relationship('Transaction', back_populates='category_relationship')

    def add_category(self, session):
        try: 
            check_if_exists = session.query(Category).filter(Category.name == self.name, Category.account_id == self.account_id).all()
            if len(check_if_exists) != 0:
                return None
            else:
                session.add(self)
                session.commit()
        except:
            return None

    def delete_category(self, session):
        session.delete(self)
        session.commit()

