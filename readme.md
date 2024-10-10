# Flags
-a: Analyze a specified file.

-d: Debug mode for the server.

-e: Send an email as an alert.

-f: Specify the file to analyze.

-l: Logging level. [Info, Debug, Warning, Error]

-p: Port number.

-s: Enable server.

# Example Usage
`Python3 main.py -a -f ./PDF\ Slack\ Files/Image_With_Deleted_PDF.001  -s -p 5001`

In the above command, you utilize the `-a` flag to tell it to analyze a file, the `-f` flag to tell it which file to analyze, the `-s` flag to tell it to start hosting the server (After the analysis), and the `-p` flag to specify the port number.

# Email Alert
In order to send an email alert you must set up an app password with a Gmail account. The gmail account must be the sender address. If these values are not provided but the `-e` flag is used it will throw back a warning and not send the email.

