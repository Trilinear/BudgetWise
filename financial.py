from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox,
                            QPushButton, QVBoxLayout, QMessageBox,
                            QTableWidget, QTableWidgetItem)

from datamodel import User, Account
import sqlite3
from database import get_session
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


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

        self.show_expense_table = QPushButton(f"Show Expenses in Table")
        self.show_expense_table.clicked.connect(self.fetch_transactions)
        layout.addWidget(self.show_expense_table)

        self.table = QTableWidget()
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderItem(0, QTableWidgetItem('ID'))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Category'))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem('Amount'))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem('Date'))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem('Description'))

        layout.addWidget(self.table)

        self.figure = Figure(figsize=(16,9), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.subplot.set_title("Transactions over Time Period")
        self.figure_canvas = FigureCanvasQTAgg(self.figure)

        layout.addWidget(self.figure_canvas)


        self.show_expense_graph = QPushButton(f"Show Expenses on Graph")
        self.show_expense_graph.clicked.connect(self.set_figure)
        layout.addWidget(self.show_expense_graph)

        self.setLayout(layout)



    def fetch_transactions(self):
        # ID has to be added by 1 because SQL tables are not zero-indexed, while QComboBoxes are
        account = self.user.select_account(self.session, self.account_combo.currentIndex() + 1)
        self.table.clearContents()
        for rowNum in range(len(account.transactions)):
            self.table.insertRow(rowNum)
            # Must be stringified, PyQT's table widget doesn't accept floats or datetimes
            self.table.setItem(rowNum, 0, QTableWidgetItem(str(account.transactions[rowNum].id)))
            self.table.setItem(rowNum, 1, QTableWidgetItem(account.transactions[rowNum].category))
            self.table.setItem(rowNum, 2, QTableWidgetItem(str(account.transactions[rowNum].amount)))
            self.table.setItem(rowNum, 3, QTableWidgetItem(str(account.transactions[rowNum].date)))
            self.table.setItem(rowNum, 4, QTableWidgetItem(account.transactions[rowNum].description))
        self.table.resizeColumnsToContents()

    def set_figure(self):
        account = self.user.select_account(self.session, self.account_combo.currentIndex() + 1)
        date_list = []
        amount_list = []
        for transaction in account.transactions:
            date_list.append(transaction.date)
            amount_list.append(transaction.amount)
        line = self.subplot.plot_date([], [])[0]
        line.set_xdata(date_list)
        line.set_ydata(amount_list)
        self.subplot.relim()  # Recalculate limits
        self.subplot.autoscale_view()  # Autoscale the view
        self.figure_canvas.draw_idle()  # Redraw the canvas smoothly
            # self.figure_canvas.draw()


