'''
Copyright 2021, ESTECO s.p.a 

This file is part of A-Framework-to-Improve-the-Accuracy-of-Process-Simulation-Models.

A-Framework-to-Improve-the-Accuracy-of-Process-Simulation-Models is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation version 3 of the License.

A-Framework-to-Improve-the-Accuracy-of-Process-Simulation-Models is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with A-Framework-to-Improve-the-Accuracy-of-Process-Simulation-Models. 
If not, see <https://www.gnu.org/licenses/>.

This project was developed by Francesca Meneghello with the supervision of  
Fabio Asnicar, Massimiliano de Leoni, Alessandro Turco, as part of the collaboration between ESTECO s.p.a and the University of Padua
'''

import pandas as pd
from tree import decisionTree
from dtreeviz.trees import dtreeviz 
from sklearn import tree as t
from sklearn.preprocessing import StandardScaler

def select_risorse(data):
    delete=[]
    for key in data:
        if "R:" not in key and key!='Log':
            delete.append(key)
    data=data.drop(delete, axis=1)
    return data

real=pd.read_csv('real.csv', sep=',')
real=select_risorse(real)
sim=pd.read_csv('sim.csv', sep=',')
dataset = pd.concat([real, sim])
dataset.reset_index(drop=True, inplace=True)


def create_df(set_task, size):
    data=dict()
    for elem in set_task:
        data[elem]=[0.0] * size
    return pd.DataFrame(data=data)

def classify(X, y, columns, name):
    min=int(len(X)*0.1)
    clf = t.DecisionTreeClassifier(min_samples_split=min, min_samples_leaf=min)
    clf = clf.fit(X, y)
    viz = dtreeviz(clf, X, y, feature_names=columns, class_names=["real", "simulation"])  
    viz.save(name)  


def normalization(X):
    columns=X.columns
    X_new=X.copy()
    for column in columns:
        mean=X[column].mean()
        std=X[column].std()
        for i in range(0, len(columns)):
            val=X.iloc[i][column]
            X_new.at[i, column]=(val-mean)/std
    return X_new


def denormalization(X):
    columns=X.columns
    X_new=X.copy()
    for column in columns:
        mean=X[column].mean()
        std=X[column].std()
        for i in range(0, len(columns)):
            val=X.iloc[i][column]
            X_new.at[i, column]=(val*mean) + std
    return X_new


tree= decisionTree(real, sim)
X, string= tree.featureSelection()
y =dataset.Log
print(string)


################ Z-SCORE ###############################

std_scaler = StandardScaler()
new_X= std_scaler.fit_transform(X)


min=int(len(X)*0.1)
clf = t.DecisionTreeClassifier(min_samples_split=min, min_samples_leaf=min)
clf = clf.fit(new_X, y)

viz = dtreeviz(clf, new_X, y, feature_names=X.columns, class_names=["Real event log", "Simulated event log"])  
viz.view()


X1=std_scaler.inverse_transform(new_X)


media=new_X.mean()
deviation= new_X.std()

clf.tree_.threshold[0]= (clf.tree_.threshold[0]*deviation) + media





