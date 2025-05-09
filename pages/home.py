from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QMessageBox)
from controller.datamodel import User
from controller.database import get_session
from PyQt5.QtCore import Qt

class HomeScreen(QWidget):
    def __init__(self, user, on_account_click, on_transaction_click, on_financial_click):
        super().__init__()
        self.user = user
        self.acc_list = list()
        self.on_account_click = on_account_click
        self.on_transaction_click = on_transaction_click
        self.on_financial_click = on_financial_click
        self.layout = QVBoxLayout()
        self.session = get_session()
        self.setup_ui()
        
    def setup_ui(self):
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #378805;
                color: white;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
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
        """)

        
        self.welcome = QLabel(f"Welcome to BudgetWise {self.user.username}!")
        self.welcome.setObjectName("titleLabel")
        self.welcome.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.welcome)
        
        accounts = self.user.get_all_accounts(self.session)

        for account in accounts:
            acc_label = QLabel(f"ID: {account.id} Name: {account.name} Balance: ${account.balance:.2f}")
            self.layout.addWidget(acc_label)
            self.acc_list.append(acc_label)

        self.account_history = QPushButton("Account Page")
        self.account_history.clicked.connect(self.open_account)
        self.layout.addWidget(self.account_history)

        self.add_tranasction = QPushButton("Transactions Page")
        self.add_tranasction.clicked.connect(self.open_transactions)
        self.layout.addWidget(self.add_tranasction)

        self.financial_history = QPushButton("Financial History")
        self.financial_history.clicked.connect(self.open_financial)
        self.layout.addWidget(self.financial_history)
        self.setLayout(self.layout)


        
    def open_account(self):
        self.on_account_click(self.user)
        self.close()

    def open_transactions(self):
        self.on_transaction_click(self.user)
        self.close()

    def open_financial(self):
        self.on_financial_click(self.user)
        self.close()

    def update_window(self):
        self.layout.removeWidget(self.welcome)
        for widget in self.acc_list:
            self.layout.removeWidget(widget)
        self.acc_list = list()
        self.layout.removeWidget(self.account_history)
        self.layout.removeWidget(self.add_tranasction)
        self.layout.removeWidget(self.financial_history)
        self.setup_ui()



    def showEvent(self, event):
        # This refreshes our combo boxes whenever we launch or relaunch this window so that the account pages update properly.
        super().showEvent(event)
        self.update_window()