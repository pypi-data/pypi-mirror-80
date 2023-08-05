
from ..utils.data_loader import DataLoader

from ..utils.data_structure_utils import remove_elems
from ..utils.data_structure_utils import get_min_value_key

import copy
import numpy as np

class FeatureSelector():
	
	def __init__(self, max_num_features, parallel_feature_evaluator, data_loader,
				 corr_thres=0.85, verbose=False):
		
		self.current_features = []
		# self.feature_stack = copy.copy(feature_stack)
		self.max_num_features = max_num_features
		self.score_tracking_dict = dict()
		
		self.parallel_feature_evaluator = parallel_feature_evaluator
		
		self.data_loader = data_loader
		self.corr_thres = corr_thres

		self.verbose = verbose
	
	def select_features(self, group_key=None):

		self.feature_stack = self.data_loader.load_feature_stack(group_key=group_key)
		self.data = self.data_loader.load_dataframe(self.feature_stack, group_key=group_key)
		
		
		counter = 0
		best_score = np.inf
		
		while(len(self.feature_stack)>0 and self.max_num_features>len(self.current_features)):
			
			feature_score_dict = self.parallel_feature_evaluator.evaluate_features(
				self.current_features, 
				self.feature_stack,
				group_key=group_key
			)
			
			best_feature = get_min_value_key(feature_score_dict)
			new_score = feature_score_dict[best_feature]
			
			if best_score > new_score:
				best_score = new_score
			else:
				print('stopping criterion met!')
				break
				
			# if the new error is lower than the old best error:
			self.feature_stack.remove(best_feature)
			self.current_features.append(best_feature)
			self.score_tracking_dict[counter] = feature_score_dict
			counter += 1

			print("new score : " , new_score)

			# print(feature_score_dict)
			# print(self.current_features)

			# eliminate correlated features
			corred_features, corred_values = self._drop_correlated_features(best_feature)
			self.feature_stack = remove_elems(self.feature_stack, corred_features)

		return self.score_tracking_dict, self.current_features
			
	def _drop_correlated_features(self, new_feature):
		
		corred_features = []
		corred_values = dict()
		
		for feature in self.feature_stack:
			
			corr = np.abs(np.corrcoef(self.data[feature],
									  self.data[new_feature])[1, 0])
			
			corred_values[feature] = corr
		
			if corr > self.corr_thres:
				
				corred_features.append(feature)

		if self.verbose:

			print('there were {} correlated features with {}'.format(len(corred_features), new_feature))
				
		return corred_features, corred_values
			
		
		
		
	