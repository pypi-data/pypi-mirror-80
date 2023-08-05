

from ..utils.data_structure_utils import return_indices

import HMF
import numpy as np
import pandas as pd

class DataLoader():
	
	def __init__(self):
		
		pass
	
	@staticmethod
	def save_data(dirpath, data, orderby=None, groupby=None):
		"""Later, add support for groupby
		
		"""
		
		f = HMF.open_file(dirpath, mode='w+')
		numeric_data = data.select_dtypes(include=[np.number])
		
		f.from_pandas(numeric_data, orderby=orderby)

		f.register_array('data_array', numeric_data.columns)
		f.set_node_attr('/column_names', key='column_names', value=numeric_data.columns)

		f.close()
		

	@staticmethod
	def load_data(dirpath, features, target=None):

		f = HMF.open_file(dirpath, mode='r+')
		
		data_array = f.get_array('/data_array')
		column_names = list(f.get_node_attr('/column_names', key='column_names'))
		
		feature_column_indices = return_indices(column_names, features)
		X = data_array[:, feature_column_indices]

		if target:

			target_column_index = return_indices(column_names, [target])
			y = data_array[:, target_column_index]

			return X, y

		else:

			return X

	@staticmethod
	def load_dataframe(dirpath, features):

		f = HMF.open_file(dirpath, mode='r+')
		
		data_array = f.get_array('/data_array')
		column_names = list(f.get_node_attr('/column_names', key='column_names'))

		return pd.DataFrame(data_array, columns=column_names)

