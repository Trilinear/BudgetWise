import unittest
import os
import pandas as pd
from database import init_db_unit_test
from datamodel import User, Account, Transaction, Category
from datetime import datetime



class TestAccount(unittest.TestCase):

    # Method to run setUp once for all test, needed becasuse session needs to be persistent
    # across all test cases in this instance for testing so that our base classes work
    @classmethod
    def setUpClass(self):
        if os.path.exists('./Databases/test.db'):
            os.remove('./Databases/test.db')
        self.session = init_db_unit_test()
        # Create User
        self.user = User(
            id=1,
            username='Michael',
            password='FreeRAM'
        )

        # Create Account
        self.account = Account(
            id=2,
            name='Test Account',
            balance=0.0,
            user_id=self.user.id,
        )

        # Create Category
        self.category = Category(
            id=3,
            name='Expansion',
            account_id=self.account.id
        )

        # Create Transaction
        self.transaction = Transaction(
            id=4,
            amount=4.82,
            category = 'Expansion',
            description = 'Test Descript',
            account_id = self.account.id,
            date = datetime.now()
        )

        self.user.add_user(self.session)
        self.account.add_account(self.session)
        self.category.add_category(self.session)
        self.transaction.add_transaction(self.session)

    def test_createUser(self):
        new_user = User(
            id=5,
            username='John',
            password='Coffee'
        )
        new_user.add_user(self.session)

        self.assertTrue(self.session.query(User).filter(User.id == 5).scalar().username == 'John')
        self.assertTrue(self.session.query(User).filter(User.id == 5).scalar().password == 'Coffee')

    def test_deleteUser(self):
        temp_user = User(
            id=6, 
            username='Del', 
            password='This'
        )
        temp_user.add_user(self.session)

        self.assertTrue(self.session.query(User).filter(User.id == 6).scalar().username == 'Del')

        temp_user.delete_user(self.session)

        self.assertTrue(self.session.query(User).filter(User.id == 6).scalar() == None)

    def test_createAccount(self):
        new_account = Account(
            id=7,
            name='Test New Account',
            balance=0.0,
            user_id=self.user.id,
        )
        new_account.add_account(self.session)

        # Check if the other table is still okay
        self.assertTrue(self.session.query(User).filter(User.id == 1).scalar().username == 'Michael')
        self.assertTrue(self.session.query(Account).filter(Account.id == 7, Account.user_id == 1).scalar().name == 'Test New Account')
        self.assertTrue(self.session.query(Account).filter(Account.id == 7, Account.user_id == 1).scalar().balance == 0.0)
    
    def test_deleteAccount(self):
        new_del_account = Account(
            id=8,
            name='Del Acc',
            balance=0.0,
            user_id=self.user.id,
        )
        new_del_account.add_account(self.session)

        self.assertTrue(self.session.query(User).filter(User.id == 1).scalar().username == 'Michael')
        self.assertTrue(self.session.query(Account).filter(Account.id == 8, Account.user_id == 1).scalar().name == 'Del Acc')


        new_del_account.delete_account(self.session)
        self.assertTrue(self.session.query(Account).filter(Account.id == 8, Account.user_id == 1).scalar() == None)


    def test_createCategory(self):
        self.category = Category(
            id=9,
            name='Expansion 2',
            account_id=2
        )
        self.category.add_category(self.session)

        # Check if the other tables are still okay
        self.assertTrue(self.session.query(User).filter(User.id == 1).scalar().username == 'Michael')
        self.assertTrue(self.session.query(Account).filter(Account.id == 2, Account.user_id == 1).scalar().name == 'Test Account')
        self.assertTrue(self.session.query(Category).filter(Category.id == 9, Category.account_id == 2).scalar().name == 'Expansion 2')

    def test_deleteCategory(self):
        self.category = Category(
            id=10,
            name='Del Cat',
            account_id=2
        )
        self.category.add_category(self.session)

        # Check if the other tables are still okay
        self.assertTrue(self.session.query(User).filter(User.id == 1).scalar().username == 'Michael')
        self.assertTrue(self.session.query(Account).filter(Account.id == 2, Account.user_id == 1).scalar().name == 'Test Account')
        self.assertTrue(self.session.query(Category).filter(Category.id == 10, Category.account_id == 2).scalar().name == 'Del Cat')

        self.category.delete_category(self.session)
        self.assertTrue(self.session.query(Category).filter(Category.id == 10, Category.account_id == 2).scalar() == None)

    def test_createTransaction(self):
        new_transaction = Transaction(
            id=11,
            amount=4.82,
            category = self.category.name,
            description = 'Test Descript',
            account_id = self.account.id,
            date = datetime.now()
        )
        new_transaction.add_transaction(self.session)

        # # Check if the other tables are still okay
        self.assertTrue(self.session.query(User).filter(User.id == 1).scalar().username == 'Michael')
        self.assertTrue(self.session.query(Account).filter(Account.id == 2, Account.user_id == 1).scalar().name == 'Test Account')
        self.assertTrue(self.session.query(Category).filter(Category.id == 3, Category.account_id == 2).scalar().name == 'Expansion')

        self.assertTrue(self.session.query(Transaction).filter(Transaction.id == 11, Transaction.category == 'Expansion',
                                                                Transaction.account_id == 2).scalar().amount == 4.82)
        self.assertTrue(self.session.query(Transaction).filter(Transaction.id == 11, Transaction.category == 'Expansion',
                                                        Transaction.account_id == 2).scalar().description == 'Test Descript')
        
    def test_deleteTransaction(self):
        new_transaction = Transaction(
            id=12,
            amount=7.27,
            category = self.category.name,
            description = 'Test Del',
            account_id = self.account.id,
            date = datetime.now()
        )
        new_transaction.add_transaction(self.session)

        # Check if the other tables are still okay
        self.assertTrue(self.session.query(User).filter(User.id == 1).scalar().username == 'Michael')
        self.assertTrue(self.session.query(Account).filter(Account.id == 2, Account.user_id == 1).scalar().name == 'Test Account')
        self.assertTrue(self.session.query(Category).filter(Category.id == 3, Category.account_id == 2).scalar().name == 'Expansion')

        self.assertTrue(self.session.query(Transaction).filter(Transaction.id == 12, Transaction.category == 'Expansion',
                                                                Transaction.account_id == 2).scalar().amount == 7.27)
        self.assertTrue(self.session.query(Transaction).filter(Transaction.id == 12, Transaction.category == 'Expansion',
                                                        Transaction.account_id == 2).scalar().description == 'Test Del')
        
        new_transaction.delete_transaction(self.session)

        self.assertTrue(self.session.query(Transaction).filter(Transaction.id == 12, Transaction.category == 'Expansion',
                                                                Transaction.account_id == 2).scalar() == None)

if __name__ == '__main__':
    unittest.main()