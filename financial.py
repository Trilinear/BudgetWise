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
    def __init__(self, user, on_home_click):
        super().__init__()
        self.user = user
        self.on_home_click = on_home_click
        self.session = get_session()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
            background-color: #378805;
            color: white;
        """)

        layout = QVBoxLayout()
        header = QLabel(f"User {self.user.username}'s Financial History")
        layout.addWidget(header)


        self.account_header = QLabel(f"Accounts:")
        self.account_combo = QComboBox()
        for account in self.user.accounts:
            self.account_combo.addItem(account.name)
        self.account_combo.activated.connect(self.update_category_combo)
        layout.addWidget(self.account_header)
        layout.addWidget(self.account_combo)

        self.category_header = QLabel(f"Existing Transaction Categories for Account:")
        self.category_combo = QComboBox()
        # This is for when you initially open the data, this will just insert the categories for the first account
        self.update_category_combo()

        layout.addWidget(self.category_header)
        layout.addWidget(self.category_combo)

        self.show_expense_table = QPushButton(f"Show Expenses in Table")
        self.show_expense_table.clicked.connect(self.set_table)
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
        self.line = self.subplot.plot_date([], [])[0]

        layout.addWidget(self.figure_canvas)

        self.show_expense_graph = QPushButton(f"Show Expenses on Graph")
        self.show_expense_graph.clicked.connect(self.set_figure)
        layout.addWidget(self.show_expense_graph)

        self.home_button = QPushButton('Return to Home')
        self.home_button.clicked.connect(self.open_home)
        layout.addWidget(self.home_button)

        self.setLayout(layout)

    # Functions to display table and figure based on selected combos
    def set_table(self):
        account = self.user.select_account(self.session, self.account_combo.currentIndex())
        if self.category_combo.currentIndex() == 0:
            transactions = account.transactions
        else:
            transactions = account.select_transactions_by_category(self.session, self.category_combo.currentIndex() - 1)

        self.table.clearContents()
        self.table.setRowCount(0)
        for rowNum in range(len(transactions)):
            self.table.insertRow(rowNum)
            # Must be stringified, PyQT's table widget doesn't accept floats or datetimes
            self.table.setItem(rowNum, 0, QTableWidgetItem(str(transactions[rowNum].id)))
            self.table.setItem(rowNum, 1, QTableWidgetItem(transactions[rowNum].category))
            self.table.setItem(rowNum, 2, QTableWidgetItem(str(transactions[rowNum].amount)))
            self.table.setItem(rowNum, 3, QTableWidgetItem(str(transactions[rowNum].date)))
            self.table.setItem(rowNum, 4, QTableWidgetItem(transactions[rowNum].description))
        self.table.resizeColumnsToContents()

    def set_figure(self):
        date_list = []
        amount_list = []
        if self.line:
            self.line.remove()

        account = self.user.select_account(self.session, self.account_combo.currentIndex())
        if self.category_combo.currentIndex() == 0:
            transactions = account.get_all_transactions(self.session)
        else:
            transactions = account.select_transactions_by_category(self.session, self.category_combo.currentIndex() - 1)

        for transaction in transactions:
            date_list.append(transaction.date)
            amount_list.append(transaction.amount)

        self.line = self.subplot.plot_date([], [])[0]
        self.line.set_xdata(date_list)
        self.line.set_ydata(amount_list)
        self.subplot.relim()  # Recalculate limits
        self.subplot.autoscale_view()  # Autoscale the view
        self.figure_canvas.draw_idle()  # Redraw the canvas smoothly
            # self.figure_canvas.draw()


    # Update logic for updating combos on launch, relaunch, or switched to new account combo index
    def update_accounts_combo(self):
        self.account_combo.clear()
        accounts = self.user.get_all_accounts(self.session)
        for account in accounts:
            self.account_combo.addItem(account.name)

    def update_category_combo(self):
        account = self.user.select_account(self.session, self.account_combo.currentIndex())
        categories = account.get_all_categories(self.session)
        category_names = list()
        for category in categories:
            category_names.append(category.name)
        self.category_combo.clear()
        self.category_combo.insertItem(0, 'All Categories')
        self.category_combo.insertItems(1, category_names)

    def showEvent(self, event):
        # This refreshes our combo boxes whenever we launch or relaunch this window so that the account pages update properly.
        super().showEvent(event)
        self.update_accounts_combo()
        self.update_category_combo()


    # Route to return back to home page
    def open_home(self):
        self.on_home_click(self.user)
        self.close()