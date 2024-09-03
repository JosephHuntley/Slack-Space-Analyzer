from db import open_db, read_files_db 
from cmd_arguments import args
from alert import send_email
from slack_space import analyze_slack

# For dev purposes
file = None

# Connect to the DB
conn = open_db()

# Handle the arguments
if args.analyze:
    analyze_slack(conn, file)
if args.server:
    print("HOSTING")



