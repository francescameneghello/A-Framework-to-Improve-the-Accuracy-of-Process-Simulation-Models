######### GENERAZIONE DI DIVERSE NORMALIZZAZIONI #########
import pandas as pd
from tree import decisionTree
from dtreeviz.trees import dtreeviz 
from sklearn import tree as t
import numpy
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import MinMaxScaler
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
            #print("VAL ", val)
            X_new.at[i, column]=(val*mean) + std
            #print("NEW_VAL ", X_new.iloc[i][column])
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

print(clf.tree_.threshold)


media=new_X.mean()
print(media)
deviation= new_X.std()
print(deviation)

clf.tree_.threshold[0]= (clf.tree_.threshold[0]*deviation) + media

print(clf.tree_.threshold)





