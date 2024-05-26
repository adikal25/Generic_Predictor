
from src.exception import CustomException
import pickle
import os
import sys


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)  # Create directory if it doesn't exist
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)
