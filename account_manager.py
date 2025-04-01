import bcrypt
from getpass import getpass
from user_account import UserAccount
from account_validator import AccountValidator
from account_storage import FILE_PATH, load_accounts
from games import Games
from to_do_list import UserToDoList
from helper import (
    log_info, log_warning, menu_choice, 
    update_accounts_file, remove_account, 
    remove_account_by_username, edit_profile
)

# ------------------ AccountManager Class ------------------
class AccountManager:

    def __init__(self):
        # Composition: AccountManager "has-a" UserAccount and AccountValidator
        self.user_account = UserAccount()
        self.validator = AccountValidator(self.user_account)

    def account_creation(self):
        # User info validation
        log_info("Starting account creation process...")
        while True:
            fname, lname = self.user_account.get_user_info()
            errors = []
            # Validate first name (fname)
            if not fname:
                errors.append("🚫 First name cannot be empty.")
            elif not fname.isalpha():
                errors.append("❌ First name should only contain letters.")
            elif len(fname) < 3:
                errors.append("⏬ First name should be at least 3 characters long.")
            elif len(fname) > 15:
                errors.append("⏫ First name should be at most 15 characters long.")
            # Validate last name (lname)
            if not lname:
                errors.append("🚫 Last name cannot be empty.")
            elif not lname.isalpha():
                errors.append("❌ Last name should only contain letters.")
            elif len(lname) < 3:
                errors.append("⏬ Last name should be at least 3 characters long.")
            elif len(lname) > 15:
                errors.append("⏫ Last name should be at most 15 characters long.")

            if errors:
                for error in errors:
                    print(error)
                    log_warning(f"User info validation error: {error}")
            else:
                self.user_account.fname = fname
                self.user_account.lname = lname
                log_info("User info validation successful.")
                print("✅ User info is valid!")
                break

        # Username validation
        while True:
            username = self.user_account.get_username()
            if not self.validator.is_unique("username", username):
                continue
            if not username:
                print("🚫 Username cannot be empty.")
                log_warning("Username cannot be empty.")
            elif not username.isalnum():
                print("❌ Usernames should only contain letters and numbers.")
                log_warning("Username should only contain letters and numbers.")
            elif len(username) < 8:
                print("⏬ Username is too short (min 8 characters).")
                log_warning("Username is too short.")
            elif len(username) > 15:
                print("⏫ Username is too long (max 15 characters).")
                log_warning("Username is too long.")
            else:
                self.user_account.username = username
                log_info(f"Username '{username}' validated successfully.")
                print("✅ Username is valid!")
                break

        # Phone number validation
        while True:
            phone = self.user_account.get_user_number()
            if not self.user_account.validate_phone_number(phone):
                print("❌ Invalid phone number format.")
                log_warning("Invalid phone number format.")
                continue
            if not phone.startswith(("873","514","438","263")):
                print("❌ Phone number must start with 873, 514, 438, or 263.")
                log_warning("Phone number must start with 873, 514, 438, or 263.")
                continue
            if not self.validator.is_unique("phone number", phone):
                continue
            self.user_account.phone_number = phone
            log_info(f"Phone number '{phone}' validated successfully.")
            print("✅ Phone number is valid!")
            break

        # Password generation/validation
        while True:
            password = getpass("Enter your password (or press Enter to generate one): ").strip()
            if not password:
                password = self.user_account.get_generated_password()
                print(f"🚀 Generated password: {password}")
                log_info("Generated password.")
                self.user_account.password = password
                break
            if not self.user_account.validate_password(password):
                print("❌ Password must have at least 8 characters, including uppercase, lowercase, a digit, and a special character.")
                log_warning("Invalid password format.")
                continue
            if not self.validator.confirm_password(password):
                continue
            # adding hashing to the password
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # Hash password
            self.user_account.password = hashed_password.decode()  # Store the hashed password as a string
            log_info("Password validation successful!")
            break

        # Email validation
        while True:
            email = input("Enter your email: ").strip().lower()
            if not self.validator.is_unique("email", email):
                continue
            if not self.user_account.validate_email(email):
                print("⚠️ Invalid email format.")
                log_warning("Invalid email format.")
                continue
            allowed_domains = (".com", ".org", ".net", ".ca")
            if not email.endswith(allowed_domains):
                print("⚠️ Email should end with .com, .org, .net, or .ca.")
                log_warning("Email should end with .com, .org, .net, or .ca.")
                continue
            self.user_account.email = email
            print("✅ Email is valid!")
            log_info(f"Email '{email}' validated successfully.")
            break
        
        # Build and display the user profile
        user_profile = {
            "first name": self.user_account.fname,
            "last name": self.user_account.lname,
            "username": self.user_account.username,
            "phone number": self.user_account.phone_number,
            "password": self.user_account.password,
            "email": self.user_account.email,
            "role": "user",
            "is_locked": False,
            "date_created": self.user_account.date_created,
            "date_modified": self.user_account.date_modified
        }
        print("\n*********************** User Profile ***********************")
        for key, value in user_profile.items():
            print(f"🚀 {key.title()}: {value}")
        print("***********************************************************\n")
        return user_profile

       # *********************** Login Feature ***********************

    def post_login_menu(self, matched_account):
        # """Displays a post-login menu based on whether the user is admin or non-admin."""
        accounts = load_accounts() # Reload accounts if needed
        # ✅ Only show the menu if login is successful
        if matched_account:         
            # Non-admin user menu
            if matched_account.get("role", "user").lower() != "admin":
                    print(
                        f"🔑 Welcome, {matched_account['first name']}!\n"
                        "User Menu:\n"
                        "1. View profile.\n"
                        "2. Edit profile.\n"
                        "3. Remove account.\n"
                        "4. Play Games.\n"
                        "5. To-do List.\n"
                        "6. Log out.\n"
                        )
                    while True:
                        choice = menu_choice("\nplease enter your option between 1 and 6: ",1,6)

                        if choice == 1:
                            print("\nYour profile information: \n")
                            # for key, value in account.items():
                            for key, value in matched_account.items():
                                print(f"{key.title()}: {value}")
                        elif choice == 2:
                            edit_profile(matched_account, accounts, FILE_PATH)
                        elif choice == 3:
                            print("Remove Account:")
                            deletion_confirmation = input("Are you sure you want to delete your account? (y/n): ").strip().lower()
                            if deletion_confirmation == "y":
                                remove_account(accounts, matched_account)
                                return
                            else:
                                log_info(f"Account deletion canceled by user: {matched_account['username']}.")
                                print("🚀 Account deletion canceled.")
                        elif choice == 4:
                            while True:
                                print("\n🎮 Games Menu:")
                                print("1. Lottery Game")
                                print("2. Number Guessing Game")
                                print("3. Rock, Paper, Scissors")
                                print("4. Hangman")
                                print("5. Quiz Game")
                                print("6. Exit\n")
                            
                                game_choice = input("Please choose a game to play: ").strip()
                                
                                if not game_choice.isdigit() or int(game_choice) < 1 or int(game_choice) > 6:
                                    log_warning("Invalid game choice.")
                                    print("❌ Invalid game choice. Please enter a number between 1 and 6.")
                                    continue
                                
                                if game_choice == "6":
                                    log_info("Exiting the games menu.")
                                    print("\nExiting the games menu...")
                                    break  # Exit the games menu loop
        
                                
                                game_methods = {
                                    "1": Games().play_lottery,
                                    "2": Games().play_number_guessing,
                                    "3": Games().play_rock_paper_scissors,
                                    "4": Games().play_hangman,
                                    "5": Games().play_quiz,
                                }
                                
                                if game_choice in game_methods:
                                    game_methods[game_choice]()
                                else:
                                    log_warning("Invalid game choice.")
                                    print("❌ Invalid game choice. Please enter a number between 1 and 6.")
                        elif choice == 5:
                            # to do list
                            UserToDoList.run_todo_list(matched_account["username"])
                        elif choice == 6:
                            print("Logging out...")
                            print("\nExiting the program, Goodbye!")
                            return
            # Admin user menu
            else:
                    print(
                    "🔑 Welcome, Admin!"
                    "\nAdmin Menu:\n"
                    "1. View all profiles.\n"
                    "2. Search for a specific account.\n"
                    "3. Edit profiles.\n"
                    "4. Remove accounts.\n"
                    "5. Unlock accounts.\n"
                    "6. Log out.\n")

                    while True:
                        choice = menu_choice("Please enter your option (1-6): ", 1, 6)
                        if choice == 1:
                            print("\nUser Profiles:")
                            for account in accounts:
                                if account.get("role","user").lower() == "user":
                                    for key, value in account.items():
                                        print(f"{key.title()}: {value}")
                                print("*" * 50)
                        elif choice == 2:
                            print("Filter Profiles:")
                            filtered_username  = input("please enter the username of the user you want to filter. ").strip()
                            for account in accounts:
                                if account["username"].strip().lower() == filtered_username.lower():
                                    for key, value in account.items():
                                        print(f"{key.title()}: {value}")
                                        print("*" * 40)
                                    break
                        elif choice == 3:
                            print("Editing Profiles:")
                            filtered_username  = input("please enter the username of the user you want to edit. ").strip()
                            account_to_edit = None
                            for account in accounts:
                                if account['username'].strip().lower() == filtered_username.lower():
                                    account_to_edit = account
                                    break
                            if account_to_edit is None:
                                log_warning(f"User {filtered_username} not found.")
                                print("❌ User not found. Please try again.")
                            else:
                                edit_profile(account_to_edit, accounts, FILE_PATH)
                            log_info(f"Profile updated for user: {account_to_edit['username']}.")
                        elif choice == 4:
                            print("Remove Accounts:")
                            filtered_username = input("please enter the username of the user you want to remove. ").strip()
                            remove_account_by_username(accounts, filtered_username)
                        elif choice == 5:
                            print("🔒 Locked Accounts:")
                            # locked_accounts = [account for account in account if account.get("is_locked") is True]
                            locked_accounts = [account for account in accounts if account.get("is_locked")]
                            
                            if not locked_accounts:
                                print("✅ No locked accounts. ")
                            else:
                                for account in locked_accounts:
                                    print(f"- {account['username']}")
                                    print("*" * 40)
                            
                                unlock = input("Do you want to unlock an account? (y/n): ").strip().lower()
                                if unlock == "y":
                                    username_to_unlock = input("Enter the username to unlock: ").strip()
                                    
                                    # Find the account in the locked list
                                    unlocked = False
                                    for account in locked_accounts:
                                        if account['username'].lower() == username_to_unlock.lower():
                                            account["is_locked"] = False
                                            account.pop("lock_time",None) # Remove lock time since it's unlocked
                                            print(f"✅ Account for {account['username']} has been unlocked. ")
                                            unlocked = True
                                            break

                                    if unlocked:
                                        # Save all accounts back to the JSON file
                                        update_accounts_file(accounts)
                                    else:
                                        print("❌ Username not found in locked accounts.")
                                else: 
                                    print("❌ Account unlocking cancelled.")

                        elif choice == 6:
                            print("Logging out...")
                            print("\nExiting the program, Goodbye!")
                            return
        