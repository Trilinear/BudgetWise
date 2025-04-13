import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QFileDialog, QMessageBox
)
from Account import Account


class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BudgetWise - Home")

        #Sample account
        self.account = Account("Sample", [], 0.0)

        self.layout = QVBoxLayout()

        #Welcome Label
        self.label_welcome = QLabel(f"Welcome to BudgetWise, {self.account.name}!")
        self.layout.addWidget(self.label_welcome)

        #Account Balance
        self.label_balance = QLabel(f"Account Balance: ${self.account.account_balance:.2f}")
        self.layout.addWidget(self.label_balance)

        #Buttons
        self.btn_deposit = QPushButton("Add Deposit")
        self.btn_withdraw = QPushButton("Add Withdrawal")
        self.btn_view = QPushButton("View Transactions")
        self.btn_export = QPushButton("Export CSV")
        self.btn_import = QPushButton("Import CSV")
        self.btn_quit = QPushButton("Quit")

        self.layout.addWidget(self.btn_deposit)
        self.layout.addWidget(self.btn_withdraw)
        self.layout.addWidget(self.btn_view)
        self.layout.addWidget(self.btn_export)
        self.layout.addWidget(self.btn_import)
        self.layout.addWidget(self.btn_quit)

        # Connect button actions
        self.btn_deposit.clicked.connect(self.handle_deposit)
        self.btn_withdraw.clicked.connect(self.handle_withdraw)
        self.btn_view.clicked.connect(self.view_transactions)
        self.btn_export.clicked.connect(self.export_data)
        self.btn_import.clicked.connect(self.import_data)
        self.btn_quit.clicked.connect(self.close)

        self.setLayout(self.layout)

    def handle_deposit(self):
        return

    def handle_withdraw(self):
        return

    def update_balance(self):
        return

    def view_transactions(self):
        return

    def export_data(self):
        return

    def import_data(self):
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    home = HomeScreen()
    home.show()
    sys.exit(app.exec_())