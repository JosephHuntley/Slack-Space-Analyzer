import sqlite3
from logging_config import logger
from file import File



def open_db():
    # Purpose: Open's the SQL Lite DB file

    # Return: Db connection

    try:
        conn = sqlite3.connect('Files.db')
        
        # Logs a connection message
        logger.info("Database opened successfully")
    
    except conn.DatabaseError:
        logger.error("Unable to open Database.")

    return conn

def read_files_db(conn):
    # Purpose: Read all the file entries from the db

    # Return: The list of files or None in case of error

    try:
        # SQL Query 
        query = "SELECT * FROM Files"

        # Query result
        results = conn.execute(query)

    except conn.DatabaseError as e:
        logger.error(f'Unable to read from the database due to the following reason - {e}')
        return None

    return results.fetchall()

def create_file_db(conn, file):
    # Purpose: Create new file in the db

    # Return: Successful or not

    if not isinstance(file, File):
        logger.error(f'{type(file)} is not of type File')
        logger.info('File was not uploaded into the database')
        return False

    cursor = conn.cursor()

   # Use parameterized query to insert data
    query = "INSERT INTO Files (extension, starting_offset, ending_offset, filepath) VALUES (?, ?, ?, ?)"

    # Log the query before execution for debugging
    logger.debug(f"Executing query: {query} with values: ({file.file_type}, {hex(file.starting_offset)}, {hex(file.ending_offset)}, {file.filepath})")

    try:
        # Execute with parameters safely
        cursor.execute(query, (
            file.file_type,                   # PDF extension
            hex(file.starting_offset),        # Starting offset in hex format
            hex(file.ending_offset),          # Ending offset in hex format
            file.filepath                     # Absolute file path
        ))
        logger.debug("Data inserted successfully.")
        
        # Commit the transaction after successful insertion
        conn.commit()
    except sqlite3.DatabaseError as e:
        logger.error(f'Unable to write to database due to the following reason - {e}')
        return False  # Insertion failed
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        return False  # Catch-all for other exceptions
    
    return True