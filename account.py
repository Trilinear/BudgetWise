from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QMessageBox, QComboBox)
from datamodel import User, Account, Transaction
from database import get_session
from PyQt5.QtCore import Qt

class AccountPage(QWidget):
    def __init__(self, user, on_home_click):
        super().__init__()
        self.user = user
        self.session = get_session()
        self.on_home_click = on_home_click
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #378805;
                color: white;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel#headerTitle {
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
        """)

        layout = QVBoxLayout()

        # Title
        self.header = QLabel("Accounts")
        self.header.setObjectName("headerTitle")
        self.header.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.header)

        # --- Add Account Section ---
        self.add_header = QLabel("Add an Account")
        self.add_header.setObjectName("addAccount")
        self.add_header.setProperty("class", "sectionHeader")
        layout.addWidget(self.add_header)

        self.name_label = QLabel("Name of new account:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.add_account_button = QPushButton("Add Account")
        self.add_account_button.clicked.connect(self.create_account)
        layout.addWidget(self.add_account_button)

        # --- Edit/Delete Section ---
        self.edit_delete_header = QLabel("Edit/Delete an Account")
        self.edit_delete_header.setProperty("class", "sectionHeader")
        layout.addWidget(self.edit_delete_header)

        self.account_label = QLabel("Select account to be edited/deleted:")
        self.account_combo = QComboBox()
        layout.addWidget(self.account_label)
        layout.addWidget(self.account_combo)

        self.edit_name_label = QLabel("New Name:")
        self.edit_name = QLineEdit()
        layout.addWidget(self.edit_name_label)
        layout.addWidget(self.edit_name)

        self.edit_account_button = QPushButton("Edit Account")
        self.edit_account_button.clicked.connect(self.edit_account)
        layout.addWidget(self.edit_account_button)

        self.delete_account_button = QPushButton("Delete Account")
        self.delete_account_button.clicked.connect(self.remove_account)
        layout.addWidget(self.delete_account_button)

        # --- Navigation ---
        self.home_button = QPushButton("Return to Home")
        self.home_button.clicked.connect(self.open_home)
        layout.addWidget(self.home_button)

        self.setLayout(layout)


    
    def create_account(self):
        try:
            new_account = Account(user_id=self.user.id, 
                name=self.name_input.text(),
                balance=0.0
            )
            # Add operation abstracted to Account class
            add_flag = new_account.add_account(self.session)
            if add_flag == 0:
                QMessageBox.information(self, "Success", "Account creation was successful!")
            else:
                QMessageBox.critical(self, "Error", "An error occurred during creation!")
        except:
            QMessageBox.critical(self, "Error", "An unusual error occurred!")
        finally:
            self.update_accounts_combo()
        
    def edit_account(self):
        try:
            account_query = self.user.select_account(self.session, self.account_combo.currentIndex())
            if self.edit_name.text() != '':
                account_query.name = self.edit_name.text()
            update_flag = account_query.update_name(self.session)
            if update_flag == 0:
                QMessageBox.information(self, "Success", "Account update was successful!")
            else:
                QMessageBox.critical(self, "Error", "An error occurred during update!")
        except:
            QMessageBox.critical(self, "Error", "An unusual error occurred!")
        finally:
            self.update_accounts_combo()


    def remove_account(self):
        try:
            account = self.user.select_account(self.session, self.account_combo.currentIndex())
            delete_flag = account.delete_account(self.session)
            if delete_flag == 0:
                QMessageBox.information(self, "Success", "Account delete was successful!")
            else:
                QMessageBox.critical(self, "Error", "An error occurred during deletion!")
        except:
            QMessageBox.critical(self, "Error", "An unusual error occurred!")
        finally:
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
        self.update_accounts_combo()
