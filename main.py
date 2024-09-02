from db import open_db, read_files_db 
from cmd_arguments import args


# Handle the arguments
if args.analyze:
    print("ANALYZING")
if args.server:
    print("HOSTING")

conn = open_db()
read_files_db(conn)


