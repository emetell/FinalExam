# app/functions.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.db import insert_team, update_team, delete_team, fetch_teams

# Function to handle adding a team
def on_add_team(values, treeview):
    # Call the insert_team function with provided values
    insert_team(*values)
    
    # Refresh the Treeview to display the updated data
    refresh_treeview(treeview)

# Function to handle updating a team
def on_update_team(values, treeview):
    # Call the update_team function with provided values
    update_team(*values)
    
    # Refresh the Treeview to display the updated data
    refresh_treeview(treeview)

# Function to handle deleting a team
def on_delete_team(values, treeview):
    if not values:
        messagebox.showwarning("No Selection", "Please select a team to delete.")
        return

    # Extract the team_id from the values list
    team_id = values[0]

    # Call the delete_team function with the extracted team_id
    delete_team(team_id)
    
    # Refresh the Treeview to display the updated data
    refresh_treeview(treeview)

# Function to refresh the Treeview with the latest team data
def refresh_treeview(treeview):
    if not treeview:
        return

    # Fetch the latest teams from the database
    teams = fetch_teams()

    # Clear existing data in the Treeview
    treeview.delete(*treeview.get_children())

    # Insert the latest teams into the Treeview
    for team in teams:
        treeview.insert('', tk.END, values=team)
