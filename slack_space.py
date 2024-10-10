from cmd_arguments import args
from alert import send_email
from db import open_db, create_file_db
from file import File
from datetime import datetime
from logging_config import logger
import os

# PDF magic number and EOF marker
PDF_MAGIC_NUMBER = b'%PDF'
PDF_EOF_MARKER = b'%%EOF'
WINDOW_SIZE = 4096  # 4 KB window size

def analyze_slack( slack_file):
    print("ANALYZING....")
    logger.debug(f"Opening file: {slack_file}")

    # Connect to the DB
    conn = open_db()
    
    with open(slack_file, "rb") as sf:
        logger.debug(f"Opened file... {slack_file}")
        
        # Search for the PDF in slack space
        start_offset, end_offset = search_for_pdf(sf)
        
        if start_offset:
            logger.debug(f"PDF file detected in {slack_file}.")
            
            # Create file object
            file = File(
                'pdf',               # File extension
                start_offset,
                end_offset,
                os.path.abspath(slack_file) 
            )
            
            # Add file to database
            create_file_db(conn, file)
            logger.debug("Recovered PDF file added to database.")
        else:
            logger.debug("No PDF file found in the slack space.")

    # Alert user if -e flag is used
    if args.email:
        send_email()


def search_for_pdf(file):
    """Search through the file in windows, looking for PDF magic number and EOF marker."""
    file_start_pos = None  # Position where PDF starts
    buffer = b''  # Buffer to accumulate windowed content
    pdf_start_offset = -1
    pdf_end_offset = -1

    while chunk := file.read(WINDOW_SIZE):
        buffer += chunk

        # If we haven't found the PDF magic number yet, look for it
        if file_start_pos is None:
            pdf_start_offset = buffer.find(PDF_MAGIC_NUMBER)
            if pdf_start_offset != -1:
                # Found the PDF magic number
                file_start_pos = file.tell() - len(buffer) + pdf_start_offset
                logger.debug(f"PDF magic number found at offset {file_start_pos}.")

        # If the PDF start is found, now search for EOF marker
        if file_start_pos is not None:
            pdf_end_offset = buffer.find(PDF_EOF_MARKER)
            if pdf_end_offset != -1:
                # Found the EOF marker, extract and return the PDF content
                file_end_pos = file.tell() - len(buffer) + pdf_end_offset + len(PDF_EOF_MARKER)
                logger.debug(f"EOF marker found at offset {file_end_pos}.")
                
                # Extract and return the data between the start and EOF
                return pdf_start_offset, pdf_end_offset

        # Keep the last portion of the buffer to avoid missing data split between chunks
        if file_start_pos is None:
            # If we haven't found the PDF, discard the earlier part of the buffer
            buffer = buffer[-len(PDF_MAGIC_NUMBER):]
        else:
            # If we found a PDF but not the EOF, keep everything after the PDF start
            buffer = buffer[-WINDOW_SIZE:]

    # If we reach here, it means no valid PDF with both magic number and EOF was found
    logger.debug("No complete PDF found in the file.")
    return None
