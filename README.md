# TaskManagerPro

TaskManagerPro is a comprehensive task management application built with Python. It features user authentication, task management, task reminders, and more. This application uses SQLite for data storage and SQLAlchemy for database interactions.

## Features

- User Authentication (Login/Register)
- Task Management (Add, View, Edit, Delete)
- Task Priorities and Categories
- Task Reminders with Email Notifications
- Task Comments
- Task Sorting and Searching
- Data Persistence with SQLite and JSON
- Modular Code Structure
- Unit Tests for Reliability

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/brettadams0/TaskManagerPro.git
    cd TaskManagerPro
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```bash
    python task_manager.py
    ```

2. Follow the on-screen instructions to manage your tasks.

## Configuration

To enable email notifications, update the email configuration in `task_manager.py`:
```python
sender_email = "your_email@example.com"
receiver_email = "receiver_email@example.com"
password = "your_email_password"
```
## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

