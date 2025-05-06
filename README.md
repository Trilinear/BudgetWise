# BudgetWise
A Python PyQt5-based desktop application for tracking income, expenses, and financial transactions across multiple accounts.

Group Members: Simon Truong and Vincent Mei

Libraries/Dependencies:
- PyQt
- sqlalchemy
- sqlite3
- matplotlib
- datetime
- unittest
- os
- collections

Features:

Transaction Management-Add income/expense transactions, edit or delete existing transactions, categorize transactions

Visual Analytics-Expenses over time, Spending by category

Account Management-Multiple account support, Balance tracking

Steps:

- run pip install -r requirements.txt

- Run main.py and register a new account or login to existing test account:

username: test

password: password

File Structure:

Controller module: contains all of the database logic and methods

Pages module: stores all of our PyQt pages with frontend logic

Known Bugs or Limitations:
- Cannot display information of all accounts at once