import math
import warnings

import lightgbm

from . import auto_split_logic


class LGBMClassifier(lightgbm.LGBMClassifier):
    """
    Estimator which learns n_estimator by using only training data set
    """
    def __init__(self, max_n_estimators=5000, ratio_training=0.8, metric="auc", ratio_min_data_in_leaf=None,
                 early_stopping_rounds=100, num_leaves=None, max_depth=None, learning_rate=None, class_weight=None,
                 feature_fraction=None, boosting_type=None, random_state=None, n_jobs=1, importance_type="gain"):
        # kwargs cannot be used for sklearn compatibility
        super(LGBMClassifier, self).__init__(
            boosting_type=boosting_type, n_estimators=max_n_estimators, early_stopping_rounds=early_stopping_rounds,
            num_leaves=num_leaves, max_depth=max_depth, learning_rate=learning_rate, class_weight=class_weight,
            feature_fraction=feature_fraction, random_state=random_state, n_jobs=n_jobs, importance_type=importance_type
        )
        self.max_n_estimators = max_n_estimators
        self.ratio_training = ratio_training
        self.ratio_min_data_in_leaf = ratio_min_data_in_leaf
        self.metric = metric

    def call_parent_fit(self, x, y, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", message="Found `early_stopping_rounds` in params. Will use it instead of argument")
            return super(LGBMClassifier, self).fit(x, y, **kwargs)

    def fit(self, x, y, **kwargs):
        if self.early_stopping_rounds > 0:
            self._set_min_data_in_leaf(self.ratio_training * x.shape[0])
            auto_split_logic.auto_split_fit(self, x, y, **kwargs)
        self._set_min_data_in_leaf(x.shape[0])
        self.call_parent_fit(x, y, verbose=False, early_stopping_rounds=-1)

    def _set_min_data_in_leaf(self, sample_size):
        if self.ratio_min_data_in_leaf is not None:
            self.set_params(min_data_in_leaf=int(math.ceil(sample_size*self.ratio_min_data_in_leaf)))


class LGBMRegressor(lightgbm.LGBMRegressor):
    def __init__(self, max_n_estimators=5000, ratio_training=0.8, metric="rmse", ratio_min_data_in_leaf=None,
                 early_stopping_rounds=100, num_leaves=None, max_depth=None, learning_rate=None, class_weight=None,
                 feature_fraction=None, boosting_type=None, random_state=None, n_jobs=1, importance_type="gain"):
        self.max_n_estimators = max_n_estimators
        self.ratio_training = ratio_training
        self.ratio_min_data_in_leaf = ratio_min_data_in_leaf
        self.metric = metric
        super(LGBMRegressor, self).__init__(
            boosting_type=boosting_type, n_estimators=max_n_estimators, early_stopping_rounds=early_stopping_rounds,
            num_leaves=num_leaves, max_depth=max_depth, learning_rate=learning_rate, class_weight=class_weight,
            feature_fraction=feature_fraction, random_state=random_state, n_jobs=n_jobs, importance_type=importance_type
        )

    def call_parent_fit(self, x, y, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", message="Found `early_stopping_rounds` in params. Will use it instead of argument")
            return super(LGBMRegressor, self).fit(x, y, **kwargs)

    def fit(self, x, y, **kwargs):
        if self.early_stopping_rounds > 0:
            self._set_min_data_in_leaf(self.ratio_training * x.shape[0])
            auto_split_logic.auto_split_fit(self, x, y, **kwargs)
        self._set_min_data_in_leaf(x.shape[0])
        self.call_parent_fit(x, y, verbose=False, early_stopping_rounds=-1)

    def _set_min_data_in_leaf(self, sample_size):
        if self.ratio_min_data_in_leaf is not None:
            self.set_params(min_data_in_leaf=int(math.ceil(sample_size*self.ratio_min_data_in_leaf)))
