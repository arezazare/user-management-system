import json, bcrypt, logging

# file path for storing user accounts
FILE_PATH = r"c:\Users\ARZ\Desktop\USER MANAGEMENT\user_accounts.json"

# Module-level functions for account storage

def load_accounts():
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
            logging.info("Accounts loaded successfully.")
            for account in data:
                # bcrypt hashes always start with $2b$
                if not account['password'].startswith("$2b$"):
                    # The encoding step is necessary to convert the password (which is a string, e.g., "password123") into a byte representation (e.g., b'password123') before hashing.
                    hashed_password = bcrypt.hashpw(account['password'].encode(), bcrypt.gensalt())
                    # JSON only stores string data, not byte strings. So, we need to decode the hashed byte string back into a regular string
                    account['password'] = hashed_password.decode()
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("🚨 File not found! Creating a new one...")
        logging.warning(f"File not found or could not be loaded: {e}")
        return []
    
def save_accounts(user_profile):
    accounts = load_accounts()
    if not user_profile['password'].startswith("$2b$"):
        hashed_password = bcrypt.hashpw(user_profile['password'].encode(), bcrypt.gensalt())
        user_profile['password'] = hashed_password.decode()
    accounts.append(user_profile)
    with open(FILE_PATH, "w") as file:
        json.dump(accounts, file, indent=4)
    logging.info(f"Account created successfully for user: {user_profile['username']}!")
    print("✅ Account created successfully!")

def reset_accounts_file():
    print("⚠️ The accounts file appears to be corrupted. Resetting the file will result in data loss.")
    user_confirmation = input("Are you sure you want to reset the accounts file? (y/n): ").strip().lower()
    if user_confirmation == 'y':
        with open(FILE_PATH, "w") as file:
            json.dump([], file, indent=4)
        logging.info("Accounts file has been reset by user confirmation.")
        print("✅ Accounts file has been reset successfully.")
    else:
        logging.info("Reset operation was canceled by user.")
        print("❌ The reset operation was canceled. No changes were made to the accounts file.")

def seed_admin():
    """
    Ensure that an admin account exists. If not, create a default one.
    """
    accounts = load_accounts()
    
    # Check if any account has the admin role
    if any(account.get("role", "user").lower() == "admin" for account in accounts):
        logging.info("Admin account already exists, skipping seed.")
        return  # Exit if an admin already exists

    admin_account = {
            "first name": "Alpha",
            "last name": "Admin",
            "username": "AlphaAdmin",              
            "phone number": "8735522273",
            "password": bcrypt.hashpw("AlphaAdmin051192".encode(), bcrypt.gensalt()).decode(),
            "email": "AlphaAdmin@echo.ca",
            "role": "admin"
        }
    
    accounts.append(admin_account)
    
    # Save the updated accounts list
    with open(FILE_PATH, "w") as file:
        json.dump(accounts, file, indent=4)
    logging.info("Admin account created successfully!")
    print("Admin account created successfully!") #debugging purposes
