import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.base import BaseEstimator, TransformerMixin

#class OwnTransformer(BaseEstimator,TransformerMixin):
#    def __init__()
#    def fit():
#        pass
#    def transform():
#       pass

data = load_iris(as_frame = True)
features = data.get('data')
target = data.get('target')


#help(StandardScaler)

class ExperimentalTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        print("fit complete")
        return self
    
    def transform(self, X, y = None):
        X_copy = X.copy() # make sure original data doesn't get changed
        X_copy = np.sqrt(X_copy)
        return X_copy

exp_transformer = ExperimentalTransformer()
features_sqrt = exp_transformer.fit_transform(features)
display(features.head())
display(features_sqrt.head())


class IQROutlierRemover(BaseEstimator,TransformerMixin):
    
    def __init__(self, factor=1.5, quantile_bounds = (0.25, 0.75)):
        assert isinstance(factor, (float, int)), 'factor must be of type float or int'
        assert isinstance(quantile_bounds, tuple), 'quantile_bounds must be of type tuple'
        assert len(quantile_bounds) == 2, 'quantile_bounds must be of length 2'
        self.factor = factor
        self.quantile_bounds = quantile_bounds
        
    def _outlier_detector(self, X_col):
        """
        Take a feature column, create a Series and copy of it. 
        Determine quantiles and lower bound and upper bound as (first quantile - (factor * iqr)) 
        and (third quantile + (factor * iqr)) respectively, 
        where iqr = third - first quantile. 
        Append bounds to self.lower_bound_ and self.upper_bound_.

        Args:
            X_col: Column from features.

        """

        X_col = pd.Series(X_col).copy()
        q1 = X_col.quantile(self.quantile_bounds[0])
        q3 = X_col.quantile(self.quantile_bounds[1])
        iqr = q3 - q1
        self.lower_bound_.append(q1 - (self.factor * iqr))
        self.upper_bound_.append(q3 + (self.factor * iqr))

    def fit(self, X, y=None):
        """
        Instantiate self.lower_bound and self.upper_bound as empty lists.
        Apply _outlier_detector to X.
        
        Args:
            X (array-like): array-like containing features.
            y (array-like): array-like containing target value. Defaults to None.
        
        Returns:
            self

        """

        if isinstance(X, pd.DataFrame):
            X_copy = X.values.copy()
        else:
            X_copy = X.copy()
        self.lower_bound_ = []
        self.upper_bound_ = []
        np.apply_along_axis(self._outlier_detector, 0, X_copy)
        return self
    
    def transform(self, X, y=None):
        """
        Create a copy of X. Loops over columns in the copy.
        Create mask for each column marking data points outside of lower_bound_ 
        and upper_bound_ for that column as np.nan.
        Replace column in copy of X with column with mask applied.
        If y is not None. Remove rows where X_copy has np.nan.
        Remove np.nan in X_copy.
        
        Args:
            X (array-like): array-like containing features.
            y (array-like): array-like containing target value. Defaults to None.
            
        Returns:
            X_copy (np.array): Array containing features with outliers removed.
            y (np.array): Array containing target value with outliers removed.

        """

        if isinstance(X, pd.DataFrame):
            X_copy = X.values.copy()
        else:
            X_copy = X.copy()
        for i in range(X_copy.shape[1]):
            x = X_copy[:, i].copy()
            x[(x < self.lower_bound_[i]) | (x > self.upper_bound_[i])] = np.nan
            X_copy[:, i] = x
        if y is not None:
            y = y[~np.isnan(X_copy).any(axis=1)]
            X_copy = X_copy[~np.isnan(X_copy).any(axis=1)]#X_copy.dropna()
            return X_copy, y
        else:
            X_copy = X_copy[~np.isnan(X_copy).any(axis=1)]
            return X_copy


outlier_remover = IQROutlierRemover()

outlier_remover.fit(features,target)
features_trimmed, target_trimmed = outlier_remover.transform(features,target)

features.plot(kind = 'box', figsize = (10,8), title = 'Features');

features_trimmed = pd.DataFrame(features_trimmed, columns = features.columns)
features_trimmed.plot(kind = 'box', figsize = (10,8), title = 'Features Transformed');

print(features.shape, target.shape)
print(features_trimmed.shape, target_trimmed.shape)

features_trimmed_2 = outlier_remover.fit_transform(features)
features_trimmed_2.shape

# Error comming from fit_transform that has been inherited from TransformerMixin
features_trimmed, target_trimmed = outlier_remover.fit_transform(features,target)

#class ExperimentalTransformer(BaseEstimator, TransformerMixin):
#    def fit(self, X, y = None):
#        print("fit complete")
#        return self
#    
#    def transform(self, X, y = None):
#        X_copy = X.copy() # make sure original data doesn't get changed
#        X_copy = np.sqrt(X_copy)
#        return X_copy

#Another error 
pipe_outlier_scaler_logreg = Pipeline([('outlier_remover', IQROutlierRemover()),
                                ('scaler', StandardScaler()),
                               ('model', LogisticRegression(max_iter = 1e4))])

pipe_outlier_scaler_logreg.fit(features, target)



class OutlierRemoverClassifier(BaseEstimator):
    def __init__(self, outlier_remover, classifier):
        # test if sklearn?
        self.outlier_remover = outlier_remover
        self.classifier = classifier
        
    def fit(self, X, y):
        """ 
        Fit outlier remover and transform the data given by X and y.
        Fit classifier on data. Print number of removed outliers.
        
        Args:
            X (array-like): array-like containing features.
            y (array-like): array-like containing target value. Defaults to None.
        
        Returns:
            self

        """

        self.outlier_remover.fit(X, y)
        X_ , y_ = self.outlier_remover.transform(X, y)
        self.classifier_ = self.classifier.fit(X_, y_)
        print(f'{X.shape[0] - X_.shape[0]} outlier removed')
        return self
    
    def predict(self, X):
        """
        Use fitted classifier to predict based on X.
        
        Args:
            X (array-like): array-like containing features.
        
        Returns:
            self.classifier_.predict(X)
            
        """

        return self.classifier_.predict(X)


features.shape, target.shape

outlier_remover = IQROutlierRemover()
logreg = LogisticRegression(max_iter = 1e4)
out_logreg = OutlierRemoverClassifier(outlier_remover, logreg)
out_logreg.fit(features,target)
predictions = out_logreg.predict(features)
print(f'Number of predicted values: {len(predictions)}')
print(predictions)

outlier_remover = IQROutlierRemover()
logreg = LogisticRegression(max_iter = 1e4)
out_logreg = OutlierRemoverClassifier(outlier_remover, logreg)

pipe_scaler_outlierlogreg = Pipeline([('scaler', StandardScaler()),
                               ('model', out_logreg)])

pipe_scaler_outlierlogreg.fit(features, target)

preds_pipe = pipe_scaler_outlierlogreg.predict(features)
print(f'Number of predicted values: {len(preds_pipe)}')
print(preds_pipe)