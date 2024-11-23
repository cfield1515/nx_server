import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# File path for the JSON file
JSON_FILE = "timed_events.json"

# Load events from the JSON file
def load_events():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, "r") as file:
        return json.load(file)

# Save events to the JSON file
def save_events(events):
    with open(JSON_FILE, "w") as file:
        json.dump(events, file, indent=4)

# Refresh the event list in the UI
def refresh_event_list():
    event_list.delete(0, tk.END)
    for idx, event in enumerate(events):
        event_list.insert(tk.END, f"{idx + 1}. {event['EventName']}")

# Add a new event
def add_event():
    event_name = simpledialog.askstring("Event Name", "Enter the event name:")
    if not event_name:
        return

    start_time = simpledialog.askstring("Start Time", "Enter the start time (HH:MM:SS):")
    custom_function = simpledialog.askstring("Custom Function", "Enter the custom function (Lua code):", initialvalue="function() end")

    new_event = {
        "EventName": event_name,
        "EventEnabled": True,
        "StartTime": start_time,
        "CommandRan": False,
        "CustomFunction": custom_function,
        "LastExecuted": None
    }

    events.append(new_event)
    save_events(events)
    refresh_event_list()

# Edit an existing event
def edit_event():
    selected = event_list.curselection()
    if not selected:
        messagebox.showwarning("Select Event", "Please select an event to edit.")
        return

    index = selected[0]
    event = events[index]

    new_event_name = simpledialog.askstring("Event Name", "Edit the event name:", initialvalue=event["EventName"])
    start_time = simpledialog.askstring("Start Time", "Edit the start time (HH:MM:SS):", initialvalue=event["StartTime"])
    custom_function = simpledialog.askstring("Custom Function", "Edit the custom function (Lua code):", initialvalue=event["CustomFunction"])

    events[index] = {
        "EventName": new_event_name,
        "EventEnabled": True,
        "StartTime": start_time,
        "CommandRan": False,
        "CustomFunction": custom_function,
        "LastExecuted": None
    }

    save_events(events)
    refresh_event_list()

# Delete an event
def delete_event():
    selected = event_list.curselection()
    if not selected:
        messagebox.showwarning("Select Event", "Please select an event to delete.")
        return

    index = selected[0]
    del events[index]
    save_events(events)
    refresh_event_list()

# Main program
events = load_events()

root = tk.Tk()
root.title("Event Manager")

# UI Layout
frame = tk.Frame(root)
frame.pack(pady=10)

event_list = tk.Listbox(frame, width=50, height=15)
event_list.pack(side=tk.LEFT, padx=10)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=event_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
event_list.config(yscrollcommand=scrollbar.set)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

add_btn = tk.Button(btn_frame, text="Add Event", command=add_event)
add_btn.grid(row=0, column=0, padx=5)

edit_btn = tk.Button(btn_frame, text="Edit Event", command=edit_event)
edit_btn.grid(row=0, column=1, padx=5)

delete_btn = tk.Button(btn_frame, text="Delete Event", command=delete_event)
delete_btn.grid(row=0, column=2, padx=5)

refresh_event_list()
root.mainloop()
