from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                            QPushButton, QGridLayout, QMessageBox, QComboBox, QListWidget, QDateEdit)
from datamodel import User, Account, Transaction, Category
from database import get_session
from datetime import datetime
from PyQt5.QtCore import Qt, QDate

class TransactionPage(QWidget):
    def __init__(self, user, on_home_click):
        super().__init__()
        self.user = user
        self.on_home_click = on_home_click
        self.session = get_session()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #378805;
                color: white;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel#mainHeader {
                font-size: 22px;
                font-weight: bold;
            }
            QLabel.sectionHeader {
                font-size: 16px;
                font-weight: bold;
                margin-top: 15px;
                margin-bottom: 5px;
            }
            QPushButton {
                background-color: #dcdcdc;
                color: black;
                border-radius: 5px;
                padding: 8px 12px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
            QLineEdit, QComboBox {
                background-color: white;
                color: black;
                padding: 4px;
                border-radius: 4px;
            }
            QListWidget {
                background-color: white;  /* White background */
                color: black;           /* Dark gray text */
            }
        """)

        self.layout = QGridLayout()
        self.layout.setHorizontalSpacing(50)
        self.layout.setVerticalSpacing(10)

        # --- Header ---
        header = QLabel("Transactions")
        header.setObjectName("mainHeader")
        header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header, 0, 0, 1, 3)

        # --- Account ComboBox ---
        self.account_combo = QComboBox()
        self.account_combo.activated.connect(self.update_category_display)
        self.layout.addWidget(self.account_combo, 1, 0)

        # === Column 1: Add Transaction ===
        add_header = QLabel("Add a Transaction")
        add_header.setProperty("class", "sectionHeader")
        self.layout.addWidget(add_header, 2, 0)

        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        self.layout.addWidget(self.amount_label, 3, 0)
        self.layout.addWidget(self.amount_input, 4, 0)

        self.category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.category_combo.activated.connect(self.update_transactions_display)
        self.layout.addWidget(self.category_label, 5, 0)
        self.layout.addWidget(self.category_combo, 6, 0)

        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        self.layout.addWidget(self.description_label, 7, 0)
        self.layout.addWidget(self.description_input, 8, 0)

        self.date_label = QLabel("Date:")
        self.date_input = QDateEdit()
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setDate(datetime.now().date())  
        self.date_input.setCalendarPopup(True)  
        self.layout.addWidget(self.date_label, 9, 0) 
        self.layout.addWidget(self.date_input, 10, 0)

        self.add_income_button = QPushButton("Add as Income")
        self.add_income_button.clicked.connect(self.add_income)
        self.layout.addWidget(self.add_income_button, 11, 0)

        self.add_expense_button = QPushButton("Add as Expense")
        self.add_expense_button.clicked.connect(self.add_expense)
        self.layout.addWidget(self.add_expense_button, 12, 0)

        # === Column 2: Edit/Delete Transaction ===
        edit_header = QLabel("Edit Existing Transaction")
        edit_header.setProperty("class", "sectionHeader")
        self.layout.addWidget(edit_header, 2, 1)

        self.transaction_label = QLabel("Select Transaction to Edit:")
        self.transaction_combo = QComboBox()
        self.layout.addWidget(self.transaction_label, 3, 1)
        self.layout.addWidget(self.transaction_combo, 4, 1)

        self.delete_transaction_button = QPushButton("Delete Transaction")
        self.delete_transaction_button.clicked.connect(self.delete_transaction)
        self.layout.addWidget(self.delete_transaction_button, 5, 1)

        self.edit_amount_label = QLabel("Edit Amount:")
        self.edit_amount = QLineEdit()
        self.layout.addWidget(self.edit_amount_label, 6, 1)
        self.layout.addWidget(self.edit_amount, 7, 1)

        self.edit_description_label = QLabel("Edit Description:")
        self.edit_description = QLineEdit()
        self.layout.addWidget(self.edit_description_label, 8, 1)
        self.layout.addWidget(self.edit_description, 9, 1)

        self.edit_category_label = QLabel("Change Category:")
        self.edit_category_combo = QComboBox()
        self.layout.addWidget(self.edit_category_label, 10, 1)
        self.layout.addWidget(self.edit_category_combo, 11, 1)

        self.edit_transaction_button = QPushButton("Change Transaction")
        self.edit_transaction_button.clicked.connect(self.update_transaction)
        self.layout.addWidget(self.edit_transaction_button, 12, 1)

        # === Column 3: Categories ==
        self.create_categories_header = QLabel("Add New Category")
        self.create_categories_header.setProperty("class", "sectionHeader")
        self.layout.addWidget(self.create_categories_header, 2, 2)

        self.categories = QLabel("Existing Categories")
        self.layout.addWidget(self.categories, 3, 2)
        self.categories_list = QListWidget()
        self.layout.addWidget(self.categories_list, 4, 2)

        self.create_categories_label = QLabel("Category Name:")
        self.create_categories_input = QLineEdit()
        self.layout.addWidget(self.create_categories_label, 5, 2)
        self.layout.addWidget(self.create_categories_input, 6, 2)

        self.create_categories_button = QPushButton("Create Category")
        self.create_categories_button.clicked.connect(self.create_category)
        self.layout.addWidget(self.create_categories_button, 7, 2)

        self.delete_category_combo = QComboBox()
        self.layout.addWidget(QLabel("Select Category to Delete:"), 8, 2)  
        self.layout.addWidget(self.delete_category_combo, 9, 2)

        self.delete_categories_button = QPushButton("Delete Category")
        self.delete_categories_button.clicked.connect(self.delete_category)
        self.layout.addWidget(self.delete_categories_button, 10, 2)

        self.home_button = QPushButton("Return to Home")
        self.home_button.clicked.connect(self.open_home)
        self.layout.addWidget(self.home_button, 11, 2)

        self.setLayout(self.layout)

    def add_income(self):
        try:
            selected_date = self.date_input.date()
            transaction_date = datetime(
                selected_date.year(),
                selected_date.month(),
                selected_date.day()
            )
            # Fetch the account that the dropdown is on right now to create the transaction
            # ID has to be added by 1 because SQL tables are not zero-indexed, while QComboBoxes are
            account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
            new_transaction = Transaction(account_id=account_fetch.id, 
                                        amount=float(self.amount_input.text()), 
                                        category = account_fetch.select_category(self.session, self.category_combo.currentIndex()).name, 
                                        description=self.description_input.text(),
                                        date=transaction_date)
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
            selected_date = self.date_input.date()
            transaction_date = datetime(
                selected_date.year(),
                selected_date.month(),
                selected_date.day()
            )
            new_transaction = Transaction(account_id=account_fetch.id, 
                                        amount= -float(self.amount_input.text()), # Same as add_income but inverted amount so that balance is added as an expense
                                        category = account_fetch.select_category(self.session, self.category_combo.currentIndex()).name, 
                                        description=self.description_input.text(),
                                        date=transaction_date)
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
            category = account_fetch.select_category(self.session, self.delete_category_combo.currentIndex())
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
        
        # Update combo boxes
        self.category_combo.clear()
        self.edit_category_combo.clear()
        self.delete_category_combo.clear()
        
        # Update categories list widget
        self.categories_list.clear()
        
        for category in categories:
            category_names.append(category.name)
            self.categories_list.addItem(category.name)
            
        self.category_combo.insertItems(0, category_names)
        self.edit_category_combo.insertItems(0, category_names)
        self.delete_category_combo.insertItems(0, category_names)
        
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

        





