# 🔐 User Management System

## 📌 Overview
This is a modular, Python-based **User Management System** designed to simulate a lightweight, file-based backend environment. It supports **user registration**, **authentication**, **activity tracking**, **to-do list management**, and even **interactive games**. Ideal for learning authentication flows, file handling, modular coding, and system design.

---

## 🧩 Features

### ✅ User Registration & Login
- Email, username, and password validation
- Secure storage of credentials using JSON
- Handles login authentication with error feedback

### 🗂️ To-Do List (Per User)
- Add, remove, mark as complete
- Tasks persist across sessions (saved in JSON)
- Isolated task list for each user

### 📜 User Logging
- Logs user activity in a `.log` file
- Tracks logins, logouts, task modifications

### 🎮 Games Module *(Optional)*
- Text-based games (e.g., number guessing)
- Available to logged-in users for basic interactivity

### 🧱 Modular Codebase
- Fully separated into reusable, testable modules
- Clear separation of concerns for scalability and readability

---

## 🗂️ Project Structure

```plaintext
USER_MANAGEMENT/
├── main.ipynb                # Main interface for running and testing features
├── auth.py                   # Handles user authentication
├── user_account.py           # User profile and session management
├── account_validator.py      # Validates user input (email, username, password)
├── account_storage.py        # Read/write user data to JSON
├── account_manager.py        # High-level account creation and login logic
├── to_do_list.py             # To-do list logic (per user)
├── to_do_list.json           # Stores user-specific to-do list data
├── user_accounts.json        # Stores registered user credentials
├── user_activity.log         # Logs user actions (login, logout, task events)
├── helper.py                 # Utility functions (formatting, input handling)
├── games.py                  # Optional games module
```

## 🚀 How to Run

### 🔧 Clone the Repository
```bash
git clone https://github.com/your-username/user-management-system.git
cd user-management-system
```

## 🧪 Run the App
Open main.ipynb in Jupyter Notebook to explore all features interactively.

Or run individual scripts in the terminal using:
```bash
python auth.py
```

### 🧠 Concepts Practiced
- ✅ Object-Oriented Programming
- 📂 File Handling with JSON & Logging
- 🔐 Input Validation & Sanitization
- 🧩 Modular System Architecture
- 🎮 Gamification with Python

## 📎 Credits
Developed by Reza Zare as a personal Python project to practice building modular systems with authentication, persistent storage, and interactive CLI modules.
