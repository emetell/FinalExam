# app/db.py
import sqlite3

# Function to get a database connection
def get_conn(db_file):
    conn = sqlite3.connect(database=db_file)
    return conn

# Function to execute a SQL query
def execute(sql, db_file="baseball_teams.db"):
    with get_conn(db_file=db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)

    conn.commit()
    conn.close()

# Function to create the baseball_teams table if it doesn't exist
def create_table(db_file="baseball_teams.db"):
    # Create the table if it doesn't exist
    execute('''
        CREATE TABLE IF NOT EXISTS baseball_teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hometown TEXT,
            state TEXT,
            team_name TEXT,
            mascot TEXT,
            coach TEXT,
            player_count INTEGER
        )
    ''')

# Function to insert a team into the database
def insert_team(hometown, state, team_name, mascot, coach, player_count):
    conn = sqlite3.connect('baseball_teams.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO baseball_teams (hometown, state, team_name, mascot, coach, player_count)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (hometown, state, team_name, mascot, coach, player_count))

    conn.commit()
    conn.close()

# Function to update a team in the database
def update_team(team_id, hometown, state, team_name, mascot, coach, player_count):
    conn = sqlite3.connect('baseball_teams.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE baseball_teams
        SET hometown=?, state=?, team_name=?, mascot=?, coach=?, player_count=?
        WHERE id=?
    ''', (hometown, state, team_name, mascot, coach, player_count, team_id))

    conn.commit()
    conn.close()

# Function to delete a team from the database
def delete_team(team_id):
    conn = sqlite3.connect('baseball_teams.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM baseball_teams WHERE id=?', (team_id,))

    conn.commit()
    conn.close()

# Function to fetch all teams from the database
def fetch_teams():
    conn = sqlite3.connect('baseball_teams.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM baseball_teams')
    teams = cursor.fetchall()

    conn.close()

    return teams
