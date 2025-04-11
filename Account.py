
import pandas as pd
from datetime import datetime


class Account:
    def __init__(self, name, transaction_history, account_balance):
        self.name = name
        self.transaction_history = transaction_history
        self.transaction_categories = ['Expenditures', 'Income', 'Temporary Loans']
        self.account_balance = account_balance
        self.dataframe = pd.DataFrame(columns=['amount', 'category', 'transaction_type', 'timestamp'])

    # Need to migrate csv storage into sqlite so that we can have cascading events when we delete a category
    def create_category(self, new_category):
        if type(new_category) == str:
            self.transaction_categories.append(new_category)


    def delete_category(self, category):
        if category in self.transaction_categories:
            self.transaction_categories.remove(category)

    def transaction_deposit(self, amt, category):
        if category in self.transaction_categories:
            self.transaction_history.append(amt)
            self.dataframe.loc[len(self.dataframe['amount'])] = [amt, category, 'Deposit', datetime.now()]
            self.account_balance = self.account_balance + amt
    
    def transaction_withdraw(self, amt, category):
        if category in self.transaction_categories:
            self.transaction_history.append(amt)
            self.dataframe.loc[len(self.dataframe['amount'])] = [amt, category, 'Withdraw', datetime.now()]
            self.account_balance = self.account_balance - amt

    def export_data(self, file_name):
        self.dataframe.to_csv(file_name)

    def import_data(self, file_name):
        self.dataframe = pd.read_csv(file_name)