import numpy as np

from ..utils.data_structure_utils import merge_dicts


class FeatureEngineer():
    
    def __init__(self, data, features, target, na_thresh=0.2, include_all=False):
        
        self.data = data
        self.features = features
        self.target = target
        self.include_all = include_all
        self.na_thresh = na_thresh
        
    def create_new_features(self):

        # 1. if the basic feature has na values greater than thresh, remove it from considerations
        self._remove_basic_features(self.na_thresh)
        
        # 2. get neg corr features and pos corr features
        neg_corr_features, neg_corr_values, pos_corr_features, pos_corr_values = self._get_basic_features()

        # 3. cap the feature values at maximum if inf for both neg corr and pos corr features
        pos_corr_features = self._get_max_values_of_pos_corrs(pos_corr_features)
        neg_corr_features = self._get_max_values_of_pos_corrs(neg_corr_features)
        
        # 4. get prod features for neg corr features
        neg_corr_prod_features, neg_corr_prod_values = self._get_prod_features(
            neg_corr_features, neg_corr_values, neg_corr_features, neg_corr_values)

        all_neg_corr_features = neg_corr_features + neg_corr_prod_features
        all_neg_corr_values = merge_dicts([neg_corr_values, neg_corr_prod_values])
        
        # 5. get prod features for pos corr features
        pos_corr_prod_features, pos_corr_prod_values = self._get_prod_features(
            pos_corr_features, pos_corr_values, pos_corr_features, pos_corr_values)

        all_pos_corr_features = pos_corr_features + pos_corr_prod_features
        all_pos_corr_values = merge_dicts([pos_corr_values, pos_corr_prod_values])

        # 6. since neg corr features become denom, if there are 0, lower bound it by minimum value 
        all_neg_corr_features = self._get_min_values_of_neg_corrs(all_neg_corr_features)
        
        # 7. get quot features
        quot_corr_features, quot_corr_values = self._get_quot_features(
            all_pos_corr_features, all_pos_corr_values, all_neg_corr_features, all_neg_corr_values)
        
        all_corr_features = neg_corr_features + pos_corr_features + \
                            neg_corr_prod_features + pos_corr_prod_features + \
                            quot_corr_features
        all_corr_values = merge_dicts([neg_corr_values, pos_corr_values,
                                       neg_corr_prod_values, pos_corr_prod_values,
                                       quot_corr_values])
        
        return self.data, all_corr_features, all_corr_values

    def _remove_basic_features(self, na_thresh):

        self.rm_features = []

        for feat in self.features:
            if self.data[feat].isna().sum()/len(self.data) > na_thresh:
                
                self.rm_features.append(feat)

        self.features = [elem for elem in self.features if elem not in self.rm_features]
        
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

                min_feat_corr = min(
                    np.abs(feature_values1[feature1]),
                    np.abs(feature_values2[feature2])
                )

                if not self.include_all and prod_corr > feat_corr:
                    
                    prod_feature = "_PROD_".join([feature1, feature2])
                    
                    self.data[prod_feature] = self.data[feature1] * self.data[feature2]
                    
                    prod_features.append(prod_feature)
                    prod_values[prod_feature] = prod_corr

                elif self.include_all and prod_corr > min_feat_corr:

                    prod_feature = "_PROD_".join([feature1, feature2])
                    
                    self.data[prod_feature] = self.data[feature1] * self.data[feature2]
                    
                    prod_features.append(prod_feature)
                    prod_values[prod_feature] = prod_corr

                    
        return prod_features, prod_values
    
    def _get_max_values_of_pos_corrs(self, pos_corr_features):
        
        skip_cols = []
        
        for pos_corr_feature in pos_corr_features:
            
            if len(self.data[self.data[pos_corr_feature]==np.inf])/len(self.data) > 0.15:
                skip_cols.append(pos_corr_feature)
                
        pos_corr_features = [elem for elem in pos_corr_features if elem not in skip_cols]
        
        self.max_val_dict = {}
                
        for pos_corr_feature in pos_corr_features:
            
            max_val = self.data[self.data[pos_corr_feature]!=np.inf][pos_corr_feature].max()
            
            self.data.loc[self.data[pos_corr_feature]==np.inf, pos_corr_feature] = max_val
            
            self.max_val_dict[pos_corr_feature] = max_val
        
        return pos_corr_features
        
    
    def _get_min_values_of_neg_corrs(self, neg_corr_features):
        
        skip_cols = []
        
        for neg_corr_feature in neg_corr_features:
            
            if len(self.data[self.data[neg_corr_feature]==0])/len(self.data) > 0.15:
                skip_cols.append(neg_corr_feature)
                
        neg_corr_features = [elem for elem in neg_corr_features if elem not in skip_cols]
        
        self.min_val_dict = {}
                
        for neg_corr_feature in neg_corr_features:
            
            min_val = self.data[self.data[neg_corr_feature]!=0][neg_corr_feature].min()
            
            self.data.loc[self.data[neg_corr_feature]==0, neg_corr_feature] = min_val
            
            self.min_val_dict[neg_corr_feature] = min_val
            
        return neg_corr_features
        
                
    def _get_quot_features(self, pos_corr_features, pos_corr_values, neg_corr_features, neg_corr_values):
        
        quot_features = []
        quot_values = {}
        
        for pos_corr_feature in pos_corr_features:
            
            for neg_corr_feature in neg_corr_features:
                
                quot_corr = np.abs(
                    np.corrcoef(self.data[pos_corr_feature] / self.data[neg_corr_feature],
                                self.data[self.target])[1, 0]
                )
                
                

                if not self.include_all: 
                    
                    feat_corr = max(
                        pos_corr_values[pos_corr_feature],
                        np.abs(neg_corr_values[neg_corr_feature])
                    )
                
                    if quot_corr > feat_corr:
                    
                        quot_feature = '_OVER_'.join((pos_corr_feature, neg_corr_feature))

                        self.data[pos_corr_feature]
                        self.data[neg_corr_feature]

                        self.data[quot_feature] = self.data[pos_corr_feature] / self.data[neg_corr_feature]

                        quot_features.append(quot_feature)
                        quot_values[quot_feature] = quot_corr

                elif self.include_all:# and quot_corr > min_feat_corr:
                    
                    quot_feature = '_OVER_'.join((pos_corr_feature, neg_corr_feature))
                    
                    self.data[pos_corr_feature]
                    self.data[neg_corr_feature]
            
                    self.data[quot_feature] = self.data[pos_corr_feature] / self.data[neg_corr_feature]

                    quot_features.append(quot_feature)
                    quot_values[quot_feature] = quot_corr
    
        return quot_features, quot_values

