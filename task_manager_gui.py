
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE_NAME = "tasks.json"


def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            messagebox.showwarning(
                "Warning", "Could not load saved tasks."
            )
    return []


def save_tasks():
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(tasks, file, indent=4)
    except OSError:
        messagebox.showerror("Error", "Could not save tasks.")


def refresh_tasks():
    task_list.delete(*task_list.get_children())

    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        task_list.insert(
            "",
            "end",
            iid=str(task["id"]),
            values=(
                task["title"],
                task["subject"],
                task["priority"],
                status
            )
        )


def add_task():
    title = title_entry.get().strip()
    subject = subject_entry.get().strip()
    priority = priority_box.get()

    if not title or not subject:
        messagebox.showwarning(
            "Missing Information",
            "Please enter both a task title and subject."
        )
        return

    task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        "title": title,
        "subject": subject,
        "priority": priority,
        "completed": False
    }

    tasks.append(task)
    save_tasks()
    refresh_tasks()

    title_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Task added successfully!")


def complete_task():
    selected = task_list.selection()

    if not selected:
        messagebox.showwarning(
            "Select Task", "Please select a task first."
        )
        return

    task_id = int(selected[0])

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks()
            refresh_tasks()
            return


def delete_task():
    selected = task_list.selection()

    if not selected:
        messagebox.showwarning(
            "Select Task", "Please select a task to delete."
        )
        return

    task_id = int(selected[0])

    if messagebox.askyesno(
        "Confirm Delete", "Are you sure you want to delete this task?"
    ):
        tasks[:] = [task for task in tasks if task["id"] != task_id]
        save_tasks()
        refresh_tasks()


tasks = load_tasks()

root = tk.Tk()
root.title("Student Task Manager")
root.geometry("850x550")
root.minsize(700, 450)
root.configure(bg="#F1F5F9")

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    rowheight=30,
    font=("Arial", 10)
)
style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)

heading = tk.Label(
    root,
    text="STUDENT TASK MANAGER",
    font=("Arial", 22, "bold"),
    bg="#F1F5F9",
    fg="#1E3A8A"
)
heading.pack(pady=18)

form = tk.Frame(root, bg="white", padx=15, pady=15)
form.pack(fill="x", padx=25)

tk.Label(form, text="Task Title", bg="white").grid(
    row=0, column=0, sticky="w", padx=5
)
title_entry = ttk.Entry(form, width=25)
title_entry.grid(row=1, column=0, padx=5, pady=8)

tk.Label(form, text="Subject", bg="white").grid(
    row=0, column=1, sticky="w", padx=5
)
subject_entry = ttk.Entry(form, width=20)
subject_entry.grid(row=1, column=1, padx=5, pady=8)

tk.Label(form, text="Priority", bg="white").grid(
    row=0, column=2, sticky="w", padx=5
)
priority_box = ttk.Combobox(
    form,
    values=["High", "Medium", "Low"],
    state="readonly",
    width=12
)
priority_box.set("Medium")
priority_box.grid(row=1, column=2, padx=5, pady=8)

add_button = tk.Button(
    form,
    text="Add Task",
    command=add_task,
    bg="#2563EB",
    fg="white",
    padx=12,
    pady=6
)
add_button.grid(row=1, column=3, padx=8)

table_frame = tk.Frame(root, bg="#F1F5F9")
table_frame.pack(fill="both", expand=True, padx=25, pady=18)

columns = ("Title", "Subject", "Priority", "Status")

task_list = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)

for column in columns:
    task_list.heading(column, text=column)
    task_list.column(column, width=150, anchor="center")

task_list.pack(fill="both", expand=True)

buttons = tk.Frame(root, bg="#F1F5F9")
buttons.pack(pady=(0, 18))

tk.Button(
    buttons,
    text="Mark Completed",
    command=complete_task,
    bg="#15803D",
    fg="white",
    padx=12,
    pady=7
).pack(side="left", padx=8)

tk.Button(
    buttons,
    text="Delete Task",
    command=delete_task,
    bg="#DC2626",
    fg="white",
    padx=12,
    pady=7
).pack(side="left", padx=8)

refresh_tasks()
root.mainloop()
