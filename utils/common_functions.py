# Now we have to create a function for reading yaml file
# we will read the yaml file at various steps, data ingestion and data processing

import os
import pandas
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml
import pandas as pd
logger = get_logger(__name__)

# create a function to read yaml file
def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File is not present in the given path")
        
        with open(file_path, "r") as yaml_file:
            config_file = yaml.safe_load(yaml_file)
            logger.info("Successfully Loaded Config yaml file")
            return config_file
        
    except CustomException as e:
        logger.error("Error reading the yaml file")
        raise CustomException("Failed to read yaml file", e)


def load_data(path):
    try:
        logger.info("Loading Data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error("Error Loading the data.")
        raise CustomException("Error while loading the csv data", e)