import os
import json
import sqlite3
from datetime import datetime, timedelta
from getpass import getpass

class Task:
    def __init__(self, task, deadline, priority, category):
        self.task = task
        self.deadline = deadline
        self.priority = priority
        self.category = category

    def __str__(self):
        return f"Task: {self.task}, Deadline: {self.deadline}, Priority: {self.priority}, Category: {self.category}"

class TaskManager:
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self.user_id = None

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    task TEXT,
                    deadline TEXT,
                    priority TEXT,
                    category TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        print("Task Manager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Save Tasks")
        print("6. Load Tasks")
        print("7. Search Tasks")
        print("8. Sort Tasks")
        print("9. Set Reminder")
        print("10. Exit")

    def authenticate_user(self):
        while True:
            choice = input("1. Login\n2. Register\nChoose an option: ")
            if choice == '1':
                username = input("Username: ")
                password = getpass("Password: ")
                user = self.conn.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
                if user:
                    self.user_id = user[0]
                    print("Login successful!")
                    break
                else:
                    print("Invalid credentials. Please try again.")
            elif choice == '2':
                username = input("Username: ")
                password = getpass("Password: ")
                try:
                    with self.conn:
                        self.conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                    print("Registration successful! Please login.")
                except sqlite3.IntegrityError:
                    print("Username already exists. Please try again.")
            else:
                print("Invalid choice. Please try again.")

    def add_task(self):
        task = input("Enter the task: ")
        deadline = input("Enter the deadline (YYYY-MM-DD): ")
        priority = input("Enter the priority (High, Medium, Low): ")
        category = input("Enter the category: ")
        with self.conn:
            self.conn.execute("INSERT INTO tasks (user_id, task, deadline, priority, category) VALUES (?, ?, ?, ?, ?)",
                              (self.user_id, task, deadline, priority, category))
        print("Task added successfully!")

    def view_tasks(self):
        tasks = self.conn.execute("SELECT id, task, deadline, priority, category FROM tasks WHERE user_id = ?", (self.user_id,)).fetchall()
        if not tasks:
            print("No tasks available.")
        else:
            print("Tasks:")
            for task in tasks:
                print(f"{task[0]}. Task: {task[1]}, Deadline: {task[2]}, Priority: {task[3]}, Category: {task[4]}")

    def edit_task(self):
        self.view_tasks()
        task_id = int(input("Enter the task ID to edit: "))
        task = input("Enter the new task: ")
        deadline = input("Enter the new deadline (YYYY-MM-DD): ")
        priority = input("Enter the new priority (High, Medium, Low): ")
        category = input("Enter the new category: ")
        with self.conn:
            self.conn.execute("UPDATE tasks SET task = ?, deadline = ?, priority = ?, category = ? WHERE id = ? AND user_id = ?",
                              (task, deadline, priority, category, task_id, self.user_id))
        print("Task edited successfully!")

    def delete_task(self):
        self.view_tasks()
        task_id = int(input("Enter the task ID to delete: "))
        with self.conn:
            self.conn.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, self.user_id))
        print("Task deleted successfully!")

    def save_tasks(self):
        tasks = self.conn.execute("SELECT task, deadline, priority, category FROM tasks WHERE user_id = ?", (self.user_id,)).fetchall()
        with open(f"tasks_{self.user_id}.json", 'w') as file:
            json.dump([{"task": task[0], "deadline": task[1], "priority": task[2], "category": task[3]} for task in tasks], file)
        print("Tasks saved successfully!")

    def load_tasks(self):
        try:
            with open(f"tasks_{self.user_id}.json", 'r') as file:
                tasks = json.load(file)
                with self.conn:
                    self.conn.executemany("INSERT INTO tasks (user_id, task, deadline, priority, category) VALUES (?, ?, ?, ?, ?)",
                                          [(self.user_id, task["task"], task["deadline"], task["priority"], task["category"]) for task in tasks])
            print("Tasks loaded successfully!")
        except FileNotFoundError:
            print("No saved tasks found.")

    def search_tasks(self):
        keyword = input("Enter a keyword to search: ")
        tasks = self.conn.execute("SELECT id, task, deadline, priority, category FROM tasks WHERE user_id = ? AND task LIKE ?", (self.user_id, f"%{keyword}%")).fetchall()
        if tasks:
            print("Search Results:")
            for task in tasks:
                print(f"{task[0]}. Task: {task[1]}, Deadline: {task[2]}, Priority: {task[3]}, Category: {task[4]}")
        else:
            print("No tasks found with the given keyword.")

    def sort_tasks(self):
        criteria = input("Sort by (task, deadline, priority, category): ").lower()
        if criteria in ["task", "deadline", "priority", "category"]:
            tasks = self.conn.execute(f"SELECT id, task, deadline, priority, category FROM tasks WHERE user_id = ? ORDER BY {criteria}", (self.user_id,)).fetchall()
            print(f"Tasks sorted by {criteria}:")
            for task in tasks:
                print(f"{task[0]}. Task: {task[1]}, Deadline: {task[2]}, Priority: {task[3]}, Category: {task[4]}")
        else:
            print("Invalid sorting criteria.")

    def set_reminder(self):
        self.view_tasks()
        task_id = int(input("Enter the task ID to set a reminder for: "))
        reminder_time = input("Enter the reminder time before the deadline (in hours): ")
        task = self.conn.execute("SELECT task, deadline FROM tasks WHERE id = ? AND user_id = ?", (task_id, self.user_id)).fetchone()
        if task:
            deadline = datetime.strptime(task[1], "%Y-%m-%d")
            reminder_time = deadline - timedelta(hours=int(reminder_time))
            print(f"Reminder set for task '{task[0]}' at {reminder_time}")
        else:
            print("Task not found.")

    def run(self):
        self.authenticate_user()
        while True:
            self.clear_screen()
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.edit_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.save_tasks()
            elif choice == '6':
                self.load_tasks()
            elif choice == '7':
                self.search_tasks()
            elif choice == '8':
                self.sort_tasks()
            elif choice == '9':
                self.set_reminder()
            elif choice == '10':
                print("Exiting Task Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.run()
