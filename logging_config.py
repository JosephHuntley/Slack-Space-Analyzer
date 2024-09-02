import logging
import configparser
from cmd_arguments import args

# Read the configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# If --log-level argument is provided, use that, otherwise fall back to config file
log_level = args.logging if args.logging else config.get('logging', 'level', fallback='INFO')


# Convert the log level string to the corresponding logging level constant
log_level = getattr(logging, log_level.upper(), logging.INFO)

# Configure the logger
logger = logging.getLogger('Slack Space Analyzer')
logger.setLevel(log_level)

# Create a file handler
file_handler = logging.FileHandler('slack_analyzer.log')
file_handler.setLevel(log_level)


# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# Create a formatter and attach it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Avoid adding the handler multiple times if the logger is reused
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

logger.info("Logger Created")
