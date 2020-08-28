# https://scikit-learn.org/stable/modules/cross_validation.html
# https://towardsdatascience.com/fine-tuning-xgboost-in-python-like-a-boss-b4543ed8b1e
# https://scikit-learn.org/stable/auto_examples/model_selection/plot_cv_indices.html#sphx-glr-auto-examples-model-selection-plot-cv-indices-py
# https://github.com/WillKoehrsen/hyperparameter-optimization/blob/master/Bayesian%20Hyperparameter%20Optimization%20of%20Gradient%20Boosting%20Machine.ipynb
# https://www.kaggle.com/henrylidgley/xgboost-with-hyperopt-tuning

# Objective is to demonstrate:

# regression ✓
# binary classification ✓
# multiclass classification ✓
# cross-validation ✓
# hyperparameter searching ✓
# feature importance ✓
# early stopping ✓
# plotting ✓

# %%
from hgboost import hgboost
print(dir(hgboost))
# print(hgboost.__version__)
import numpy as np

# %% classifier
gs = hgboost(method='xgb_clf', max_evals=10, cv=5, eval_metric='auc', val_size=0.2, random_state=42)
# gs = hgboost(method='xgb_clf', max_evals=25, cv=5, eval_metric='auc', val_size=None, random_state=42)

df = gs.import_example()
y = df['Survived'].values
del df['Survived']
X = gs.preprocessing(df, verbose=0)

y = y.astype(str)
y[y=='1']='survived'
y[y=='0']='dead'

# results = gs.fit(X, y=='survived')
results = gs.fit(X, y, pos_label='survived')

# use the predictor
y_pred, y_proba = gs.predict(X)

# Make some plots
gs.plot_params()
gs.plot()
gs.treeplot()
gs.plot_validation()
gs.plot_cv()

# %% multi-classifier
gs = hgboost(method='xgb_clf_multi', max_evals=10, cv=5, eval_metric='kappa', val_size=0.2, random_state=42)

df = gs.import_example()
y = df['Parch'].values
y[y>=3]=3
del df['Parch']
X = gs.preprocessing(df, verbose=0)

# Fit
results = gs.fit(X, y)

# use the predictor
y_pred, y_proba = gs.predict(X)

# Make some plots
gs.plot_params()
gs.plot()
gs.treeplot()
gs.plot_validation()
gs.plot_cv()

# %% Regression
gs = hgboost(method='xgb_reg', max_evals=15, cv=5, val_size=0.2, eval_metric='rmse')
gs = hgboost(method='ctb_reg', max_evals=15, cv=5, val_size=0.2, eval_metric='mae')
# gs = hgboost(method='lgb_reg', max_evals=15, cv=5, val_size=0.2)
# gs = hgboost(method='xgb_reg', max_evals=200, cv=5, val_size=None)
# gs = hgboost(method='xgb_reg', max_evals=200, cv=None, val_size=0.2)
# gs = hgboost(method='xgb_reg', max_evals=200, cv=None, val_size=None)
# gs = hgboost(method='xgb_reg')
# gs = hgboost(method='lgb_reg')
# gs = hgboost(method='ctb_reg')

df = gs.import_example()
y = df['Age'].values
del df['Age']
I = ~np.isnan(y)
X = gs.preprocessing(df, verbose=0)
y = y[I]
X = X.loc[I,:]

# Fit
results = gs.fit(X, y)

# Prdict
y_pred, y_proba = gs.predict(X)

# Plot
gs.plot_params()
gs.plot()
gs.treeplot()
gs.plot_validation()
gs.plot_cv()

# %% CLASSIFICATION TWO-CLASS #####
from sklearn import datasets
import pandas as pd

iris = datasets.load_iris()
X = pd.DataFrame(iris.data, columns=iris['feature_names'])
y = iris.target

gs = hgboost(method='xgb_clf', max_evals=100, eval_metric='auc')
results = gs.fit(X, y==1)

# Plot
gs.plot_params()
gs.plot()
gs.treeplot()
gs.plot_validation()

# %% CLASSIFICATION MULTI-CLASS #####
iris = datasets.load_iris()
X = pd.DataFrame(iris.data, columns=iris['feature_names'])
y = iris.target

gs = hgboost(method='xgb_clf_multi', max_evals=100, eval_metric='mlogloss')
results = gs.fit(X, y)
gs.treeplot()
gs.plot()
gs.plot_validation()