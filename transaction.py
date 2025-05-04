from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QMessageBox, QComboBox)
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
        self.setStyleSheet("""
            background-color: #378805;
            color: white;
        """)

        self.layout = QVBoxLayout()
        header = QLabel(f"User {self.user.username}'s Transaction Page")
        self.layout.addWidget(header)

        self.account_combo = QComboBox()
        self.account_combo.activated.connect(self.update_category_display)
        self.layout.addWidget(self.account_combo)

        add_header = QLabel(f"Add a Transaction")
        self.layout.addWidget(add_header)
        #Amount 
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        self.layout.addWidget(self.amount_label)
        self.layout.addWidget(self.amount_input)

        #Category
        self.category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.category_combo.activated.connect(self.update_transactions_display)
        self.layout.addWidget(self.category_label)
        self.layout.addWidget(self.category_combo)

        #Description 
        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)


        self.add_income_button = QPushButton("Add as Income")
        self.add_income_button.clicked.connect(self.add_income)
        self.layout.addWidget(self.add_income_button)

        self.add_expense_button = QPushButton("Add as Expense")
        self.add_expense_button.clicked.connect(self.add_expense)
        self.layout.addWidget(self.add_expense_button)

        add_header = QLabel(f"Delete a Transaction")
        self.layout.addWidget(add_header)

        # Transaction Combo
        self.transaction_label = QLabel("Transactions to delete from:")
        self.transaction_combo = QComboBox()
        self.layout.addWidget(self.transaction_label)
        self.layout.addWidget(self.transaction_combo)

        self.delete_transaction_query = QPushButton(f"Delete Transaction")
        self.delete_transaction_query.clicked.connect(self.delete_transaction)
        self.layout.addWidget(self.delete_transaction_query)



        self.create_categories_header = QLabel("Add New Category:")
        self.create_categories_label = QLabel("Category Name:")
        self.create_categories_input = QLineEdit()

        self.layout.addWidget(self.create_categories_header)
        self.layout.addWidget(self.create_categories_label)
        self.layout.addWidget(self.create_categories_input)


        self.create_categories_button = QPushButton("Create Category")
        self.create_categories_button.clicked.connect(self.create_category)
        self.layout.addWidget(self.create_categories_button)

        self.delete_categories_label = QLabel(f"Delete Category (grabs from categories above):")
        self.layout.addWidget(self.delete_categories_label)

        self.delete_categories_button = QPushButton(f"Delete Category")
        self.delete_categories_button.clicked.connect(self.delete_category)
        self.layout.addWidget(self.delete_categories_button)

        self.home_button = QPushButton('Return to Home')
        self.home_button.clicked.connect(self.open_home)
        self.layout.addWidget(self.home_button)


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
        except:
            QMessageBox.critical(self, "Error", "An unusual error has occured!")
        finally:
            self.update_category_display()

    def update_category_display(self):
        category_names = list()
        account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
        categories = account_fetch.get_all_categories(self.session)
        self.category_combo.clear()
        for category in categories:
            category_names.append(category.name)
        self.category_combo.insertItems(0, category_names)
        
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
        





