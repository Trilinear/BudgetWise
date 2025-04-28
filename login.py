from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QFont
from database import get_session
from datamodel import User

class LoginScreen(QWidget):
    def __init__(self, on_login_success, on_register):
        super().__init__()
        self.on_login_success = on_login_success
        self.on_register = on_register
        self.session = get_session()
        self.setup_ui()
        
    def setup_ui(self):
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

        #Login 
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.on_register)
        self.register_button.setStyleSheet("""
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
        layout.addWidget(self.register_button)

        font = QFont("Arial", 10)
        self.setFont(font)
        self.setLayout(layout)
        
    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        user = self.session.query(User).filter_by(
            username=username, 
            password=password  
        ).first()
        
        if user:
            self.on_login_success(user)
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")