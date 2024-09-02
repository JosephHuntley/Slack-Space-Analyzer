from db import open_db, read_files_db 
from cmd_arguments import args
from alert import send_email
from slack_space import analyze_slack

# For dev purposes
file = None

# Handle the arguments
if args.analyze:
    analyze_slack(file)
if args.server:
    print("HOSTING")
