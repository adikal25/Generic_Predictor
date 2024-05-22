import logging
import os
from datetime import datetime

# Define the logging format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - Line %(lineno)d - %(message)s"

# Create the log file name with the current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define the logs directory path
logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)

# Define the full log file path
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format=LOG_FORMAT,
    level=logging.INFO,
)

