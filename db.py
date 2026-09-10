import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent #find project folder
DB_PATH = BASE_DIR / "fundraising.db"

def get_connection():
    connection = sqlite3.connect(DB_PATH) #open database
    connection.row_factory = sqlite3.Row #Enable access to columns using name
    connection.execute("PRAGMA foreign_keys = ON") #enforce foreign keys
    return connection