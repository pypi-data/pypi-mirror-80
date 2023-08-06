import numpy as np
import pandas as pd
from collections import Counter
from sklearn.utils import resample
from tqdm.notebook import tqdm_notebook
import copy
from sklearn.base import is_classifier

class DSClassifier:
    
    """This classifier is designed to handle unbalanced data. 
       The classification is based on an ensemble of sub-sets.

        Input:

            base_estimator     A base model that the classifier will use to make a prediction on each subset.

            ratio              The ratio of the minority group to the rest of the data. 
                               The default is 1.
                               The ratio describes a ratio of 1: ratio.
                               For example:
                               Ratio = 1 Creates a 1: 1 ratio (50% / 50%) between the minority group and the rest of the data.
                               Ratio = 2 Creates a 2: 1 ratio (33% / 66%) between the minority group and the rest of the data.

            ensemble           The method by which the models of each subset will be combined together. 
                               The default is mean.
                               For numeric labels you can select max or min to tilt the classifier to a certain side. 

            random_state       Seed for the distribution of the majority population in each subset.
                                The default is 42.

        Attributes:
        
            fit(X_train, y_train)
            
            predict(X)
            
            predict_proba(X)
            
            list_of_df         List of all created sub-sets.
            
            list_models        List of all the models that make up the final model.
        
    """
    def __init__(self, base_estimator, ratio = 1, ensemble = 'mean', random_state = 42):
        
        def get_ensemble(ensemble):
            if ensemble == 'mean':
                return np.mean
            if ensemble == 'max':
                return np.max
            if ensemble == 'min':
                return np.min
            else:
                raise ValueError("ensemble must be one of these options: 'mean', 'max', 'min' not " + ensemble)
                
        if is_classifier(base_estimator):
              self.base_estimator = base_estimator
        else:
            raise ValueError("base_estimator must be a classifier not " + base_estimator)
        self._estimator_type =  'classifier'
        self._ratio = ratio
        self.ensemble = get_ensemble(ensemble)
        self._random_state = random_state
        self.classes_ = None
        self._target = None
        self.list_of_df = None
        self.list_models = None
    
    def __repr__(self):
        return self._estimator_type
    
    def fit(self, X_train, y_train):
        
        def balance(X_train, y_train, ratio, random_state):
            model_input_data = pd.concat([X_train, y_train],  axis=1)
            counter = Counter(y_train).most_common()
            minority = counter[-1][0]
            majority = counter[0][0]
            
            row_by_class = {majority: model_input_data[model_input_data[self.target] != minority], \
                           minority: model_input_data[model_input_data[self.target] == minority],}
    
            num_of_samples_minority = int(row_by_class[minority].shape[0])
            num_of_samples_majority = int(num_of_samples_minority)*ratio

            list_of_df = []
            while len(row_by_class[majority])>num_of_samples_majority:
                    majority_sample = resample(row_by_class[majority], 
                                        replace = True,
                                        n_samples = num_of_samples_majority, random_state=random_state)
                    row_by_class[majority] = row_by_class[majority].drop(majority_sample.index.values.tolist())
                    subsets = pd.concat([row_by_class[minority], majority_sample])
                    list_of_df.append(subsets)
            old_minority_percent = format(counter[-1][1] / (counter[0][1] + counter[-1][1]) *100, '.2f')
            new_minority_percent = format(num_of_samples_minority / (num_of_samples_majority + num_of_samples_minority) *100, '.2f')
            return list_of_df

        def modeling(list_of_df, base_estimator):
            list_models = []
            for i in tqdm_notebook(range((len(list_of_df)))):
                x_train = list_of_df[i].drop(self.target, axis=1)
                y_train = list_of_df[i][self.target]
                model = copy.deepcopy(base_estimator)
                model.fit(x_train, y_train)
                list_models.append(model)
            return list_models
    
        self.target = y_train.name
        self.classes_ = np.unique(y_train)
        self.list_of_df = balance(X_train, y_train, self._ratio, self._random_state)
        self.list_models = modeling(self.list_of_df, self.base_estimator)
    
    def predict(self, X):
        list_of_predict = []
        for i in tqdm_notebook(range(len(self.list_models))):
            list_of_predict.append(self.list_models[i].predict(X))
        return self.ensemble(list_of_predict, axis=0).round()
    
    def predict_proba(self, X):
        list_of_predict_proba = []
        for i in tqdm_notebook(range(len(self.list_models))):
            list_of_predict_proba.append(self.list_models[i].predict_proba(X))
        return self.ensemble(list_of_predict_proba, axis=0)