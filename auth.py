# auth.py
import bcrypt
from getpass import getpass
from datetime import datetime
from account_storage import load_accounts
from helper import (
    log_info, log_warning, log_error,
    update_accounts_file, auto_unlock_account,
    reset_password)

# ------------------ Main Login Function ------------------
def login():
    """
    Main login flow:
    1. Loads accounts from FILE_PATH
    2. Prompts user for username & password
    3. Auto-unlocks account if locked > 30 minutes
    4. Offers password reset after second failed attempt
    5. Locks account after third failed attempt
    """
    print("🔐 Logging in...")
    accounts = load_accounts()
    print("🔍 Searching for accounts...")
    print("🔍 Please wait...")
    print("🔍 Checking credentials...")

    if not accounts:
        log_warning("No accounts found.")
        print("❌ No accounts found. Please create an account first.")
        return None

    login_counter = 3
    matched_account = None

    while login_counter > 0:
        username_input = input("Enter your username: ").strip()
        
        account = next((acc for acc in accounts if acc["username"].strip() == username_input), None)

        if not account:
            print("❌ Username not found. Please try again.")
            login_counter -= 1
            continue

        # For non-admins, check if account is locked and try auto-unlock
        if account.get("role", "user").lower() != "admin" and account.get("is_locked", False):
            if auto_unlock_account(account):
                update_accounts_file(accounts)
                print("🔓 Your account has been auto-unlocked. Please continue.")
            else:
                log_warning(f"User {username_input} is locked out.")
                print("🔒 Your account is locked. Please contact the admin.")
                return None

        # Prompt for password
        password_input = getpass("Enter your password: ").strip()
        
        if bcrypt.checkpw(password_input.encode(), account["password"].encode()):
            matched_account = account
            log_info(f"Login successful for user: {username_input}.")
            print(f"✅ Login successful! Welcome back, {matched_account.get('first name', 'User').capitalize()}")
            break
        else:
            login_counter -= 1
            log_warning(f"Login failed for user: {username_input}. {login_counter} attempts remaining.")
            print(f"❌ Login failed. {login_counter} attempts remaining.")

            if login_counter == 1:  # Prompt for reset after 2 failures
                forgot = input("❓ Forgot your password? (y/n): ").strip().lower()
                if forgot == "y":
                    if reset_password(account, accounts):
                        return account
                    else:
                        return None

    if login_counter == 0:
        log_error(f"User {username_input} exceeded max login attempts.")
        print("⚠️ Too many attempts. Your account is now locked.")
        account["is_locked"] = True
        account["lock_time"] = datetime.now().isoformat()
        update_accounts_file(accounts, log_message=f"User {username_input} locked out.")
        return None

    return matched_account

if __name__ == "__main__":
    user = login()
    if user:
        print("User logged in:", user["username"])
    else:
        print("Login failed.")