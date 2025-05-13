from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import *
from config.paths_config import *


if __name__ == "__main__":

    #1. Data Ingestion
    # create data ingestion class object, read_yaml for reading yaml file
    data_ingestion_obj = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion_obj.run()

    # 2. Data Processing
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR,CONFIG_PATH)
    processor.process_data()

    # 3. Model Training
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    trainer.run()
