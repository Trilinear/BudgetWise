from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                            QPushButton, QGridLayout, QMessageBox, QComboBox)
from datamodel import User, Account, Transaction, Category
from database import get_session
from datetime import datetime

class TransactionPage(QWidget):
    def __init__(self, user, on_home_click):
        super().__init__()
        self.user = user
        self.on_home_click = on_home_click
        self.session = get_session()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 600, 400)
        # self.setStyleSheet("""
        #     background-color: #378805;
        #     color: white;
        # """)

        self.layout = QGridLayout()
        self.layout.setHorizontalSpacing(50)
        header = QLabel(f"User {self.user.username}'s Transaction Page")
        self.layout.addWidget(header, 0, 0)

        self.account_combo = QComboBox()
        self.account_combo.activated.connect(self.update_category_display)
        self.layout.addWidget(self.account_combo, 0, 1)

        add_header = QLabel(f"Add a Transaction")
        self.layout.addWidget(add_header, 1, 0)
        #Amount 
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        self.layout.addWidget(self.amount_label, 2, 0)
        self.layout.addWidget(self.amount_input, 3, 0)

        #Category
        self.category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.category_combo.activated.connect(self.update_transactions_display)
        self.layout.addWidget(self.category_label, 4, 0)
        self.layout.addWidget(self.category_combo, 5, 0)

        #Description 
        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        self.layout.addWidget(self.description_label, 6, 0)
        self.layout.addWidget(self.description_input, 7, 0)


        self.add_income_button = QPushButton("Add as Income")
        self.add_income_button.clicked.connect(self.add_income)
        self.layout.addWidget(self.add_income_button, 8, 0)

        self.add_expense_button = QPushButton("Add as Expense")
        self.add_expense_button.clicked.connect(self.add_expense)
        self.layout.addWidget(self.add_expense_button, 9, 0)


        # Edit/Delete Transactions Column
        edit_header = QLabel(f"Edit Existing Transaction")
        self.transaction_label = QLabel(f"Select Transaction to Edit:")
        self.transaction_combo = QComboBox()
        self.delete_transaction_button = QPushButton(f"Delete Transaction")
        self.delete_transaction_button.clicked.connect(self.delete_transaction)

        self.edit_amount_label = QLabel('Edit Amount')
        self.edit_amount = QLineEdit()
        self.edit_description_label = QLabel('Edit Description')
        self.edit_description = QLineEdit()
        self.edit_category_label = QLabel('Edit Category')
        self.edit_category_combo = QComboBox()

        self.edit_transaction_button = QPushButton("Change Transaction")
        self.edit_transaction_button.clicked.connect(self.update_transaction)

        self.layout.addWidget(edit_header, 1, 1)
        self.layout.addWidget(self.transaction_label, 2, 1)
        self.layout.addWidget(self.transaction_combo, 3, 1)
        self.layout.addWidget(self.delete_transaction_button, 4, 1)

        self.layout.addWidget(self.edit_amount_label, 5, 1)
        self.layout.addWidget(self.edit_amount, 6, 1)
        self.layout.addWidget(self.edit_description_label, 7, 1)
        self.layout.addWidget(self.edit_description, 8, 1)
        self.layout.addWidget(self.edit_category_label, 9, 1)
        self.layout.addWidget(self.edit_category_combo, 10, 1)

        self.layout.addWidget(self.edit_transaction_button, 11, 1)


        # Categories Column
        self.create_categories_header = QLabel("Add New Category:")
        self.create_categories_label = QLabel("Category Name:")
        self.create_categories_input = QLineEdit()

        self.layout.addWidget(self.create_categories_header, 1, 2)
        self.layout.addWidget(self.create_categories_label, 2, 2)
        self.layout.addWidget(self.create_categories_input, 3, 2)


        self.create_categories_button = QPushButton("Create Category")
        self.create_categories_button.clicked.connect(self.create_category)
        self.layout.addWidget(self.create_categories_button, 4, 2)

        self.delete_categories_label = QLabel(f"Delete Category (grabs from categories above):")
        self.layout.addWidget(self.delete_categories_label, 5, 2)

        self.delete_categories_button = QPushButton(f"Delete Category")
        self.delete_categories_button.clicked.connect(self.delete_category)
        self.layout.addWidget(self.delete_categories_button, 6, 2)

        self.home_button = QPushButton('Return to Home')
        self.home_button.clicked.connect(self.open_home)
        self.layout.addWidget(self.home_button, 10, 2)


        self.setLayout(self.layout)

    def add_income(self):
        try:
            # Fetch the account that the dropdown is on right now to create the transaction
            # ID has to be added by 1 because SQL tables are not zero-indexed, while QComboBoxes are
            account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
            new_transaction = Transaction(account_id=account_fetch.id, 
                                        amount=float(self.amount_input.text()), 
                                        category = account_fetch.select_category(self.session, self.category_combo.currentIndex()).name, 
                                        description=self.description_input.text(),
                                        date=datetime.now())
            # Add operation abstracted to Transaction class
            add_flag = new_transaction.add_transaction(self.session)
            new_balance = account_fetch.balance + float(self.amount_input.text())
            account_fetch.update_balance(self.session, new_balance)
            if add_flag == 0:
                QMessageBox.information(self, "Success", "Transaction creation was successful!")
            else:
                QMessageBox.critical(self, "Error", "An error occured during creation!")
        except ValueError:
            QMessageBox.critical(self, "Error", "Amount must be a number!")
        except:
            QMessageBox.critical(self, "Error", "An unusual error occured!")
        finally:
            self.update_transactions_display()


    def add_expense(self):
        account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
        try:
            new_transaction = Transaction(account_id=account_fetch.id, 
                                        amount= -float(self.amount_input.text()), # Same as add_income but inverted amount so that balance is added as an expense
                                        category = account_fetch.select_category(self.session, self.category_combo.currentIndex()).name, 
                                        description=self.description_input.text(),
                                        date=datetime.now())
            # Add operation abstracted to Transaction class
            add_flag = new_transaction.add_transaction(self.session)
            new_balance = account_fetch.balance - float(self.amount_input.text())
            account_fetch.update_balance(self.session, new_balance)
            if add_flag == 0:
                QMessageBox.information(self, "Success", "Transaction creation was successful!")
            else:
                QMessageBox.critical(self, "Error", "An error occured during creation!")
        except ValueError:
            QMessageBox.critical(self, "Error", "Amount must be a number!")
        except:
            QMessageBox.critical(self, "Error", "An unusual error occured!")
        finally:
            self.update_transactions_display()

    def update_transaction(self):
        try:
            net_change = 0.0
            account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
            transactions = account_fetch.select_transactions_by_category(self.session, self.category_combo.currentIndex())
            transaction = transactions[self.transaction_combo.currentIndex()]
            # For when user inputs a change in amount
            if self.edit_amount.text() != "":
                # For updating account balance after update
                if transaction.amount > float(self.edit_amount.text()):
                    net_change = float(self.edit_amount.text()) - transaction.amount
                    print(net_change)
                elif transaction.amount < float(self.edit_amount.text()):
                    net_change = float(self.edit_amount.text()) - transaction.amount
                transaction.amount = float(self.edit_amount.text())

            # For when user inputs a change in description
            if self.edit_description.text() != "":
                transaction.description = self.edit_description.text()
            
            # For when user inputs a change in category, always runs because its a ComboBox
            transaction.category = self.edit_category_combo.currentText()
            update_flag = transaction.update_transaction(self.session)
            if update_flag == 0:
                QMessageBox.information(self, "Success", "Transaction update was successful!")
            else:
                # Revert net_change back to 0.0 if an error occurs so we don't put a bad update
                net_change = 0.0
                QMessageBox.critical(self, "Error", "An error occured during update!")
            
            # Update the balance after everything is done
            if net_change != 0.0:
                new_balance = account_fetch.balance + net_change
                account_fetch.update_balance(self.session, new_balance)

        except ValueError:
            QMessageBox.critical(self, "Error", "Amount must be a number!")
        except:
            QMessageBox.critical(self, "Error", "An unusual error occured!")
        finally:
            self.update_category_display()
            self.update_transactions_display()


    def delete_transaction(self):
        try:
            # ID has to be added by 1 because SQL tables are not zero-indexed, while QComboBoxes are
            account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
            transactions = account_fetch.select_transactions_by_category(self.session, self.category_combo.currentIndex())
            transaction = transactions[self.transaction_combo.currentIndex()]
            if transaction.account_id == account_fetch.id:
                # Delete operation abstracted to Transaction class
                delete_flag = transaction.delete_transaction(self.session)
                if delete_flag == 0:
                    QMessageBox.information(self, "Success", "Transaction deletion was successful!")
                else:
                    QMessageBox.critical(self, "Error", "An error occured during deletion!")
                self.update_transactions_display()
            new_balance = account_fetch.balance - transaction.amount
            account_fetch.update_balance(self.session, new_balance)
        except:
            QMessageBox.critical(self, "Error", "An unusual error occured!")
        finally:
            self.update_transactions_display()


    def open_home(self):
        self.on_home_click(self.user)
        self.close()

    def create_category(self):
        try:
            account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
            new_category = Category(name=self.create_categories_input.text(),
                                    account_id=account_fetch.id)
            add_flag = new_category.add_category(self.session)
            if add_flag == 0:
                QMessageBox.information(self, "Success", "Transaction creation was successful!")
            else:
                QMessageBox.critical(self, "Error", "An error occured during creation!")
        except:
            QMessageBox.critical(self, "Error", "An unusual error occured!")
        finally:
            self.update_category_display()


    def delete_category(self):
        try:
            account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
            category = account_fetch.select_category(self.session, self.category_combo.currentIndex())
            delete_flag = category.delete_category(self.session)
            if delete_flag == 0:
                QMessageBox.information(self, "Success", "Category deletion was successful!")
            else:
                QMessageBox.critical(self, "Error", "An error occured during deletion!")
            new_balance = 0.0
            transactions = account_fetch.get_all_transactions(self.session)
            for transaction in transactions:
                new_balance = new_balance + transaction.amount
            account_fetch.update_balance(self.session, new_balance)
        except:
            QMessageBox.critical(self, "Error", "An unusual error has occured!")
        finally:
            self.update_category_display()

    def update_category_display(self):
        category_names = list()
        account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
        categories = account_fetch.get_all_categories(self.session)
        self.category_combo.clear()
        self.edit_category_combo.clear()
        for category in categories:
            category_names.append(category.name)
        self.category_combo.insertItems(0, category_names)
        self.edit_category_combo.insertItems(0, category_names)
        
    def update_accounts_display(self):
        self.account_combo.clear()
        accounts = self.user.get_all_accounts(self.session)
        for account in accounts:
            self.account_combo.addItem(account.name)

    def update_transactions_display(self):
        account = self.user.select_account(self.session, self.account_combo.currentIndex())
        transactions = account.select_transactions_by_category(self.session, self.category_combo.currentIndex())
        self.transaction_combo.clear()
        for transaction in transactions:
            self.transaction_combo.addItem(f'ID {transaction.id}: {transaction.amount}')
        
        
        
    
    def showEvent(self, event):
        # This refreshes our combo boxes whenever we launch or relaunch this window so that the account pages update properly.
        super().showEvent(event)
        self.update_accounts_display()
        self.update_category_display()
        self.update_transactions_display()

    # def clear_window(self):
        





