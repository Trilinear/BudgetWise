from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QMessageBox)
from datamodel import User
from database import get_session

class HomeScreen(QWidget):
    def __init__(self, user, on_account_click, on_expense_click, on_financial_click):
        super().__init__()
        self.user = user
        self.on_account_click = on_account_click
        self.on_expense_click = on_expense_click
        self.on_financial_click = on_financial_click
        self.setup_ui()
        self.session = get_session()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        welcome = QLabel(f"Welcome {self.user.username}!")
        layout.addWidget(welcome)
        
        for account in self.user.accounts:
            acc_label = QLabel(f"ID: {account.id} Name: {account.name} Balance: ${account.balance:.2f}")
            layout.addWidget(acc_label)
        

        self.account_history = QPushButton("Account Page")
        self.account_history.clicked.connect(self.open_account)
        layout.addWidget(self.account_history)

        self.add_expense = QPushButton("Expenses Page")
        self.add_expense.clicked.connect(self.open_expenses)
        layout.addWidget(self.add_expense)

        self.financial_history = QPushButton("Financial History")
        self.financial_history.clicked.connect(self.open_financial)
        layout.addWidget(self.financial_history)
            
        

        self.setLayout(layout)


        
    def open_account(self):
        self.on_account_click(self.user)
        self.close()

    def open_expenses(self):
        self.on_expense_click(self.user)
        self.close()

    def open_financial(self):
        self.on_financial_click(self.user)
        self.close()