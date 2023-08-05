from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae
import numpy as np

import HMF


from ..utils.data_loader import DataLoader


class FeatureEvaluator():
    """This class is responsible for evaluating 1 feature given a set of current 
    features. 

    Return
    ------

    score of the feature
    """
    
    def __init__(self, cv, model_algo, target, data_loader, evaluation_method=None):
        
        self.cv = cv
        self.model_algo = model_algo
        self.target = target
        self.custom_evaluation_method = evaluation_method
        self.data_loader = data_loader
        
    def evaluate_feature(self, current_features, new_feature, i, group_key=None):
        """
        Requirements:
        - read in data
        - create train/valid split ith iter
        - evaluate 
        - return feature name, score tuple
        """
        
        self.current_features = current_features
        self.new_feature = new_feature
        self.i = i
        
        X, y = self.data_loader.load_data(current_features + [new_feature], self.target, group_key=group_key)

        # X, y = self._load_data(current_features, new_feature)
        X_train, X_valid, y_train, y_valid, train_index, valid_index = self._train_valid_split(X, y, i)
        model_algo = self._fit_model(self.model_algo, X_train, y_train)
        score = self._evaluate_model(model_algo, X_valid, y_valid, valid_index)
        
        return score
        

        
    def _train_valid_split(self, X, y, i):
        
        for idx, (train_index, valid_index) in enumerate(self.cv.split(X)):
            
            if idx == i:
                # continue

            
                X_train, y_train = X[train_index], y[train_index]
                X_valid, y_valid = X[valid_index], y[valid_index]

                break

        return X_train, X_valid, y_train, y_valid, train_index, valid_index
        
    
    def _fit_model(self, model_algo, X_train, y_train):
        """may require configurable preprocess steps..."""

        self.model_algo = model_algo
        self.model_algo.fit(X_train, y_train)
        return self.model_algo
        
    
    def _evaluate_model(self, model_algo, X_valid, y_valid, valid_index):

        # if self.custom_evaluation_method:
        #     result = self.custom_evaluation_method(X_valid=X_valid, 
        #         y_valid=y_valid,
        #         valid_index=valid_index,
        #         model_algo=model_algo,
        #         task_manager=self.task_manager,
        #         i=self.i,
        #         cv=self.cv,
        #         self_state=self)
        #     return result
        
        preds = model_algo.predict(X_valid)
        
        rmse_score = np.sqrt(mse(preds, y_valid))
        mae_score = mae(preds, y_valid)
        composite_score = rmse_score/2.0 + mae_score/2.0
        return composite_score

        
        