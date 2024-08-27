"""
===============================================================================
 Author: Dr. Francisco J. Arriaza G.
 Date: 2024.06.18
 Description: Creates custom outlier removal based on median and custom IQR.
 This was done as assignment for an Advanced OOP python course.
===============================================================================
"""

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.base import is_classifier
import pandas as pd
import numpy as np


class IQROutlierRemover(BaseEstimator, TransformerMixin):
    """Custom outlier removal transformer for the sklearn module based on median and custom
    Inter Quantile Range (IQR)

    Args:
        factor (int or float): limit from IQR that delimits outliers. Defaults to 1.5
        quantile_bounds (tuple): tupe of len 2 that creates the IQR. Defaults to (0.25, 0.75)
    """
    def __init__(self, factor: int = 1.5, quantile_bounds: tuple = (0.25, 0.75)):
        
        if not (isinstance(factor, int) or isinstance(factor, float)):
            raise ValueError("factor must be int or float")
        
        if not isinstance(quantile_bounds, tuple) or len(quantile_bounds) != 2:
            raise ValueError("quantile_bounds must be a tuple of length 2")

        self.factor = factor
        self.quantile_bounds = quantile_bounds
    
    def _outlier_detector(self, X_col: pd.Series | np.ndarray):
        """
        Take a feature column, create a Series and copy of it. 
        Determine quantiles and lower bound and upper bound as (first quantile - (factor * iqr)) 
        and (third quantile + (factor * iqr)) respectively, 
        where iqr = third - first quantile. 
        Append bounds to self.lower_bound_ and self.upper_bound_.

        Args:
            X_col: Column from features.
        """
        #Check if X_col is array or Series and makes a copy if Series or transforms into Series and copy if ndarray
        if isinstance(X_col, pd.Series):
            X_series_copy = X_col.copy()
        if isinstance(X_col, np.ndarray):
            X_series_copy = pd.Series(X_col)
        
        #Calculate quantiles using self.quantile_bounds
        first_quantile = X_series_copy.quantile(self.quantile_bounds[0])
        third_quantile = X_series_copy.quantile(self.quantile_bounds[1])
        
        #Calculate IQR
        iqr = third_quantile - first_quantile

        #Append lower and upper bounds
        self.lower_bound_.append(first_quantile - (self.factor * iqr))
        self.upper_bound_.append(third_quantile + (self.factor * iqr))

    def fit(self, X: pd.DataFrame | np.ndarray, y: np.ndarray | pd.Series = None):
        """
        Instantiate self.lower_bound_ and self.upper_bound_ as empty lists.
        Apply _outlier_detector to X.
        
        Args:
            X (array-like): array-like containing features.
            y (array-like): array-like containing target value. Defaults to None.
        
        Returns:
            self

        """
        #Initiate lower and upper bounds as empty lists
        self.lower_bound_ = []
        self.upper_bound_ = []

        #Apply _otlier_detector to X column-wise.
        if isinstance(X, pd.DataFrame):
            for i in range(X.shape[1]):
                self._outlier_detector(X.iloc[:,i])
        if isinstance(X, np.ndarray):
            for i in range(X.shape[1]):
                self._outlier_detector(X[:,i])

        #Return self for method chaining
        return self
        
    def transform(self, X: pd.DataFrame | np.ndarray, y: np.ndarray | pd.Series = None):
        """
        Create a copy of X. Loop over columns in the copy.
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
        if not isinstance(X, (pd.DataFrame | np.ndarray)):
            raise ValueError('X must be pandas DataFrame or Numpy ndarray')

        if isinstance(X, pd.DataFrame):
            X_copy = X.copy()
        if isinstance(X, np.ndarray):
            X_copy = pd.DataFrame(X)
        
        #Iterate through all columns in DataFrame using numerical index instead of column names.
        for i in range(len(X_copy.columns)):
            #Set masks for both limits individualy
            X_copy_lower_mask = X_copy.iloc[:,i] < self.lower_bound_[i]
            X_copy_upper_mask = X_copy.iloc[:,i] > self.upper_bound_[i]
            
            #Use bitwise OR to combine them into a single mask
            X_copy_mask = X_copy_lower_mask | X_copy_upper_mask

            #Use mask to replace values with numpy NaN
            X_copy[X_copy_mask] = np.nan

            #Drop NaN by inplace pandas.DataFrame.dropna()
            X_copy.dropna(axis = 0, inplace = True)
        
        if type(y) != type(None):
            y = y.reindex(X_copy.index)
            y.dropna(inplace=True)

        #Return self for method chaining
        return X_copy, y
    
class OutlierRemoverClassifier(BaseEstimator):
    """
    MetaClassifier that adds Pipeline compatibility to IQROutlierRemover

    Args:
        outlier_remover (IQROutlierRemover): instance of IQROutlierRemover
        classifier: instance of sklearn classifier
        force_classifier: skips the classifier check, this is because is_classifier doesn't always work. Defaults to False
    """

    def __init__(self, outlier_remover : IQROutlierRemover, classifier, force_classifier : bool = False):
        
        self.force_classifier = force_classifier #Removes a bug with BaseEstimator when printing model (i.e End of Cell)

        #Check if classifier is of sklearn classifier. Can be overriden by force_classifier = True
        if not is_classifier(classifier):
            if not force_classifier:
                raise TypeError("classifier is not a sklearn Classifier \n Note: Use force_classifier = True to override. NOT RECOMMENDED")
        
        #Store instantiated outlier_remover and classifier
        self.outlier_remover = outlier_remover
        self.classifier = classifier
    
    def fit(self, X : pd.DataFrame | np.ndarray , y : pd.Series | np.ndarray = None):
        
        #Remove outliers with outlier_remover
        self.outlier_remover.fit(X)
        features_trimmed, target_trimmed = self.outlier_remover.transform(X, y)

        #Train classifier with trimmed features and target
        self.classifier.fit(features_trimmed, target_trimmed)

        print(F"{len(X) - len(features_trimmed)} features removed.")

        return self
    
    def predict(self, X : pd.DataFrame | np.ndarray):
        target_predicted = self.classifier.predict(X)
        return target_predicted
        


