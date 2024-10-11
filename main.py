'''
Name: Joseph Huntley
Class: CYBR-260-40
Date Oct 11th, 2024
Desc:
    The application searches through a provided image of a drive for files.
'''
from db import read_files_db, init_db
from cmd_arguments import args
from alert import send_email
from slack_space import analyze_slack
from server import start_server
from logging_config import logger

# For debug purposes
logger.debug("Starting application...")

# Initializes the database
init_db()

# Handle the arguments
if args.analyze:
    file = args.file
    if file == None:
        logger.warning("No file was provided to analyze. Please provide a file with -f flag.")
        exit(0)
    analyze_slack(file)

if args.server:
    start_server()



