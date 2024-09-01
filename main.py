from db import open_db, read_files_db 

import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Process some flags.")

# Add command-line flags (or arguments)
parser.add_argument('-a', '--analyze', action='store_true', help="Enable analyze mode")
parser.add_argument('-f', '--file', action='store', type=str, help="File path to slack space")
parser.add_argument('-p', '--port', action='store', type=str, help="port number to access server")
parser.add_argument('-s', '--server', action='store_true', type=str, help="Make the file data accessible via server")

# Parse the arguments
args = parser.parse_args()

# Handle the arguments
if args.analyze:
    print("ANALYZING")
if args.server:
    print("HOSTING")



