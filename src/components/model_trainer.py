import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_models, save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifact", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_arr, test_arr):
        try:
            logging.info(
                "Splitting training and test input data from data transformation")
            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            models = {
                "RandomForest": RandomForestRegressor(),
                "DecisionTree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoostRegressor": CatBoostRegressor(verbose=False),
                "AdaBoostRegressor": AdaBoostRegressor()
            }

            params = {
                "RandomForest": {
                    'n_estimators': [2, 4, 8, 16, 32, 64, 128, 256],
                    'max_depth': [10, None],
                    'min_samples_split': [2, 5]
                },
                "DecisionTree": {
                    'max_depth': [10, None],
                    'min_samples_split': [2, 5]
                },
                "Gradient Boosting": {
                    'n_estimators': [2, 4, 8, 16, 32, 64, 128, 256],
                    'learning_rate': [0.01, 0.1],
                    'max_depth': [3, 5]
                },
                "Linear Regression": {
                    'fit_intercept': [True, False]
                },
                "K-Neighbors Regressor": {
                    'n_neighbors': [3, 5],
                    'weights': ['uniform', 'distance']
                },
                "XGBRegressor": {
                    'n_estimators': [2, 4, 8, 16, 32, 64, 128, 256],
                    'learning_rate': [0.01, 0.1],
                    'max_depth': [3, 5]
                },
                "CatBoostRegressor": {
                    'iterations': [2, 4, 8, 16, 32, 64, 128, 256],
                    'learning_rate': [0.01, 0.1],
                    'depth': [4, 6]
                },
                "AdaBoostRegressor": {
                    'n_estimators': [2, 4, 8, 16, 32, 64, 128, 256],
                    'learning_rate': [0.01, 0.1]
                }
            }

            model_report: dict = evaluate_models(
                X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, param=params
            )

            best_model_score = max(model_report.values())
            best_model_name = [
                name for name, score in model_report.items() if score == best_model_score][0]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            r2 = r2_score(y_test, predicted)
            return r2

        except Exception as e:
            raise CustomException(str(e), sys)

