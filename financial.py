from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox,
                            QPushButton, QVBoxLayout, QMessageBox,
                            QTableWidget, QTableWidgetItem)

from datamodel import User, Account
import sqlite3
from database import get_session


class FinancialHistory(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setup_ui()
        self.session = get_session()

    def setup_ui(self):
        layout = QVBoxLayout()
        header = QLabel(f"User {self.user.username}'s Financial History")
        layout.addWidget(header)


        self.account_combo = QComboBox()
        for account in self.user.accounts:
            self.account_combo.addItem(account.name)
        layout.addWidget(self.account_combo)

        self.show_expense_query = QPushButton(f"Show Expenses")
        self.show_expense_query.clicked.connect(self.fetch_transactions)
        layout.addWidget(self.show_expense_query)

        self.table = QTableWidget()
        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderItem(0, QTableWidgetItem('ID'))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Category'))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem('Amount'))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem('Date'))

        layout.addWidget(self.table)


        self.setLayout(layout)



    def fetch_transactions(self):
        # ID has to be added by 1 because SQL tables are not zero-indexed, while QComboBoxes are
        account = self.user.select_account(self.session, self.account_combo.currentIndex() + 1)
        self.table.clearContents()
        for rowNum in range(len(account.transactions)):
            self.table.insertRow(rowNum)
            # Must be stringified, PyQT's table widget doesn't accept floats or datetimes
            self.table.setItem(rowNum, 0, QTableWidgetItem(str(account.transactions[rowNum].id)))
            self.table.setItem(rowNum, 1, QTableWidgetItem(account.transactions[rowNum].description))
            self.table.setItem(rowNum, 2, QTableWidgetItem(str(account.transactions[rowNum].amount)))
            self.table.setItem(rowNum, 3, QTableWidgetItem(str(account.transactions[rowNum].date)))
        self.table.resizeColumnsToContents()


