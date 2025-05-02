from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QMessageBox, QComboBox)
from datamodel import User, Account, Transaction, Category
from database import get_session
from datetime import datetime

class ExpensePage(QWidget):
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
        header = QLabel(f"User {self.user.username}'s Add Expense Page")
        self.layout.addWidget(header)

        self.account_combo = QComboBox()
        self.account_combo.activated.connect(self.update_category_display)
        # self.update_accounts_display()
        self.layout.addWidget(self.account_combo)

        add_header = QLabel(f"Add an Expense")
        self.layout.addWidget(add_header)
        #Amount 
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        self.layout.addWidget(self.amount_label)
        self.layout.addWidget(self.amount_input)

        #Category
        self.category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.layout.addWidget(self.category_label)
        self.layout.addWidget(self.category_combo)
        self.update_category_display()

        #Description 
        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)


        self.add_expense_query = QPushButton("Add Expenses")
        self.add_expense_query.clicked.connect(self.add_expense)
        self.layout.addWidget(self.add_expense_query)

        add_header = QLabel(f"Delete an Expense")
        self.layout.addWidget(add_header)

        #ID 
        self.id_label = QLabel("Transaction ID:")
        self.id_input = QLineEdit()
        self.layout.addWidget(self.id_label)
        self.layout.addWidget(self.id_input)

        self.delete_expense_query = QPushButton(f"Delete Expenses")
        self.delete_expense_query.clicked.connect(self.delete_expense)
        self.layout.addWidget(self.delete_expense_query)



        self.create_categories_header = QLabel("Add new category:")
        self.create_categories_label = QLabel("Category Name:")
        self.create_categories_input = QLineEdit()

        self.layout.addWidget(self.create_categories_header)
        self.layout.addWidget(self.create_categories_label)
        self.layout.addWidget(self.create_categories_input)


        self.create_categories_button = QPushButton("Create Category")
        self.create_categories_button.clicked.connect(self.create_category)
        self.layout.addWidget(self.create_categories_button)

        self.delete_categories_label = QLabel(f"Delete category (grabs from categories above):")
        self.layout.addWidget(self.delete_categories_label)

        self.delete_categories_button = QPushButton(f"Delete Category")
        self.delete_categories_button.clicked.connect(self.delete_category)
        self.layout.addWidget(self.delete_categories_button)

        self.home_button = QPushButton('Return to Home')
        self.home_button.clicked.connect(self.open_home)
        self.layout.addWidget(self.home_button)


        self.setLayout(self.layout)

    def add_expense(self):
        # Fetch the account that the dropdown is on right now to create the transaction
        # ID has to be added by 1 because SQL tables are not zero-indexed, while QComboBoxes are
        account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
        new_transaction = Transaction(account_id=account_fetch.id, 
                                      amount=self.amount_input.text(), 
                                      category = account_fetch.select_category(self.session, self.category_combo.currentIndex()).name, 
                                      description=self.description_input.text(),
                                      date=datetime.now())
        # Add operation abstracted to Transaction class
        new_transaction.add_transaction(self.session)

    def delete_expense(self):
        # ID has to be added by 1 because SQL tables are not zero-indexed, while QComboBoxes are
        account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
        transaction = account_fetch.select_transaction(self.session, self.id_input.text())
        if transaction.account_id == account_fetch.id:
            # Delete operation abstracted to Transaction class
            transaction.delete_transaction(self.session)

    def open_home(self):
        self.on_home_click(self.user)
        self.close()

    def create_category(self):
        account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
        new_category = Category(name=self.create_categories_input.text(),
                                 account_id=account_fetch.id)
        new_category.add_category(self.session)
        self.update_category_display()


    def delete_category(self):
        try:
            # account_fetch = self.user.select_account(self.session, self.account_combo.currentIndex())
            # category = account_fetch.select_category(self.session, self.category_combo.currentIndex())
            # category.delete_category(self.session)
            print(self.category_combo.currentIndex())
        except:
            pass
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
    
    def showEvent(self, event):
        # This refreshes our combo boxes whenever we launch or relaunch this window so that the account pages update properly.
        super().showEvent(event)
        self.update_accounts_display()
        self.update_category_display()

    # def clear_window(self):
        





