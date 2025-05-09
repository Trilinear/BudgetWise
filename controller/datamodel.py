
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, update
from sqlalchemy.orm import relationship
from controller.database import Base
from datetime import datetime
import os

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    accounts = relationship('Account', back_populates='user', cascade='all, delete')
    def add_user(self, session):
        try:
            session.add(self)
            session.commit()
            return 0
        except:
            print('Error adding user to database')
            session.rollback()
            return -1

    def delete_user(self, session):
        try:
            session.delete(self)
            session.commit()
            return 0
        except:
            print('Error deleting user from database')
            session.rollback()
            return -1

    def select_account(self, session, account_index):
        try:
            accounts = session.query(Account).filter(Account.user_id == self.id).all()

            if (accounts[account_index].user_id == self.id):
                return accounts[account_index]
            else:
                return None
        except:
            print('Error selecting account')
            self.session.rollback()
            return None
        
    def get_all_accounts(self, session):
        try:
            accounts = session.query(Account).filter(Account.user_id == self.id).all()
            return accounts
        except:
            print('Error getting accounts')
            self.session.rollback()
            return None
    

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account', cascade='all, delete')
    categories = relationship('Category', back_populates='account', cascade='all, delete')
    
    def add_account(self, session):
        try:
            session.add(self)
            session.commit()
            return 0
        except:
            print('Error adding account to database')
            session.rollback()
            return -1

    def delete_account(self, session):
        try:
            session.delete(self)
            session.commit()
            return 0
        except:
            print('Error deleting account from database')
            session.rollback()
            return -1

    def update_name(self, session):
        try:
             # Session() has no .update() function so we have to run an execute to change the balance
            session.execute(update(Account).where(Account.id == self.id).values(name=self.name))
            session.commit()
            return 0
        except:
            print('Error updating name')
            session.rollback()
            return -1


    def update_balance(self, session, new_balance):
        try:
            # Session() has no .update() function so we have to run an execute to change the balance
            session.execute(update(Account).where(Account.id == self.id).values(balance=new_balance))
            session.commit()
            return 0
        except:
            print('Error updating balance')
            session.rollback()
            return -1

    # Needed because errors occur from SQLAlchemy's lazy loading method when trying to load 
    # transactions from two different accounts using just account.transactions
    def get_all_transactions(self, session):
        try:
            transactions = session.query(Transaction).filter(Transaction.account_id == self.id).all()
            return transactions
        except:
            print('Error getting transactions')
            return None

    def select_transaction(self, session, transaction_index):
        try:
            transactions = session.query(Transaction).filter(Transaction.account_id == self.id).all()
            transaction = transactions[transaction_index]
            return transaction
        except:
            print('Error selecting transaction')
            return None
        
    def select_transactions_by_category(self, session, category_index):
        try:
            categories = session.query(Category).filter(Category.account_id == self.id).all()
            category = categories[category_index].name
            transactions = session.query(Transaction).filter(Transaction.category == category,
                                                             Transaction.account_id == self.id).all()
            return transactions
        except:
            print('Error selecting transactions by category')
            return None
    
    def get_all_categories(self, session):
        try:
            categories = session.query(Category).filter(Category.account_id == self.id).all()
            return categories
        except:
            print('Error getting categories')
            return None

    def select_category(self, session, category_index):
        try:
            categories = session.query(Category).filter(Category.account_id == self.id).all()
            category = categories[category_index]
            return category
        except:
            print('Error selecting category')
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
        try:
            session.add(self)
            session.commit()
            return 0
        except:
            print('Error adding transaction')
            session.rollback()
            return -1

    def delete_transaction(self, session):
        try:
            session.delete(self)
            session.commit()
            return 0
        except:
            print('Error deleting transaction')
            session.rollback()
            return -1
        
    def update_transaction(self, session):
        try:
            session.execute(update(Transaction).where(Transaction.id == self.id).values(
                amount=self.amount, category=self.category, description=self.description))
            session.commit()
            return 0
        except:
            print('Error updating transaction')
            session.rollback()
            return -1


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship('Account', back_populates='categories')
    transactions = relationship('Transaction', back_populates='category_relationship', cascade='all, delete')

    def add_category(self, session):
        try: 
            check_if_exists = session.query(Category).filter(Category.name == self.name, Category.account_id == self.account_id).all()
            if len(check_if_exists) != 0:
                return -1
            else:
                session.add(self)
                session.commit()
                return 0
        except:
            print('Error adding transaction')
            session.rollback()
            return -1

    def delete_category(self, session):
        try:
            session.delete(self)
            session.commit()
            return 0
        except:
            print('Error adding transaction')
            session.rollback()
            return -1

