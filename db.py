import sqlite3
import logging

# 
logger = logging.getLogger(__name__)

def open_db():
    # Purpose: Open's the SQL Lite DB file

    # Return: Db connection

    try:
        conn = sqlite3.connect('Files.db')
    
    except con.DatabaseError:
        print("Unable to open Database.")
        exit(0)

    # Logs a connection message
    logger.info("Database opened successfully")

    return conn

def read_files_db(conn):
    # Purpose: Read all the file entries from the db

    # Return: The list of files

    # SQL Query 
    query = "SELECT * FROM Files"

    # Query result
    results = conn.execute(query)

    return results.fetchall()