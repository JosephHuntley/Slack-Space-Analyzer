from db import open_db, read_files_db 
from cmd_arguments import args
from alert import send_email


# Handle the arguments
if args.analyze:
    print("ANALYZING")
if args.server:
    print("HOSTING")
