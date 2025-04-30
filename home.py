from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QMessageBox)
from datamodel import User
from expense import ExpensePage
from financial import FinancialHistory
from database import get_session

class HomeScreen(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.current_window = None
        self.setup_ui()
        self.session = get_session()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        welcome = QLabel(f"Welcome {self.user.username}!")
        layout.addWidget(welcome)
        
        for account in self.user.accounts:
            acc_label = QLabel(f"{account.name}: ${account.balance:.2f}")
            layout.addWidget(acc_label)
        
        self.add_expense = QPushButton("Add Expenses")
        self.add_expense.clicked.connect(self.show_expense)
        layout.addWidget(self.add_expense)

        self.financial_history = QPushButton("Financial History")
        self.financial_history.clicked.connect(self.show_financial_history)
        layout.addWidget(self.financial_history)
            
        self.setLayout(layout)


    def show_expense(self):
        if self.current_window:
            self.current_window.close()
        self.current_window = ExpensePage(self.user)
        self.current_window.show()

    def show_financial_history(self):
        if self.current_window:
            self.current_window.close()
        self.current_window = FinancialHistory(self.user)
        self.current_window.show()

        