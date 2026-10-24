
import json
import os

FILE_NAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved tasks.")
        return []


def save_tasks(tasks):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(tasks, file, indent=4)
    except OSError:
        print("Error: Could not save tasks.")


def add_task(tasks):
    title = input("Enter task title: ").strip()
    subject = input("Enter subject: ").strip()

    if not title or not subject:
        print("Title and subject cannot be empty.")
        return

    priority = input("Priority (High/Medium/Low): ").strip().capitalize()

    if priority not in ["High", "Medium", "Low"]:
        print("Invalid priority. Setting it to Medium.")
        priority = "Medium"

    task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        "title": title,
        "subject": subject,
        "priority": priority,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")


def view_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n--- YOUR TASKS ---")

    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        print(
            f'ID: {task["id"]} | '
            f'Title: {task["title"]} | '
            f'Subject: {task["subject"]} | '
            f'Priority: {task["priority"]} | '
            f'Status: {status}'
        )


def complete_task(tasks):
    view_tasks(tasks)

    if not tasks:
        return

    try:
        task_id = int(input("Enter task ID to complete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print("Task marked as completed!")
            return

    print("Task ID not found.")


def delete_task(tasks):
    view_tasks(tasks)

    if not tasks:
        return

    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print("Task deleted successfully!")
            return

    print("Task ID not found.")


def main():
    tasks = load_tasks()

    while True:
        print("\n===== STUDENT TASK MANAGER =====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Thank you for using Student Task Manager!")
            break
        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()
