import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
from logging_config import logger

# Read the configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Set up your email information
sender_email = config.get('alert', 'sender', fallback = '')
receiver_email = config.get('alert', 'receiver', fallback = '')
password = config.get('alert', 'app_password', fallback = '')

# Set up the email content
subject = config.get('alert', 'subject', fallback = "Alert from Slack Space Analyzer")
body = config.get('alert', 'body', fallback = "The Slack Space Analyzer has  completed its analysis.")

# Create the email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject


# Attach the body text to the email
message.attach(MIMEText(body, "plain"))

# Gmail SMTP server configuration
smtp_server = config.get('alert', 'smtp_server', fallback = "smtp.gmail.com")
smtp_port = config.get('alert', 'smtp_port', fallback = "587") 

def send_email():
    # Checks if email details are included in config.ini file
    if sender_email == '' or receiver_email == '' or password == '':
        logger.warning("Please add sender, receiver, and password into config.ini file")
        exit(0)

    # Log the email details for debugging
    logger.debug(f"From: {sender_email}")
    logger.debug(f"To: {receiver_email}")
    logger.debug(f"SMTP Server: {smtp_server}")
    logger.debug(f"SMTP Port: {smtp_port}")

    # Sending the emails
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection

        # Login to your email account
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

        logger.info("Email sent successfully!")

    except Exception as e:
        logger.error(f"Failed to send email. Error: {e}")

    finally:
        # Close the connection
        server.quit()
