# main.py
import tkinter as tk
from tkinter import ttk, messagebox

from app.functions import on_add_team, on_update_team, on_delete_team, refresh_treeview
from app.db import create_table

# Define a global variable to use in the functions
global treeview

# Function to create an entry form
def create_entry_form(root, fields, action_callback):
    form = tk.Frame(root)
    form.entries = {}

    # Create labels and entry fields for each form field
    for field in fields:
        tk.Label(form, text=field).grid(row=fields.index(field), column=0, padx=5, pady=5)
        entry_var = tk.StringVar()
        entry = tk.Entry(form, textvariable=entry_var)
        entry.grid(row=fields.index(field), column=1, padx=5, pady=5)
        form.entries[field] = entry_var

    # Create a Submit button that calls the provided action_callback
    tk.Button(form, text="Submit", command=lambda: action_callback(form, treeview)).grid(row=len(fields), columnspan=2, pady=10)

    return form

# Function to handle form submission
def on_submit_form(form, action_callback):
    values = [form.entries[field].get() for field in form.entries]

    # Check if all fields are filled
    if not all(values):
        messagebox.showwarning("Incomplete Form", "Please fill in all fields.")
        return

    # Check if player count is an integer
    try:
        values[-1] = int(values[-1])
    except ValueError:
        messagebox.showwarning("Invalid Player Count", "Player Count must be an integer.")
        return

    # Call the provided action_callback with form values and treeview
    action_callback(values, treeview)
    form.destroy()

# Main function
def main():
    global treeview  # Use the globally defined treeview

    # Create or ensure the table exists
    create_table()

    # Create the main window
    root = tk.Tk()
    root.title("Baseball Teams Management")

    # Create Treeview widget
    treeview = ttk.Treeview(root)
    treeview['columns'] = ('ID', 'Hometown', 'State', 'Team Name', 'Mascot', 'Coach', 'Player Count')

    # Define column headings
    treeview.column('#0', width=0, stretch=tk.NO)
    for col in treeview['columns']:
        treeview.column(col, anchor=tk.W, width=100)
        treeview.heading(col, text=col, anchor=tk.W)

    # Add data to the Treeview
    refresh_treeview(treeview)

    # Add buttons for actions
    add_button = tk.Button(root, text="Add Team", command=lambda: on_add_team_form(root))
    update_button = tk.Button(root, text="Update Team", command=lambda: on_update_team_form(root))
    delete_button = tk.Button(root, text="Delete Team", command=on_delete_team_form)  # Use on_delete_team_form

    # Place widgets on the window
    treeview.pack(padx=10, pady=10)
    add_button.pack(pady=5)
    update_button.pack(pady=5)
    delete_button.pack(pady=5)

    # Start the main loop
    root.mainloop()

# Function to handle the "Add Team" form
def on_add_team_form(root):
    fields = ['Hometown', 'State', 'Team Name', 'Mascot', 'Coach', 'Player Count']
    form = create_entry_form(root, fields, on_submit_add_team)
    form.pack(pady=10)

# Function to handle the "Update Team" form
def on_update_team_form(root):
    fields = ['Hometown', 'State', 'Team Name', 'Mascot', 'Coach', 'Player Count']
    form = create_entry_form(root, fields, on_submit_update_team)
    form.pack(pady=10)

# Function to handle the "Delete Team" form
def on_delete_team_form():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a team to delete.")
        return

    # Get the ID from the selected Treeview item
    team_id = treeview.item(selected_item, "values")[0]

    # Call the delete function with the ID and treeview
    on_delete_team(team_id, treeview)

# Function to handle the "Add Team" form submission
def on_submit_add_team(form, treeview):
    on_submit_form(form, on_add_team)

# Function to handle the "Update Team" form submission
def on_submit_update_team(form, treeview):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a team to update.")
        return

    # Get the values from the form
    values = [form.entries[field].get() for field in form.entries]

    # Check if player count is an integer
    try:
        values[-1] = int(values[-1])
    except ValueError:
        messagebox.showwarning("Invalid Player Count", "Player Count must be an integer.")
        return

    # Get the ID from the selected Treeview item
    team_id = treeview.item(selected_item, "values")[0]
    
    # Call the update function with the ID and values
    on_update_team([team_id] + values, treeview)
    form.destroy()

# Entry point for the script
if __name__ == "__main__":
    main()
