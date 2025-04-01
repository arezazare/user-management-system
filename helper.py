import json, logging, bcrypt
from datetime import datetime, timedelta
from getpass import getpass
from account_storage import FILE_PATH

# ------------------ Logging ------------------
def log_warning(message):
    logging.warning(message)
def log_info(message):
    logging.info(message)
def log_error(message):
    logging.info(message)
# ------------------ Menu Choice ------------------
def menu_choice(prompt, low_bin, high_bin):
    """
    Prompt the user until they enter a valid choice between low_bin and high_bin.
    Returns the validated choice as an integer.
    """
    while True:
        choice = input(prompt).strip()
        if not choice.isdigit() or int(choice) < low_bin or int(choice) > high_bin:
            log_warning(f"Invalid user choice: {choice}. Expected a number between {low_bin} and {high_bin}.")
            print(f"❌ Invalid option. Please enter a number between {low_bin} and {high_bin}.")
        else:
            return int(choice)
# ------------------ Edit Profile ------------------
def edit_profile(account, accounts, file_path):
    """
    Allows the user to edit their profile.
    After editing, the updated accounts list is saved to file.
    """
    print("Editing Profile:\n")
    # Mapping options to fields and prompts
    field_prompts = {
        "1": ("first name", "Enter new first name: ", lambda x: x.strip().title()),
        "2": ("last name", "Enter new last name: ", lambda x: x.strip().title()),
        "3": ("phone number", "Enter new phone number: ", lambda x: x.strip()),
        "4": ("email", "Enter new email: ", lambda x: x.strip().lower()),
        "5": ("password", "Enter new password: ", None)  # We'll hash the password
    }
    while True:
        print("\n1. First Name")
        print("2. Last Name")
        print("3. Phone Number")
        print("4. Email")
        print("5. Reset Password")
        print("6. Cancel")
        option = input("Please choose your option: ").strip().lower()
        if option in field_prompts:
            field, prompt_msg, transform = field_prompts[option]
            new_value = input(prompt_msg)
            if field == "password":
                hashed = bcrypt.hashpw(new_value.encode(), bcrypt.gensalt())
                account["password"] = hashed.decode()
                log_info(f"Password updated for user: {account['username']}.")
                print("✅ Password updated successfully!")
            else:
                if transform:
                    new_value = transform(new_value)
                account[field] = new_value
                print(f"✅ {field.title()} updated successfully!")
        elif option == "6":
            print("🚀 Canceling edit...")
            break
        else:
            print("❌ Invalid option. Please try again.")
        cont = input("Do you want to continue editing? (y/n): ").strip().lower()
        if cont != "y":
            break
    log_info(f"Profile updated for user: {account['username']}.")
    # update the time modified
    account["date modified"] = datetime.now().isoformat()
    with open(file_path, "w") as file:
        json.dump(accounts, file, indent=4)
    log_info(f"Profile saved for user: {account['username']}.")
    print("✅ Profile updated successfully!")
# ------------------ Remove Profile (user panel) ------------------
def remove_account(accounts, account):
    """Removes the given account from the list and updates the file."""
    if account in accounts:
        accounts.remove(account)
        update_accounts_file(accounts)
        log_info(f"Account deleted for user: {account['username']}.")
        print("✅ Account deleted successfully!")
    else:
        log_warning("Attempted to remove an account that does not exist.")
        print("❌ Account not found.")
# ------------------ Remove Profiles (admin panel) ------------------
def remove_account_by_username(accounts, username):
    """Removes the account matching the given username and updates the file."""
    for acc in accounts:
        if acc["username"].strip().lower() == username.lower():
            accounts.remove(acc)
            update_accounts_file(accounts)
            log_info(f"Account deleted for user: {acc['username']}.")
            print("✅ Account deleted successfully!")
            return
    log_warning(f"No account found with username: {username}.")
    print("❌ No account found with that username.")
# ------------------ Update the accounts file ------------------
def update_accounts_file(accounts,log_message="Accounts file updated successfully."):
    """Writes the accounts list to the file."""
    with open(FILE_PATH, "w") as file:
        json.dump(accounts, file, indent=4)
    log_info(log_message)
# ------------------ Reset password ------------------
def reset_password(account, accounts):
    """
    Allows a user to reset their password for the given account.
    Updates the account and saves changes to the accounts list.
    """
    print("\n🔑 Password Reset: ")
    new_password = getpass("Enter your new password: ").strip()
    confirm_password = getpass("Confirm your new password: ").strip()
    
    if not new_password:
        print("❌ New password cannot be empty.")
        return False
    
    if new_password != confirm_password:
        print("❌ Passwords do not match. Please try again.")
        return False

    hashed_password = bcrypt.hashpw(new_password.encode(),bcrypt.gensalt())
    account['password'] = hashed_password.decode()
    account['date_modified'] = datetime.now().isoformat()
    update_accounts_file(accounts, log_message=f"Password reset for {account['username']}.")
    print("✅ Password reset successfully!")
    return True
# ------------------ Auto-unlock accounts ------------------
def auto_unlock_account(account):
    """
    If the account is locked and has been locked for at least 30 minutes,
    unlocks the account (sets 'is_locked' to False and removes 'lock_time').
    
    Returns:
        True if the account was unlocked (i.e., 30 minutes have passed), else False.
    """
        # Check if the account is marked as locked and has a lock time recorded
    if account.get("is_locked") and account.get("lock_time"):
        # Convert the stored lock_time (ISO string) back to a datetime object
        lock_time = datetime.fromisoformat(account["lock_time"])
        # Check if 30 minutes have passed since lock_time
        if datetime.now() - lock_time >= timedelta(minutes=30):
            account["is_locked"] = False   # Unlock the account
            account.pop("lock_time", None) # Remove the lock_time key
            return True
    return False
