from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from datamodel import User

class HomeScreen(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        welcome = QLabel(f"Welcome {self.user.username}!")
        layout.addWidget(welcome)
        
        for account in self.user.accounts:
            acc_label = QLabel(f"{account.name}: ${account.balance:.2f}")
            layout.addWidget(acc_label)
            
        self.setLayout(layout)