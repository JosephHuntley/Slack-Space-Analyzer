from cmd_arguments import args
from alert import send_email
from db import create_file_db
from file import File
from datetime import datetime
from file_signatures import check_file_signature, signatures_dict
from logging_config import logger


def analyze_slack(conn, slack_file):
    print("ANALYZING...")
    # Open File
    logger.debug(f"Opening file: {slack_file}")
    with open(slack_file, "rb") as sf:
        lines = sf.readlines()

        for line in lines:
            print(line)

    # Window through binary

    # Regex file header signatures
    file_header = b'\x4D\x53\x57\x49\x4D' # Example for testing purposes - WIM file

    if file_header:
        # Compare with known signatures
        file_extension, description = check_file_signature(file_header, signatures_dict)
        logger.debug(f'{file_header} - {file_extension} - {description}')

        # Create file obj
        file = File( 'name', file_extension, 123, datetime.now(), '0x45 0x76 0xAB 0xFF' )

        # Add file to database
        create_file_db(conn, file)
    
    # Alert user if -e flag is used
    if(args.email):
        send_email()