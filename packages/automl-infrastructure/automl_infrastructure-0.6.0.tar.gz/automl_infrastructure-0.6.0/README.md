# AutoML Infrastructure
## Library Goal
The automl_infrastructure library's main goal is supplying
wide and easy-to-use infrastructure for classifiers modeling
 and evaluation, including inner cross-validated hyper-param 
 optimization.
 
 ## Main Features
 * Inner cross-validation process using repeated k-fold.
 * Optional hyper-params optimization process.
 * Complex modeling creation (e.g. blending several weak classifiers).
 * Experiment definition with final report that contains:
    * Experiment's information (start time, end time and ect')
    * For each model:
        * Observations (metrics) summary for every class.
        * Visualizations (e.g ConfusionMatrix).
 
 Note that every Visualization/Observation/Metric may be implemented by the user. 

## Simple Example
```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from automl_infrastructure.classifiers.adapters import SklearnClassifierAdapter
from automl_infrastructure.classifiers import EnsembleClassifier
from automl_infrastructure.experiment import Experiment
from automl_infrastructure.experiment.observations import Avg, Std
from automl_infrastructure.experiment.params import RangedParameter, ListParameter
from automl_infrastructure.visualization import ConfusionMatrix


cords_df = pd.DataFrame([[5,0,'Low'], [9,3,'Low'], [8,5,'Low'], [12,8,'Low'], [3,0,'Low'],
                         [1,6,'High'], [5,9,'High'], [0,4,'High'], [9,15,'High'], [7,11,'High']],
                         columns=['X','Y','LABEL'])

# create models we want to examine
lr_model = SklearnClassifierAdapter(name='lr', sklearn_model=LogisticRegression())
rf_model = SklearnClassifierAdapter(name='rf', sklearn_model=RandomForestClassifier())

# declare hyper-params we want to optimize
hyper_parameters = {
    'rf': [ListParameter('max_depth', options=[2, 4, 6]), 
           ListParameter('n_estimators', options=[20, 50, 100])]
}

experiment = Experiment('experiment2', cords_df[['X','Y']], cords_df['LABEL'], 
                models=[lr_model, rf_model],
                hyper_parameters=hyper_parameters, 
                observations={
                    'avg_precision': Avg(metric='precision'),
                    'std_precision': Std(metric='precision'),
                    'avg_recall': Avg(metric='recall'),
                    'std_recall': Std(metric='recall')
                },
                visualizations={
                    'confusion_matrix': ConfusionMatrix(figsize=(5,5))
                },
                objective='accuracy'
            )

experiment.run(n_trials=20, n_jobs=1)
experiment.print_report()

```


Make sure to look at the [docs](https://htmlpreview.github.io/?https://github.com/barak1412/automl_infrastructure/blob/master/docs/sphinx/build/html/index.html) and [examples](/examples).
