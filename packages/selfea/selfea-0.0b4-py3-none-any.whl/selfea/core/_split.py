from abc import ABCMeta, abstractmethod
import numpy as np

from sklearn.model_selection._split import *
from sklearn.utils import indexable
from sklearn.utils.validation import _num_samples

__all__ = ['BaseCrossValidator',
           'KFold',
           'GroupKFold',
           'LeaveOneGroupOut',
           'LeaveOneOut',
           'LeavePGroupsOut',
           'LeavePOut',
           'RepeatedStratifiedKFold',
           'RepeatedKFold',
           'ShuffleSplit',
           'GroupShuffleSplit',
           'StratifiedKFold',
           'StratifiedShuffleSplit',
           'PredefinedSplit',
           'train_test_split',
           'check_cv',
           'BaseRollingWindowSplit',
           'DateRollingWindowSplit']


def get_cv_splitter(cross_validation_scheme, *args, **kwargs):

    if cross_validation_scheme=='date_rolling_window':
        return DateRollingWindowSplit(*args, **kwargs)
    elif cross_validation_scheme=='k_fold':
        return KFold(*args, **kwargs)

