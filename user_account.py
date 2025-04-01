import re, random, string
from datetime import datetime

class UserAccount:

    def __init__(self, fname="", lname="", username="", phone_number="", password="", email=""):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.phone_number = phone_number
        self.password = password
        self.email = email
        # JSON cannot serialize datetime objects by default, so we save it as .isoformat()
        self.date_created = datetime.now().isoformat()
        self.date_modified = datetime.now().isoformat()


    # *********************** User Info ***********************
    def get_user_info(self):
        fname = input("Please enter your first name: ").strip().title()
        lname = input("Please enter your last name: ").strip().title()
        return fname, lname

    # *********************** Username Validation ***********************
    def get_username(self):
        return input("Please enter your username: ").strip()

    # *********************** Phone Number Validation ***********************
    def get_user_number(self):
        return input("Please enter your phone number without the area code: ").strip()

    def validate_phone_number(self, phone_number):
        # Pattern to validate phone number (must include exactly 10 digits and can contain optional hyphens or spaces)
        pattern = r"^(?=.*\d)(?:\(?\d{3}\)?[\s\-]?)?\d{3}[\s\-]?\d{4}$"
        return re.fullmatch(pattern, phone_number)

    # *********************** Password Generator ***********************
    def get_generated_password(self, length=12):
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
        return "".join(random.choice(characters) for _ in range(length))

    def validate_password(self, password):
        # Pattern to require at least one digit, one lowercase letter, one uppercase letter, and one special character
        pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:'\",<>\./?]).{8,}$"
        return re.fullmatch(pattern, password)

    # *********************** Email Validator ***********************
    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.fullmatch(pattern, email)
