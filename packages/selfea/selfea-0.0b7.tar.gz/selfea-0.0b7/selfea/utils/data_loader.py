from ..utils.data_structure_utils import return_indices

import HMF
import numpy as np
import pandas as pd

class DataLoader():
	
	def init(self, dirpath):
		
		self.f = HMF.open_file(dirpath, mode='r+')
		self.dirpath = dirpath

	
	@staticmethod
	def save_data(dirpath, data, orderby=None, groupby=None):
		"""Later, add support for groupby
		
		"""
		
		f = HMF.open_file(dirpath, mode='w+')
		numeric_data = data.select_dtypes(include=[np.number])
		
		f.from_pandas(numeric_data, orderby=orderby, groupby=groupby)

		f.register_array('data_array', numeric_data.columns)
		f.set_node_attr('/column_names', key='column_names', value=numeric_data.columns)

		f.close()
		

	def load_data(self, features, target=None, group_key=None):

		
		if not group_key:
			
			data_array = self.f.get_array('/data_array')
			column_names = list(self.f.get_node_attr('/column_names', key='column_names'))
		
		else:

			data_array = self.f.get_array('/{}/data_array'.format(group_key))
			column_names = self.f.get_node_attr('/{}/column_names'.format(group_key), key='column_names')

		
		feature_column_indices = return_indices(column_names, features)
		X = data_array[:, feature_column_indices]

		if target:

			target_column_index = return_indices(column_names, [target])
			y = data_array[:, target_column_index]

			return X, y

		else:

			return X


	def load_dataframe(self, features, group_key=None):

		
		if not group_key:
			data_array = self.f.get_array('/data_array')
			column_names = list(self.f.get_node_attr('/column_names', key='column_names'))

		else:

			data_array = self.f.get_array('/{}/data_array'.format(group_key))
			column_names = self.f.get_node_attr('/{}/column_names'.format(group_key), key='column_names')


		return pd.DataFrame(data_array, columns=column_names)

	def load_feature_stack(self, group_key=None):

		return self.f.get_node_attr('/{}/all_corr_features'.format(group_key), key='all_corr_features')





