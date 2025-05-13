import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:

    def __init__(self,train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config_path = read_yaml(config_path)

        # Now we will create the processed dir, to store the processed data
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self, df):
        try:
            logger.info("Starting data preprocessing steps-")

            logger.info("Dropping columns - Unnamed: 0', 'Booking_ID")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'] , inplace=True)
            logger.info("Drop duplicates")        
            df.drop_duplicates(inplace=True)

            logger.info("Starting Label Encoding")
            label_encoder = LabelEncoder()

            cat_columns = self.config_path["data_processing"]["categorical_columns"]
            num_columns = self.config_path["data_processing"]["numerical_columns"]
            
            mappings={}
            
            for col in cat_columns:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label,code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}

            logger.info("Label Mappings are -")
            for col,mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            logger.info("Doing Skewness Handling")
            skew_threshold = self.config_path["data_processing"]["skewness_threshold"]
            skewness  = df[num_columns].apply(lambda x:x.skew())
            for col in skewness[skewness>skew_threshold].index:
                df[col] = np.log1p(df[col])
            logger.info("Data Skewness Handling Completed")
            
            return df

        except Exception as e:
            logger.error(f"Error during data pre-processing - {e}")
            raise CustomException("Error while performing data preprocessing", e)

    def balanced_data(self, df):

            
        try:
            logger.info("Starting Imbalanced Data Handling")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]  

            smote = SMOTE(random_state=99)
            X_res , y_res = smote.fit_resample(X,y)
            balanced_df = pd.DataFrame(X_res , columns=X.columns)
            balanced_df["booking_status"] = y_res
            logger.info("Data balanced successfully")

            return balanced_df

        except Exception as e:
            logger.error(f"Error during balancing dataset - {e}")
            raise CustomException("Error - ",e)
                
    def feature_selection(self, df):    
        try:
            logger.info("Starting Feature Selection")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            model = RandomForestClassifier(random_state=42)
            model.fit(X,y)
            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                    'feature':X.columns,
                    'importance':feature_importance})
            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)
            
            top_10_features = top_features_importance_df["feature"].head(self.config_path["data_processing"]["top_features"]).values
            logger.info(f"Features Selected: {top_10_features}")
            top_10_df = df[top_10_features.tolist() + ["booking_status"]]
            
            logger.info("Feature Selection Completed Succesfully")
            return top_10_df
        
        except Exception as e:
            logger.error(f"Error during feature selection -{e}")
            raise CustomException("Error - ",e)
                
    # now we need to save the data in csv format
    def save_data(self, df, file_path):
         
        try:
            logger.info("Saving the data in processed folder")
            df.to_csv(file_path, index = False)
            logger.info(f"Data Saved succesfully to {file_path}")

        except Exception as e:
            logger.error("Error during saving the data")
            raise CustomException("Error - ", e)
        
    # now how we had made def run(self) and under this function we mentioned the sequence of operations, we do the same below
    def process_data(self):
        try:
            logger.info("Starting Data Processing")
            logger.info("Loading raw data from artifacts")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balanced_data(train_df)
            
            train_df = self.feature_selection(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data preprocessing completed succesfully")

        except Exception as e:
            logger.error(f"Unable to perform data preprocessing - {e}")
            raise CustomException("Error during data preprocessing - ",e)
        
if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR,CONFIG_PATH)
    processor.process_data()

            


         
