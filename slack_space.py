from cmd_arguments import args
from alert import send_email
from db import open_db, create_file_db
from file import File
from datetime import datetime
from logging_config import logger
import os, io, zipfile

WINDOW_SIZE = 4096  # 4 KB window size

def analyze_slack(slack_file):
    # function: analyze_slack

    # purpose: Analyze the slack space provided with the -f flag. 

    # inputs: 
        # slack_file: The file provided with the -f flag.

    # returns:
    
    # Logging and prints message for user
    print("ANALYZING....")
    logger.info("Analyzing....")
    logger.debug(f"Opening file: {slack_file}")

    # Connect to the DB
    conn = open_db()
    
    with open(slack_file, "rb") as sf:
        logger.debug(f"Opened file... {slack_file}")
        
        # Search for files in slack space
        search_for_pdf(slack_file, conn)
        search_for_jpeg(slack_file, conn)

    # Alert user if -e flag is used
    if args.email:
        send_email()


def search_for_pdf(file_path, conn):
    # function: search_for_pdf

    # purpose: Searches for PDF files in the slack space.

    # inputs: 
        # file_path: The File containing the slack space to be examined for PDF files.
        # conn: DB Connection

    # returns: 

    # PDF magic number and EOF marker
    PDF_MAGIC_NUMBER = b'%PDF'
    PDF_EOF_MARKER = b'%%EOF'

    logger.info("Searching for PDF files in slack space.")

    logger.debug(f"Opening file: {file_path}")
    with open(file_path, 'rb') as sf:

        file_start_pos = None  # Position where PDF starts
        buffer = b''  # Buffer to accumulate windowed content
        pdf_start_offset = -1
        pdf_end_offset = -1

        while chunk := sf.read(WINDOW_SIZE):
            buffer += chunk

            # If we haven't found the PDF magic number yet, look for it
            if file_start_pos is None:
                pdf_start_offset = buffer.find(PDF_MAGIC_NUMBER)
                if pdf_start_offset != -1:
                    # Found the PDF magic number
                    file_start_pos = sf.tell() - len(buffer) + pdf_start_offset
                    logger.debug(f"PDF magic number found at offset {file_start_pos} - {hex(file_start_pos)}.")

            # If the PDF start is found, now search for EOF marker
            if file_start_pos is not None:
                pdf_end_offset = buffer.find(PDF_EOF_MARKER)
                if pdf_end_offset != -1:
                    # Adjust the pdf_end_offset to account for the length of the EOF marker
                    pdf_end_offset += len(PDF_EOF_MARKER)
                    file_end_pos = sf.tell() - len(buffer) + pdf_end_offset
                    logger.debug(f"PFD EOF found at offset {file_end_pos} - {hex(file_end_pos)}")
                    logger.debug(f"PDF file detected in {sf}.")

                    # Create file object with correct offsets
                    file = File(
                        'pdf',               
                        file_start_pos,
                        file_end_pos,         
                        os.path.abspath(file_path) 
                    )
                    
                    # Add file to database
                    create_file_db(conn, file)
                    logger.debug("Recovered PDF file added to database.")

                    # Stop once a PDF is found (optional, if looking for multiple PDFs, remove this break)
                    break

            # Keep the last portion of the buffer to avoid missing data split between chunks
            if file_start_pos is None:
                # If we haven't found the PDF, discard the earlier part of the buffer
                buffer = buffer[-len(PDF_MAGIC_NUMBER):]
            else:
                # If we found a PDF but not the EOF, keep everything after the PDF start
                buffer = buffer[-WINDOW_SIZE:]

        # If we reach here, it means no valid PDF with both magic number and EOF was found
        if pdf_start_offset == -1 or pdf_end_offset == -1:
            logger.debug("No complete PDF found in the file.")

def search_for_jpeg(file_path, conn):
    # function: search_for_jpeg

    # purpose: Search for JPEG files in the slack space.

    # inputs: 
        # file_path: The file containing the slack space to search JPEG files for.
        # conn: The database connection 

    # returns:

    JPEG_MAGIC_NUMBER = b'\xFF\xD8'  # JPEG Start of Image (SOI) marker
    JPEG_END_MARKER = b'\xFF\xD9'    # JPEG End of Image (EOI) marker

    logger.info("Searching for JPEG files in slack space.")

    logger.debug(f"Opening file: {file_path}")
    with open(file_path, "rb") as f:
        buffer = b''  # Buffer to accumulate windowed content
        file_start_pos = None  # Position where JPEG starts

        while chunk := f.read(WINDOW_SIZE):
            buffer += chunk

            # Search for JPEG SOI (magic number)
            if file_start_pos is None:
                jpeg_start_offset = buffer.find(JPEG_MAGIC_NUMBER)
                if jpeg_start_offset != -1:
                    # Found the JPEG start of image (SOI) marker
                    file_start_pos = f.tell() - len(buffer) + jpeg_start_offset
                    logger.debug(f"JPEG SOI marker found at offset {file_start_pos} - {hex(file_start_pos)}.")

            # If JPEG SOI is found, search for EOI (end of image) marker
            if file_start_pos is not None:
                jpeg_end_offset = buffer.find(JPEG_END_MARKER)
                if jpeg_end_offset != -1:
                    # Adjust the jpeg_end_offset to account for the length of the EOI marker
                    jpeg_end_offset += len(JPEG_END_MARKER)
                    file_end_pos = f.tell() - len(buffer) + jpeg_end_offset
                    logger.debug(f"JPEG EOI marker found at offset {file_end_pos} - {hex(file_end_pos)}.")
                    
                    # Create file object with correct offsets
                    file = File(
                        'jpeg',              # File extension
                        file_start_pos,
                        file_end_pos,        # Use actual file end position
                        os.path.abspath(file_path)  # Absolute file path
                    )

                    # Add file to database
                    create_file_db(conn, file)
                    logger.debug("Recovered JPEG file added to database.")

                    # Stop after the first JPEG is found (or remove this break to search for multiple JPEGs)
                    break

            # Keep the last portion of the buffer to avoid missing data split between chunks
            if file_start_pos is None:
                # If we haven't found the JPEG SOI, discard the earlier part of the buffer
                buffer = buffer[-len(JPEG_MAGIC_NUMBER):]
            else:
                # If we found a JPEG but not the EOI, keep everything after the JPEG start
                buffer = buffer[-WINDOW_SIZE:]

    logger.debug(f"No JPEG file found in {file_path}.")