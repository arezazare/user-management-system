import logging
from getpass import getpass
from account_storage import load_accounts

class AccountValidator:

    def __init__(self, user_account):
        self.user_account = user_account # Composition: AccountValidator "has-a" user_account

    # Validation for uniqueness
    def is_unique(self, key, value):
        accounts = load_accounts()
        if any(account[key].lower() == value.lower() for account in accounts):
            print(f"⚠️ This {key} is already taken. Please choose a different one.")
            logging.warning(f"Duplicate {key} found: {value}")
            return False
        return True

    # Password confirmation
    def confirm_password(self, password):
        while True:
            confirm = getpass("Confirm your password: ").strip()
            if confirm == password:
                logging.info("Password confirmation successful.")   
                print("🎉 Password confirmation successful!")
                return True
            logging.warning("Password confirmation failed.")
            print("❌ Password confirmation failed. Please try again.")