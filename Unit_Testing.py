import Account
import unittest
import os
import pandas as pd

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.fresh_account = Account.Account('Michael', [], 0)
    
    def test_initialConditions(self):
        self.assertTrue(self.fresh_account.name == 'Michael')
        self.assertEqual(len(self.fresh_account.transaction_categories), 3)
        self.assertEqual(len(self.fresh_account.transaction_history), 0)
        self.assertEqual(len(self.fresh_account.dataframe), 0)
    
    def test_create_category(self):
        self.fresh_account.create_category('Reserve Funds')
        self.assertTrue('Reserve Funds' in self.fresh_account.transaction_categories)
        self.fresh_account.create_category(120385)
        self.assertFalse(120385 in self.fresh_account.transaction_categories)

    def test_delete_category(self):
        self.fresh_account.create_category('Category For Deletion')
        self.assertTrue('Category For Deletion' in self.fresh_account.transaction_categories)
        self.fresh_account.delete_category('Category For Deletion')
    
    def test_deposit(self):
        self.fresh_account.transaction_deposit(100,'Income')
        self.assertEqual(self.fresh_account.dataframe.iloc[0]['amount'], 100)
        self.assertEqual(self.fresh_account.dataframe.iloc[0]['category'], 'Income')
        self.assertEqual(self.fresh_account.dataframe.iloc[0]['transaction_type'], 'Deposit')

    def test_withdraw(self):
        self.fresh_account.transaction_withdraw(25,'Temporary Loans')
        self.assertEqual(self.fresh_account.dataframe.iloc[0]['amount'], 25)
        self.assertEqual(self.fresh_account.dataframe.iloc[0]['category'], 'Temporary Loans')
        self.assertEqual(self.fresh_account.dataframe.iloc[0]['transaction_type'], 'Withdraw')

    def test_export(self):
        self.fresh_account.transaction_deposit(100,'Income')
        self.fresh_account.export_data('./temp_test.csv')
        self.assertTrue(os.path.exists('./temp_test.csv'))

    def test_import(self):
        self.fresh_account.dataframe = []
        self.assertTrue(type(self.fresh_account.dataframe) == list)
        self.fresh_account.import_data('./temp_test.csv')
        self.assertEqual(self.fresh_account.dataframe.iloc[0]['amount'], 100)
        self.assertEqual(self.fresh_account.dataframe.iloc[0]['category'], 'Income')
        self.assertEqual(self.fresh_account.dataframe.iloc[0]['transaction_type'], 'Deposit')
        os.remove('./temp_test.csv') # Comment this line out if you want to confirm the csv is properly made
    


if __name__ == '__main__':
    unittest.main()