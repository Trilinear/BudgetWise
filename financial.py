from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox,
                            QPushButton, QVBoxLayout, QMessageBox,
                            QTableWidget, QTableWidgetItem, QSizePolicy, QHBoxLayout)

from datamodel import User, Account
import sqlite3
from database import get_session
import matplotlib as plt
plt.use('Qt5Agg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.dates import date2num, DateFormatter
import datetime
from collections import defaultdict
from datamodel import Category
import numpy as np



class FinancialHistory(QWidget):
    def __init__(self, user, on_home_click):
        super().__init__()
        self.user = user
        self.on_home_click = on_home_click
        self.session = get_session()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(0, 0, 1600, 800)
        self.setStyleSheet("""
            QWidget {
                background-color: #378805;
                color: white;
            }
            QPushButton {
                background-color: #dcdcdc;
                color: black;
                border-radius: 5px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
            QTableWidget {
                color: black;
                background-color:#378805;
                border: none;
            }
            QComboBox {
                color: black;
                background-color: white;
            }
        """)

        layout = QVBoxLayout()
        header = QLabel(f"User {self.user.username}'s Financial History")
        layout.addWidget(header)


        self.account_header = QLabel(f"Accounts:")
        self.account_combo = QComboBox()
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

        #Show transactions table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem('ID'))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Category'))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem('Amount'))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem('Date'))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem('Description'))
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setMinimumHeight(250)
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #dddddd; color: black; }")
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        #Sort controls
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Sort by Category (A-Z)",
            "Sort by Amount (Ascending)",
            "Sort by Amount (Descending)"
        ])
        layout.addWidget(self.sort_combo)

        self.sort_button = QPushButton("Sort Table")
        self.sort_button.clicked.connect(self.sort_table)
        layout.addWidget(self.sort_button)
        
        #Expense over time
        self.figure = Figure(figsize=(8, 4), dpi=100)  
        self.figure_canvas = FigureCanvasQTAgg(self.figure)
        self.subplot = self.figure.add_subplot(111)

        #Categorical spending
        self.category_figure = Figure(figsize=(8, 4), dpi=100)  
        self.category_canvas = FigureCanvasQTAgg(self.category_figure)
        self.category_subplot = self.category_figure.add_subplot(111)

        #Container for side by side graphs
        graphs_container = QWidget()
        graphs_layout = QHBoxLayout()
        graphs_layout.addWidget(self.figure_canvas)
        graphs_layout.addWidget(self.category_canvas)
        graphs_container.setLayout(graphs_layout)

        layout.addWidget(graphs_container)

        self.show_expense_graph = QPushButton(f"Show Expenses on Graph")
        self.show_expense_graph.clicked.connect(self.set_figure)
        self.show_expense_graph.clicked.connect(self.set_category_figure)
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

    def sort_table(self):
        row_count = self.table.rowCount()
        if row_count == 0:
            return

        data = []
        for row in range(row_count):
            row_data = [
                self.table.item(row, 0).text(),  # ID
                self.table.item(row, 1).text(),  # Category
                float(self.table.item(row, 2).text()),  # Amount (as float)
                self.table.item(row, 3).text(),  # Date
                self.table.item(row, 4).text()   # Description
            ]
            data.append(row_data)

        sort_index = self.sort_combo.currentIndex()
        if sort_index == 0:
            data.sort(key=lambda x: x[1])  # Category (A-Z)
        elif sort_index == 1:
            data.sort(key=lambda x: x[2])  # Amount ascending
        elif sort_index == 2:
            data.sort(key=lambda x: x[2], reverse=True)  # Amount descending

        self.table.setRowCount(0)
        for rowNum, rowData in enumerate(data):
            self.table.insertRow(rowNum)
            for colNum, value in enumerate(rowData):
                self.table.setItem(rowNum, colNum, QTableWidgetItem(str(value)))

        self.table.resizeColumnsToContents()

    def set_figure(self):
        self.subplot.clear()
        self.subplot.set_title("Expenses Over Time")
        self.subplot.set_xlabel("Date")
        self.subplot.set_ylabel("Amount Spent")

        account = self.user.select_account(self.session, self.account_combo.currentIndex())
        if self.category_combo.currentIndex() == 0:
            transactions = account.get_all_transactions(self.session)
        else:
            transactions = account.select_transactions_by_category(self.session, self.category_combo.currentIndex() - 1)

        #Aggregate expenses by date
        daily_expenses = defaultdict(float)
        for transaction in transactions:
            if transaction.amount < 0:
                date = transaction.date.date()  
                daily_expenses[date] += abs(transaction.amount)

        if daily_expenses:
            #Sort by date
            sorted_dates = sorted(daily_expenses.keys())
            amount_list = [daily_expenses[date] for date in sorted_dates]

            #Convert to matplotlib date format
            date_nums = date2num(sorted_dates)
            self.subplot.plot(date_nums, amount_list, linestyle='-', marker='o', color='red', label='Spending')

            self.subplot.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            self.subplot.tick_params(axis='x', rotation=45)

            self.subplot.legend()
            self.figure.tight_layout()
            self.figure_canvas.draw_idle()
    
    def set_category_figure(self):
        self.category_subplot.clear()  
        
        self.category_subplot.set_title("Spending by Category")
        self.category_subplot.set_xlabel("Categories")
        self.category_subplot.set_ylabel("Total Amount Spent ($)")
        account = self.user.select_account(self.session, self.account_combo.currentIndex())
        transactions = account.get_all_transactions(self.session)
        
        #Aggregate spending by category
        category_spending = {}
        for transaction in transactions:
            if transaction.amount < 0:  
                category = transaction.category
                amount = abs(transaction.amount)
                if category in category_spending:
                    category_spending[category] += amount
                else:
                    category_spending[category] = amount
        
        if category_spending:
            categories = list(category_spending.keys())
            amounts = list(category_spending.values())
            bars = self.category_subplot.bar(categories, amounts)
            #Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                self.category_subplot.text(bar.get_x() + bar.get_width()/2., height,
                                        f'${height:.2f}',
                                        ha='center', va='bottom')
            
            #Formatting
            self.category_subplot.tick_params(axis='x', rotation=45)
            self.category_subplot.set_ylim(top=max(amounts)*1.2)  # Add 10% headroom
            self.category_figure.tight_layout()
            self.category_canvas.draw_idle()

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