from cmd_arguments import args
from alert import send_email
from db import create_file_db
from file import File
from datetime import datetime


def analyze_slack(conn, slack_file):
    print("ANALYZING")
    # Open File

    # Window through binary

    # Regex file header signatures

    # Compare with known signatures

    # Create file obj
    file = File( 'name', 'ext', 123, datetime.now(), '0x45 0x76 0xAB 0xFF' )

    # Add file to database
    create_file_db(conn, file)
    
    # Alert user if -e flag is used
    if(args.email):
        send_email()