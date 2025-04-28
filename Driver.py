
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3
import pandas as pd
from datetime import datetime


from base import Base
from Account import Account
from Transaction import Transaction


class Driver():
    def __init__(self, db_name):
        self.db_filename = db_name
        self.engine = create_engine(f"sqlite:///{self.db_filename}", echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine, checkfirst=True)
        # acc = Account()
        # transaction = Transaction()
        # self.session.add(acc)
        # self.session.add(transaction)
        # self.session.commit()

    def create_account(self, name):
        new_account = Account(Name=name)
        self.session.add(new_account)
        self.session.commit()
        # print(self.session.query(Account).filter(Account.AccountID == 1).scalar())

    def read_account(self, acc_id):
        try:
            name = self.session.query(Account.Name).filter(Account.AccountID == acc_id).scalar()
            return name
        except:
            print("No result found")

    # idea is to let the front-end grab the account id and then pass it to create a transaction
    def create_transaction(self, acc_id, amt, category):
        account_fetch = self.session.query(Account).filter(Account.AccountID == acc_id).scalar()
        new_transaction = Transaction(AccountID=account_fetch.AccountID, Transaction_Category=category, 
                                    Timestamp = datetime.now(), Quantity = amt)
        self.session.add(new_transaction)
        self.session.commit()
        # print(self.session.query(Transaction).filter(Transaction.TransactionID == 1).one().AccountID)


    def update_transaction(self, acc_id, id, amt, category):
        row = self.session.query(Transaction.AccountID).filter(Transaction.AccountID == acc_id).scalar()
        if (row.AccountID == acc_id):
            update_transaction = Transaction(TransactionID = id, AccountID=acc_id, Transaction_Category=category, 
                                    Timestamp = datetime.datetime.now(), Quantity = amt)
            self.session.update(update_transaction)
            self.session.commit()
        else:
            return 'Transaction does not belong to account'

    def delete_transaction(self, acc_id, id):
        try:
            row = self.session.query(Transaction).filter(Transaction.TransactionID == id).scalar()
            if (row.AccountID == acc_id):
                self.session.delete(row)
                self.session.commit()
            else:
                return 'Transaction does not belong to account'
        except:
            print("No result found")
        
    def read_transaction(self, acc_id, id):
        try:
            row = self.session.query(Transaction).filter(Transaction.TransactionID == id).scalar()
            # Check if this transaction belongs to the current account
            if (row.AccountID == acc_id):
                return row
            else:
                return 'Bad access using wrong account'
        except:
            return 'No result found'

    def export_accounts(self, acc_file_name):
        conn = sqlite3.connect(self.db_filename)
        acc_df = pd.read_sql_query("""SELECT * FROM Accounts""", conn)
        acc_df.to_csv(acc_file_name)

    def export_transactions(self, transact_file_name):
        conn = sqlite3.connect(self.db_filename)
        transact_df = pd.read_sql_query("""SELECT * FROM Transactions""", conn)
        transact_df.to_csv(transact_file_name)

    def import_accounts(self, acc_file_name):
        acc_df = pd.read_csv(acc_file_name)
        acc_df.to_sql('Accounts', con=self.engine, if_exists='replace', index=False)

    def import_transactions(self, transact_file_name):
        transact_df = pd.read_csv(transact_file_name)
        transact_df.to_sql('Transactions', con=self.engine, if_exists='replace', index=False)



