import sys
from PyQt5.QtWidgets import QApplication
from pages.login import LoginScreen
from pages.home import HomeScreen
from controller.database import init_db
from pages.register import RegisterScreen
from pages.transaction import TransactionPage
from pages.financial import FinancialHistory
from pages.account import AccountPage


class AppController:
    def __init__(self):
        self.session = init_db()
        self.app = QApplication(sys.argv)
        self.current_window = None
        self.show_login()
        
    def show_login(self):
        if self.current_window:
            self.current_window.close()
        self.current_window = LoginScreen(
            on_login_success=self.on_login_success,
            on_register=self.show_register
        )
        self.current_window.show()
        
    def show_register(self):
        if self.current_window:
            self.current_window.close()
        self.current_window = RegisterScreen(
            on_back_to_login=self.show_login,
            on_registration_success=self.on_login_success
        )
        self.current_window.show()
        
    def on_login_success(self, user):
        if self.current_window:
            self.current_window.close()
        self.current_window = HomeScreen(user=user,
            on_account_click=self.show_account_page,
            on_transaction_click=self.show_transaction_page,
            on_financial_click=self.show_financial_history
        )
        self.current_window.show()

    def show_home_page(self, user):
        if self.current_window:
            self.current_window.close()
        self.current_window = HomeScreen(user=user,
            on_account_click=self.show_account_page,
            on_transaction_click=self.show_transaction_page,
            on_financial_click=self.show_financial_history
        )
        self.current_window.show()

    def show_account_page(self, user):
        if self.current_window:
            self.current_window.close()
        self.current_window = AccountPage(user=user,
            on_home_click=self.show_home_page
        )
        self.current_window.show()

    def show_transaction_page(self, user):
        if self.current_window:
            self.current_window.close()
        self.current_window = TransactionPage(user,
            on_home_click=self.show_home_page
        )
        self.current_window.show()

    def show_financial_history(self, user):
        if self.current_window:
            self.current_window.close()
        self.current_window = FinancialHistory(user, on_home_click=self.show_home_page)
        self.current_window.show()

        
    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = AppController()
    controller.run()