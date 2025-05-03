from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QMessageBox, QComboBox)
from datamodel import User, Account, Transaction
from database import get_session

class AccountPage(QWidget):
    def __init__(self, user, on_home_click):
        super().__init__()
        self.user = user
        self.session = get_session()
        self.on_home_click = on_home_click
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            background-color: #378805;
            color: white;
        """)

        layout = QVBoxLayout()
        header = QLabel(f"User {self.user.username}'s Account Page")
        layout.addWidget(header)

        add_header = QLabel(f"Add an Account")
        layout.addWidget(add_header)

        #name 
        self.name_label = QLabel("Name of new account:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)


        self.add_account_button = QPushButton("Add Account")
        self.add_account_button.clicked.connect(self.create_account)
        layout.addWidget(self.add_account_button)

        delete_header = QLabel(f"Delete an Account")
        layout.addWidget(delete_header)

        self.id_label = QLabel(f"Select account to be deleted:")
        self.account_combo = QComboBox()
        layout.addWidget(self.account_combo)

        self.add_account_button = QPushButton(f"Delete Account")
        self.add_account_button.clicked.connect(self.remove_account)
        layout.addWidget(self.add_account_button)

        self.home_button = QPushButton('Return to Home')
        self.home_button.clicked.connect(self.open_home)
        layout.addWidget(self.home_button)

        self.setLayout(layout)


    
    def create_account(self):
        new_account = Account(user_id=self.user.id, 
            name=self.name_input.text(),
            balance=0.0
        )
        # Add operation abstracted to Account class
        new_account.add_account(self.session)
        self.update_accounts_combo()
        

    def remove_account(self):
        account = self.user.select_account(self.session, self.account_combo.currentIndex())
        account.delete_account(self.session)
        self.update_accounts_combo()

    def open_home(self):
        self.on_home_click(self.user)
        self.close()

    def update_accounts_combo(self):
        self.account_combo.clear()
        accounts = self.user.get_all_accounts(self.session)
        for account in accounts:
            self.account_combo.addItem(account.name)

    def showEvent(self, event):
        # This refreshes our combo boxes whenever we launch or relaunch this window so that the account pages update properly.
        super().showEvent(event)
        print('update')
        self.update_accounts_combo()
