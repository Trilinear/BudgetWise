from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QMessageBox, QComboBox)
from datamodel import User, Account, Transaction
from database import get_session
from datetime import datetime

class ExpensePage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setup_ui()
        self.session = get_session()

    def setup_ui(self):
        layout = QVBoxLayout()
        header = QLabel(f"User {self.user.username}'s Add Expense Page")
        layout.addWidget(header)

        self.account_combo = QComboBox()
        for account in self.user.accounts:
            self.account_combo.addItem(account.name)
        layout.addWidget(self.account_combo)

        add_header = QLabel(f"Add an Expense")
        layout.addWidget(add_header)
        #Amount 
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)

        #Category 
        self.category_label = QLabel("Category:")
        self.category_input = QLineEdit()
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)


        self.add_expense_query = QPushButton("Add Expenses")
        self.add_expense_query.clicked.connect(self.add_expense)
        layout.addWidget(self.add_expense_query)

        add_header = QLabel(f"Delete an Expense")
        layout.addWidget(add_header)

        #ID 
        self.id_label = QLabel("Transaction ID:")
        self.id_input = QLineEdit()
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)

        self.delete_expense_query = QPushButton(f"Delete Expenses")
        self.delete_expense_query.clicked.connect(self.delete_expense)
        layout.addWidget(self.delete_expense_query)

        self.setLayout(layout)

    def add_expense(self):
        # Fetch the account that the dropdown is on right now to create the transaction
        account_fetch = self.session.query(Account).filter(Account.id == self.user.accounts[self.account_combo.currentIndex()].id).scalar()
        new_transaction = Transaction(account_id=account_fetch.id, amount=self.amount_input.text(), 
                                    description=self.category_input.text(), date=datetime.now())
        # Add operation abstracted to Transaction class
        new_transaction.add_transaction(self.session)

    def delete_expense(self):
        account_fetch = self.session.query(Account).filter(Account.id == self.user.accounts[self.account_combo.currentIndex()].id).scalar()
        transaction = self.session.query(Transaction).filter(Transaction.id == self.id_input.text()).scalar()
        if transaction.account_id == account_fetch.id:
            # Delete operation abstracted to Transaction class
            transaction.delete_transaction(self.session)