
from collections import defaultdict
import numpy as np

class ParallelFeatureEvaluator():
    
    def __init__(self, feature_evaluator, dask_client):
        
        self.feature_evaluator = feature_evaluator
        self.dask_client = dask_client
        
    def evaluate_features(self, current_features, feature_stack, group_key=None):
        
        feature_score_dict = dict()
        
        feature_score_futures_dict = self._feature_evaluation_score_futures(
            current_features, feature_stack, group_key=group_key
        )
        
        for k, v in feature_score_futures_dict.items():
            
            score = np.mean([future.result() for future in v])
            feature_score_dict[k] = score
        
        return feature_score_dict
     
        
    def _feature_evaluation_score_futures(self, current_features, feature_stack, group_key=None):
        
        feature_score_futures_dict = defaultdict(list)
        
        for new_feature in feature_stack:
            
            for i in range(0, 5):
                
                feature_score_futures_dict[new_feature].append(self.dask_client.submit(
                    self.feature_evaluator.evaluate_feature, 
                                                                            current_features, 
                                                                            new_feature,
                                                                            i,
                                                                            group_key=group_key))
                
        return feature_score_futures_dict



