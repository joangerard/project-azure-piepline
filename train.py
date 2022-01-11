#!/usr/bin/env python
# coding: utf-8
# %%
# azureml-core of version 1.0.72 or higher is required
# azureml-dataprep[pandas] of version 1.1.34 or higher is required
from azureml.core import Workspace, Dataset
# Import the model we are using
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import argparse
import numpy as c
import joblib
from azureml.data.dataset_factory import TabularDatasetFactory

# azureml-core of version 1.0.72 or higher is required
# azureml-dataprep[pandas] of version 1.1.34 or higher is required
from azureml.core import Workspace, Dataset

subscription_id = 'aa7cf8e8-d23f-4bce-a7b9-1f0b4e0ac8ee'
resource_group = 'aml-quickstarts-174280'
workspace_name = 'quick-starts-ws-174280'

workspace = Workspace(subscription_id, resource_group, workspace_name)

dataset = Dataset.get_by_name(workspace, name='divorce-ds')
df = dataset.to_pandas_dataframe()
df = df.sample(frac=1)


# %%


run = Run.get_context()


# %%


x = df.iloc[:,:-1]
y = df.iloc[:,-1]


# %%


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# %%
parser = argparse.ArgumentParser()
parser.add_argument('--e', type=int, default=1000, help="Number of estimators")
parser.add_argument('--md', type=int, default=100, help="Max Depth")
parser.add_argument('--msp', type=int, default=5, help="Min Samples Split")
args = parser.parse_args()

run.log('Number of estimators: ', np.int(args.e))
run.log('Max Depth: ', np.int(args.md))
run.log('Min Samples Split: ', np.int(args.msp))

# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(n_estimators = args.e, max_depth=args.md, min_samples_split=args.msp, random_state = 42)
# Train the model on training data
rf.fit(X_train, y_train);


# %%
joblib.dump(value=rf, filename="./outputs/model.joblib")

accuracy = rf.score(X_test, y_test)
run.log("Accuracy", accuracy)


# %%




