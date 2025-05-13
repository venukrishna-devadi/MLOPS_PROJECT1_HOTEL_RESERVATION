# from src.logger import get_logger
# from src.custom_exception import CustomException
# import sys

# logger = get_logger(__name__)

# def divide_num(a,b):
#     try:
#         result = a/b
#         logger.info("dividing 2 numbers")
#         return result
#     except Exception as e:
#         logger.error("Error Occured while dividing a and b")
#         raise CustomException("Custom Error Zero", sys)
    
# if __name__ == "__main__":
#     try:
#         logger.info("Starting main problem")
#         divide_num(10,20)
#     except Exception as e:
#         logger.error(str(e))

from google.cloud import storage

client = storage.Client()
buckets = list(client.list_buckets())
print("Buckets:", [bucket.name for bucket in buckets])