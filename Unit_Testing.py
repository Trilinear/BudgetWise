from Driver import Driver
import unittest
import os
import pandas as pd

class TestAccount(unittest.TestCase):
    def setUp(self):
        # if (os.path.exists('test.db') == True):
        #     os.remove('test.db')
        # if (os.path.exists('ext_test.db') == True):
        #     os.remove('ext_test.db')

        # Driver is our base testing, while driver_io is for import/export testing
        self.driver = Driver('./Databases/test.db')
        self.driver_io = Driver('./Databases/ext_test.db')
    
    def test_createAccount(self):
        self.driver.create_account('Michael')
        self.assertTrue(self.driver.read_account(1) == 'Michael')
    
    def test_transactionCreateAndRead(self):
        self.driver.create_transaction(acc_id=1, amt=727.61, category='Paycheck')
        # First set of transactions
        self.assertTrue(self.driver.read_transaction(1, 1).TransactionID == 1)
        self.assertTrue(self.driver.read_transaction(1, 1).AccountID == 1)
        self.assertTrue(self.driver.read_transaction(1, 1).Transaction_Category == 'Paycheck')
        self.assertTrue(self.driver.read_transaction(1, 1).Quantity == 727.61)

        # Second set of transactions
        self.driver.create_transaction(1, 89.61, '401k')
        self.assertTrue(self.driver.read_transaction(1, 2).TransactionID == 2)
        self.assertTrue(self.driver.read_transaction(1, 2).AccountID == 1)
        self.assertTrue(self.driver.read_transaction(1, 2).Transaction_Category == '401k')
        self.assertTrue(self.driver.read_transaction(1, 2).Quantity == 89.61)

    def test_transactionDelete(self):
        # Delete Test
        self.driver.create_transaction(1, 123.84, 'Groceries')
        self.driver.delete_transaction(1, 3)
        self.assertEqual(self.driver.read_transaction(1, 3), 'No result found')

        # Confirm other transaction is not broken from delete
        self.assertTrue(self.driver.read_transaction(1, 1).TransactionID == 1)
        self.assertTrue(self.driver.read_transaction(1, 1).AccountID == 1)
        self.assertTrue(self.driver.read_transaction(1, 1).Transaction_Category == 'Paycheck')
        self.assertTrue(self.driver.read_transaction(1, 1).Quantity == 727.61)

    def test_export_import(self):
        self.driver_io.create_account('Michael')
        self.driver_io.create_transaction(1, 727.61, 'Paycheck')
        self.driver_io.create_transaction(1, 123.84, 'Groceries')
        self.driver_io.create_transaction(1, 89.61, '401k')
        self.driver_io.export_accounts('./acc_test.csv')
        self.driver_io.export_transactions('./transaction_test.csv')
        self.assertTrue(os.path.exists('./acc_test.csv'))
        self.assertTrue(os.path.exists('./transaction_test.csv'))

        self.driver_io.import_accounts('./acc_test.csv')
        self.driver_io.import_transactions('./transaction_test.csv')
        self.assertTrue(self.driver_io.read_account(1) == 'Michael')
        self.assertTrue(self.driver_io.read_transaction(1, 1).TransactionID == 1)
        self.assertTrue(self.driver_io.read_transaction(1, 1).AccountID == 1)
        self.assertTrue(self.driver_io.read_transaction(1, 1).Transaction_Category == 'Paycheck')
        self.assertTrue(self.driver_io.read_transaction(1, 1).Quantity == 727.61)

        os.remove('./acc_test.csv') # Comment these lines out if you want to confirm the csv is properly made
        os.remove('./transaction_test.csv')

    


if __name__ == '__main__':
    unittest.main()