import os, json

# File path to save the tasks
TASKS_FILE_PATH = r"c:\Users\ARZ\Desktop\USER MANAGEMENT\to_do_list.json"

class UserToDoList:

    @staticmethod
    def load_tasks():
        """Load tasks from the file if it exists."""
        if os.path.exists(TASKS_FILE_PATH):
            with open(TASKS_FILE_PATH, 'r') as file:
                try:
                    data = json.load(file)
                    # If the loaded data is not a dictionary, return an empty dict.
                    if isinstance(data, dict):
                        return data
                except json.JSONDecodeError:
                    return {}
        return {} 

    @staticmethod
    def save_tasks(tasks):
        """Save tasks to the JSON file in a structured format."""
        with open(TASKS_FILE_PATH, 'w') as file:
            json.dump(tasks, file, indent = 4)
    
    @staticmethod
    def load_tasks_for_user(username):
        """Retrieve the list of tasks for the given username."""
        all_tasks = UserToDoList.load_tasks()
        return all_tasks.get(username, [])
    
    @staticmethod
    def save_tasks_for_user(username, tasks):
        """Save tasks for a specific user."""
        all_tasks = UserToDoList.load_tasks()
        all_tasks[username] = tasks
        UserToDoList.save_tasks(all_tasks)
        
    def run_todo_list(username):
        """Run the user-specific to-do list menu."""
        tasks = UserToDoList.load_tasks_for_user(username)
        print(f"\n📌 Welcome to your To-Do List, {username.capitalize()}!")
        
        while True:
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("1️⃣  ➤ Add a Task 📝")
            print("2️⃣  ➤ View Tasks 📋")
            print("3️⃣  ➤ Remove a Task ❌")
            print("4️⃣  ➤ Mark Task as Completed ✅")
            print("5️⃣  ➤ Exit 🚪")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━")
            choice = input("👉 Enter your option (1-5): ").strip()            
            
            if choice == "1":
                new_task = input("📝 Add a new task: ").strip()
                if new_task:
                    if new_task not in tasks:
                        tasks.append(new_task)
                        UserToDoList.save_tasks_for_user(username, tasks)
                        print(f"✅ Task '{new_task}' added successfully!")
                    else:
                        print("⚠️ Task already exists!")
                else:
                    print("⚠️ Task cannot be empty.")
            elif choice == "2":
                if tasks:
                    print("\n📋 Your Tasks:")
                    for index, task in enumerate(tasks, start=1):
                        print(f"🔹 {index}. {task}")
                else:
                    print("📭 Your to-do list is empty!")
            elif choice == "3":
                if tasks:
                    try:
                        task_index = int(input("❌ Enter the number of the task to remove: ")) - 1
                        if 0 <= task_index < len(tasks):
                            removed_task = tasks.pop(task_index)
                            UserToDoList.save_tasks_for_user(username, tasks)
                            print(f"🗑️ Task '{removed_task}' removed successfully!")
                        else:
                            print("⚠️ Invalid task number.")
                    except ValueError:
                        print("⚠️ Please enter a valid number.")
                else:
                    print("📭 Your to-do list is empty!")
            elif choice == "4":
                if tasks:
                    try:
                        task_index = int(input("✅ Enter the number of the task to mark as completed: ")) - 1
                        if 0 <= task_index < len(tasks):
                            if not tasks[task_index].startswith("✅"):
                                tasks[task_index] = f"✅ {tasks[task_index]}"
                                UserToDoList.save_tasks_for_user(username, tasks)
                                print("🎯 Task marked as completed!")
                            else:
                                print("ℹ️ This task is already marked as completed.")
                        else:
                            print("⚠️ Invalid task number.")
                    except ValueError:
                        print("⚠️ Please enter a valid number.")
                else:
                    print("📭 Your to-do list is empty!")
            elif choice == "5":
                print("👋 Exiting your To-Do List. Goodbye!")
                break
            else:
                print("⚠️ Invalid choice, please try again.")