import os
import pandas
import joblib # for model saving
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from utils.common_functions import load_data,read_yaml
from config.model_params import *
from config.paths_config import *
from src.custom_exception import CustomException
from scipy.stats import randint
from utils.common_functions import get_logger

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:

    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.param_dist = HISTGB_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):

        try:
            logger.info("Loading and data split started")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns='booking_status')
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns = "booking_status")
            y_test = test_df["booking_status"]

            logger.info("Data loaded succesfully for model training.")
            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error(f"Unable to load data and split the data - {e}")
            raise CustomException("Error occured during loading the data - ", e)
        
    def train_histgb(self, X_train, y_train):

        try:
            logger.info("Started model HistGradientBoosting initialization")
            model = HistGradientBoostingClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Started Hyperparameter fine tuning the model")
            random_search = RandomizedSearchCV(
                estimator=model,
                param_distributions=self.param_dist,
                n_iter=self.random_search_params["n_iter"],
                cv=self.random_search_params["cv"],
                n_jobs=self.random_search_params["n_jobs"],
                verbose=self.random_search_params["verbose"],
                random_state=self.random_search_params["random_state"],
                scoring=self.random_search_params["scoring"]
            )
            random_search.fit(X_train, y_train)
            logger.info("Hyperparamter fine tuning completed")
            
            best_params = random_search.best_params_
            best_model = random_search.best_estimator_
            logger.info(f"Best params are {best_params}")
            logger.info("Returning the best model")
            return best_model
        
        except Exception as e:
            logger.error(f"Error occured during model training - {e}")
            raise CustomException("Model Training Unsucesful", e)
        
    def model_evaluation(self, X_test, y_test, model):

        try:
            logger.info("Model Evaluation STarted")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)

            logger.info(f"Model Accuracy is : {accuracy}")
            logger.info(f"Model Precision is {precision}")
            logger.info(f"Model Recall is {recall}")
            logger.info(f"Model F1 Score is {f1}")

            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }
        except Exception as e:
            logger.error(f"Error Occured during Model Evaluation - {e}")
            raise CustomException("Model Evaluation Error - ", e)
        
    def save_model(self, model):

        try:
            logger.info("Saving the best model")
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok= True)
            joblib.dump(model, self.model_output_path)
            logger.info("Model saved succesfully")

        except Exception as e:
            logger.error(f"Error occured during saving the model - {e}")
            raise CustomException("Failed to save the model", e)
        
    def run(self):
        
        try:
            with mlflow.start_run():

                logger.info("Starting our model training pipeline")
                logger.info("Starting our ml flow experimentation")
                # we want to log our dataset
                
                # wshich dataset was used to train this particular model
                logger.info("Logging the training and testing datasetto MLFLOW")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                # we also need to log the model, which model is trained like the model version
                logger.info("Logging the model into ML Flow")
                mlflow.log_artifact(self.model_output_path)

                
                X_train, y_train, X_test, y_test = self.load_and_split_data()
                best_histgb_model = self.train_histgb(X_train, y_train)
                metrics = self.model_evaluation(X_test, y_test, best_histgb_model)
                self.save_model(best_histgb_model)

                # Now we here we have to log our parameters used metrics
                logger.info("Logging Metrics and Params to ML-FLow")
                mlflow.log_params(best_histgb_model.get_params())
                mlflow.log_metrics(metrics)
                

                logger.info("Model Training pipeline successfully completed")
        
        except Exception as e:
            logger.error(f"Error occured while model training pipeline- {e}")
            raise CustomException("Error occured during model training pipeline", e)
        
if __name__ == "__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    trainer.run()

            
