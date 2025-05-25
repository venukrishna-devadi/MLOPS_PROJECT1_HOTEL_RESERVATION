import logging
import os
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok= True)

# now we want give the logfile name and path which we want to create
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m_%d')}.log")

# what info we want to show in the logfile
logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
    # time - info - message
    # levels -  info, warning, error
    level = logging.INFO # levels -  info, warning, error, only these levels will be shown when we do level = logging.INFO. levels above info and info
)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger