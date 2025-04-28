# register.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont
from database import get_session
from datamodel import User, Account

class RegisterScreen(QWidget):
    def __init__(self, on_back_to_login, on_registration_success):
        super().__init__()
        self.on_back_to_login = on_back_to_login
        self.on_registration_success = on_registration_success
        self.session = get_session()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("BudgetWise - Register")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            background-color: #378805;
            color: white;
        """)

        layout = QVBoxLayout()

        #Username
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        #Password
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        #Confirm Password
        self.confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)

        button_layout = QHBoxLayout()

        #Register Button
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #2a6e04;
                color: white;
                border: none;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #3a8e14;
            }
        """)
        button_layout.addWidget(self.register_button)

        #Back to Login Button
        self.back_button = QPushButton("Back to Login")
        self.back_button.clicked.connect(self.on_back_to_login)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #6e2a04;
                color: white;
                border: none;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #8e3a14;
            }
        """)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)

        font = QFont("Arial", 10)
        self.setFont(font)
        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords don't match!")
            return

        existing_user = self.session.query(User).filter_by(username=username).first()
        if existing_user:
            QMessageBox.warning(self, "Error", "Username already exists!")
            return

        try:
            new_user = User(username=username, password=password)  
            new_account = Account(name=f"{username}'s Account", balance=0.0, user=new_user)
            self.session.add_all([new_user, new_account])
            self.session.commit()
            
            QMessageBox.information(self, "Success", "Registration successful!")
            self.on_registration_success(new_user)
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")