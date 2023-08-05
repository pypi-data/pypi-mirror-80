import numpy as np

from ..utils.data_structure_utils import merge_dicts


class FeatureEngineer():
    
    def __init__(self, data, features, target):
        
        self.data = data
        self.features = features
        self.target = target
        
    def create_new_features(self):
        
        neg_corr_features, neg_corr_values, pos_corr_features, pos_corr_values = self._get_basic_features()
        
        neg_corr_prod_features, neg_corr_prod_values = self._get_prod_features(
            neg_corr_features, neg_corr_values, neg_corr_features, neg_corr_values)
        
        pos_corr_prod_features, pos_corr_prod_values = self._get_prod_features(
            pos_corr_features, pos_corr_values, pos_corr_features, pos_corr_values)
        
        all_pos_corr_features = pos_corr_features + pos_corr_prod_features
        all_pos_corr_values = merge_dicts([pos_corr_values, pos_corr_prod_values])

        all_neg_corr_features = neg_corr_features + neg_corr_prod_features
        all_neg_corr_values = merge_dicts([neg_corr_values, neg_corr_prod_values])
        
        quot_corr_features, quot_corr_values = self._get_quot_features(
            all_pos_corr_features, all_pos_corr_values, all_neg_corr_features, all_neg_corr_values)
        
        all_corr_features = neg_corr_features + pos_corr_features + \
                            neg_corr_prod_features + pos_corr_prod_features + \
                            quot_corr_features

        all_corr_values = merge_dicts([neg_corr_values, pos_corr_values,
                                       neg_corr_prod_values, pos_corr_prod_values,
                                       quot_corr_values])
        
        return self.data, all_corr_features, all_corr_values
        
    def _get_basic_features(self):
        
        neg_corr_features = []
        neg_corr_values = {}

        pos_corr_features = []
        pos_corr_values = {}

        for feature in self.features:

            corr = np.corrcoef(self.data[self.target], self.data[feature])[1, 0]

            if corr > 0:
                pos_corr_features.append(feature)
                pos_corr_values[feature] = corr
            else:
                neg_corr_features.append(feature)
                neg_corr_values[feature] = corr
                
        return neg_corr_features, neg_corr_values, pos_corr_features, pos_corr_values
                
    def _get_prod_features(self, features1, feature_values1, features2, feature_values2):
        
        prod_features = []
        prod_values = {}
        
        for feature1 in features1:
            
            for feature2 in features2:
                
                prod_corr = np.abs(
                    np.corrcoef(self.data[feature1] * self.data[feature2], 
                                self.data[self.target])[1, 0]
                )
                
                feat_corr = max(
                    np.abs(feature_values1[feature1]),
                    np.abs(feature_values2[feature2])
                )

                if prod_corr > feat_corr:
                    
                    prod_feature = "_PROD_".join([feature1, feature2])
                    
                    self.data[prod_feature] = self.data[feature1] * self.data[feature2]
                    
                    prod_features.append(prod_feature)
                    prod_values[prod_feature] = prod_corr
                    
        return prod_features, prod_values
                
    def _get_quot_features(self, pos_corr_features, pos_corr_values, neg_corr_features, neg_corr_values):
        
        quot_features = []
        quot_values = {}
        
        for pos_corr_feature in pos_corr_features:
            
            for neg_corr_feature in neg_corr_features:
                
                quot_corr = np.abs(
                    np.corrcoef(self.data[pos_corr_feature] / self.data[neg_corr_feature],
                                self.data[self.target])[1, 0]
                )
                
                feat_corr = max(
                    pos_corr_values[pos_corr_feature],
                    np.abs(neg_corr_values[neg_corr_feature])
                )
                
                if quot_corr > feat_corr:
                    
                    quot_feature = '_OVER_'.join((pos_corr_feature, neg_corr_feature))
                    
                    self.data[pos_corr_feature]
                    self.data[neg_corr_feature]
            
                    self.data[quot_feature] = self.data[pos_corr_feature] * self.data[neg_corr_feature]

                    quot_features.append(quot_feature)
                    quot_values[quot_feature] = quot_corr
    
        return quot_features, quot_values



