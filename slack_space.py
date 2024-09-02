from cmd_arguments import args
from alert import send_email


def analyze_slack(file):
    print("ANALYZING")
    # Open File

    # Window through binary

    # Regex file header signatures

    # Compare with known signatures

    # Create file obj

    # Add file to database
    
    # Alert user if -e flag is used
    if(args.email):
        send_email()