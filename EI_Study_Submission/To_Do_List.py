from getpass import getpass
from datetime import datetime, timedelta
import logging

# Behavioral Pattern - Memento Pattern
class Memento:
    def __init__(self, state):
        self._state = state

    def get_state(self):
        return self._state

# Creational Pattern - Builder Pattern
class TaskBuilder:
    def __init__(self, description):
        self.task = Task(description)

    def set_due_date(self, due_date):
        self.task.set_due_date(due_date)
        return self

    def set_tags(self, tags):
        self.task.set_tags(tags)
        return self

    def set_priority(self, priority):
        self.task.set_priority(priority)
        return self

    def set_reminder(self, reminder):
        self.task.set_reminder(reminder)
        return self

    def build(self):
        return self.task

# Inheritance and Polymorphism - Base class Item
class Item:
    def __init__(self, description):
        self.description = description
        self.completed = False
        self.priority = 0
        self.due_date = None
        self.reminder = None

    def mark_completed(self):
        self.completed = True

    def set_priority(self, priority):
        self.priority = priority

    def set_due_date(self, due_date):
        self.due_date = datetime.strptime(due_date, '%Y-%m-%d %I:%M %p') if due_date else None

    def set_reminder(self, reminder):
        self.reminder = datetime.strptime(reminder, '%Y-%m-%d %I:%M %p') if reminder else None

    def display(self):
        status = "Completed" if self.completed else "Pending"
        priority_str = f", Priority: {self.priority}" if self.priority else ""
        due_date_str = f", Due: {self.due_date.strftime('%Y-%m-%d %I:%M %p')}" if self.due_date else ""
        reminder_str = f", Reminder: {self.reminder.strftime('%Y-%m-%d %I:%M %p')}" if self.reminder else ""
        return f"{self.description} - {status}{priority_str}{due_date_str}{reminder_str}"

# Inheritance and Polymorphism - Task class
class Task(Item):
    def __init__(self, description):
        super().__init__(description)
        self.tags = []

    def set_tags(self, tags):
        self.tags = tags.split(',')

# Inheritance and Polymorphism - Note class
class Note(Item):
    def __init__(self, description, content):
        super().__init__(description)
        self.content = content

    def display(self):
        status = "Completed" if self.completed else "Pending"
        return f"{self.description} - {status}, Content: {self.content}"

# Transient Error Handling Mechanism
class TaskManager:
    def __init__(self):
        self.items = []
        self.history = []

    def add_item(self, item):
        self.items.append(item)
        self.save_state()

    def mark_completed(self, description):
        item = self._find_item(description)
        if item:
            item.mark_completed()
            self.save_state()

    def delete_item(self, description):
        item = self._find_item(description)
        if item:
            self.items.remove(item)
            self.save_state()

    def view_items(self, filter_type=None):
        filtered_items = self.items

        if filter_type == "completed":
            filtered_items = [item for item in self.items if item.completed]
        elif filter_type == "pending":
            filtered_items = [item for item in self.items if not item.completed]

        return filtered_items

    def sort_items_by_priority(self):
        return sorted(self.items, key=lambda x: x.priority)

    def sort_items_by_due_date(self):
        return sorted(self.items, key=lambda x: x.due_date)

    def undo(self):
        if len(self.history) >= 1:
            self.history.pop()
            self.items = self.history[-1].get_state()

    def save_state(self):
        self.history.append(Memento(list(self.items)))

    def _find_item(self, description):
        for item in self.items:
            if item.description == description:
                return item
        return None

# Logging Mechanism
logging.basicConfig(filename='todo.log', level=logging.INFO)

# User Authentication
def authenticate_user():
    while True:
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")  # using getpass to hide password input
        # Simple hardcoded username and password for demonstration
        if username == "Akhilesh" and password == "Nvsk2003":
            print("Login successful!")
            break
        else:
            print("Invalid username or password. Please try again.")

# Exception Handling Mechanism
try:
    # Perform user authentication before entering the main loop
    authenticate_user()
    manager = TaskManager()

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Mark Completed")
        print("3. Delete Task")
        print("4. View Tasks")
        print("5. Sort Tasks by Priority")
        print("6. Sort Tasks by Due Date")
        print("7. Undo")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD HH:MM AM/PM, press Enter if none): ")
            tags = input("Enter tags (comma-separated, press Enter if none): ")
            priority = int(input("Enter priority (0 for no priority): "))
            
            reminder = input("Enter reminder (YYYY-MM-DD HH:MM AM/PM, press Enter if none): ")
            while reminder:
                try:
                    reminder_date = datetime.strptime(reminder, '%Y-%m-%d %I:%M %p') if reminder else None
                    due_date_time = datetime.strptime(due_date, '%Y-%m-%d %I:%M %p') if due_date else None
                    if reminder_date and (reminder_date < datetime.now() or (due_date_time and reminder_date < due_date_time)):
                        break
                    else:
                        print("The reminder date should be less than the current date and due date. Please enter a valid reminder date.")
                        reminder = input("Enter reminder (YYYY-MM-DD HH:MM AM/PM, press Enter if none): ")
                except ValueError:
                    print("Invalid date format. Please enter a valid date.")

            task = TaskBuilder(description).set_due_date(due_date).set_tags(tags).set_priority(priority).set_reminder(reminder).build()
            manager.add_item(task)
        elif choice == '2':
            description = input("Enter task description to mark as completed: ")
            manager.mark_completed(description)
        elif choice == '3':
            description = input("Enter task description to delete: ")
            manager.delete_item(description)
        elif choice == '4':
            filter_type = input("Enter filter type (all/completed/pending): ")
            items_to_display = manager.view_items(filter_type)

            if filter_type == 'completed':
                if not items_to_display:
                    print("There are no completed tasks in the list.")
                else:
                    print("Task   Status       Priority       Due_date               Reminder")
                    print("*" * 90)
                    for item in items_to_display:
                        print(item.display())
            elif filter_type == 'pending':
                if not items_to_display:
                    print("There are no pending tasks in the list.")
                else:
                    print("Task   Status       Priority       Due_date               Reminder")
                    print("*" * 90)
                    for item in items_to_display:
                        print(item.display())
            else:
                if not items_to_display:
                    print("The list is empty.")
                else:
                    print("Task   Status       Priority       Due_date               Reminder")
                    print("*" * 90)
                    for item in items_to_display:
                        print(item.display())
        elif choice == '5':
            sorted_items_by_priority = manager.sort_items_by_priority()
            for item in sorted_items_by_priority:
                print(item.display())
        elif choice == '6':
            sorted_items_by_due_date = manager.sort_items_by_due_date()
            for item in sorted_items_by_due_date:
                print(item.display())
        elif choice == '7':
            manager.undo()
            if not manager.view_items():
                print("The list is empty.")
        elif choice == '8':
            print("The best preparation for tomorrow is doing your best today")
            print("Have a nice day :)")
            break
        else:
            print("Invalid choice. Please try again.")

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")
