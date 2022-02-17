import numpy as np
from catboost import Pool
from sklearn.metrics import mean_squared_error
from catboost import CatBoostRegressor

X= np.load('features.npy')
y = np.load('label.npy')
X_train = X[:100000]
y_train = y[:100000]
X_val = X[100000:]
y_val = y[100000:]


final_model = CatBoostRegressor(
    iterations=3000,
    learning_rate=0.07,
    depth=12,
    l2_leaf_reg=1,
    task_type='GPU',
    devices='0'
)
final_model.fit(
    X_train,
    y_train,
    early_stopping_rounds=100,
)