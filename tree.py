from sklearn import tree # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics
from matplotlib import pyplot as plt
from dtreeviz.trees import dtreeviz 
import graphviz 
import numpy as np
import pandas as pd

from dtreeviz.trees import *


class decisionTree():

    def __init__(self, data1, data2):
        self.real=data1
        self.sim=data2

    def getValueData(self,feature):
        return [sum(self.real[feature]), sum(self.sim[feature])]
    
    def mean_median(self, val):
        val_mean=[]
        for i in val:
            if type(val[i])==float:
                val_mean.append(val[i])
                
        return np.mean(val_mean), np.median(val_mean)

    def featureTimeSelection(self, key):
        meanR=np.mean(self.real[key])
        meanS=np.mean(self.sim[key])
        medianR=np.median(self.real[key])
        medianS=np.median(self.sim[key])
        result=True
        if (max([meanR, meanS])-min([meanR, meanS]))<=5 and (max([medianR, medianS])-min([medianR, medianS]))<=5:
            result=True
        else:
            result=False
        
        return result
    
    def featureTimeSelectionMod(self, key):
        meanR=np.mean(self.real[key])
        meanS=np.mean(self.sim[key])
        medianR=np.median(self.real[key])
        medianS=np.median(self.sim[key])
        mean_check=0.1*meanR
        median_check=0.1*medianR
        result=True
        if (max([meanR, meanS])-min([meanR, meanS]))<=mean_check and (max([medianR, medianS])-min([medianR, medianS]))<=median_check:
        #if (max([meanR, meanS])-min([meanR, meanS]))<=mean_check:
            result=True
        else:
            result=False
        
        return result
    
        

    def featureSelection(self):
        thresholdR=0.95*len(self.real)
        thresholdS=0.95*len(self.sim)
        self.dataset = pd.concat([self.real, self.sim])
        self.X=self.dataset
        delete=['Log']
        columns=(self.dataset.drop('Log', axis=1)).columns
        self.columnsTrain=[]
        string=""
        j=0
        for i in range(len(columns)):
            key=columns[i]
            if "time:" not in key or "R:" in key:
                if 0<=sum(self.real[key])<=(len(self.real)-thresholdR) and 0<=sum(self.sim[key])<=(len(self.sim)-thresholdS):
                    delete.append(key)
                elif thresholdR<=sum(self.real[key])<=(len(self.real)) and thresholdS<=sum(self.sim[key])<=len(self.sim):
                    delete.append(key)
                elif sum(self.sim[key]) >= sum(self.real[key])-12 and sum(self.sim[key]) <= sum(self.real[key])+12:
                    delete.append(key)
                else:
                    string=string + str(j) + ". " + columns[i] + "   " + str(sum(self.real[key])) +  "    "  + str(sum(self.sim[key])) + "\n"
                    self.columnsTrain.append(columns[i])
                    j=j+1
            else:
                if self.featureTimeSelectionMod(key):
                    delete.append(key)
                else:
                    string=string + str(j) + ". " + columns[i] + "   " + "Media: " + str(round(np.mean(self.real[key]))) +  "    "  + str(round(np.mean(self.sim[key])))  + "    " + "STD: " + str(round(np.std(self.real[key]))) + "      " + str(round(np.std(self.sim[key]))) + "\n"
                    j=j+1
        self.X=self.X.drop(delete, axis=1)
        return self.X, string

    def classifier(self):
        self.dataset = pd.concat([self.real, self.sim])
        self.X,string = self.featureSelection()
        y = self.dataset.Log
        #self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.0000001, random_state=1)
        min=int(len(self.dataset)*0.1)
        self.clf = tree.DecisionTreeClassifier(min_samples_split=min, min_samples_leaf=min)
        # Train Decision Tree Classifer
        self.clf = self.clf.fit(self.X, y)
        #Predict the response for test dataset
        #self.y_pred = self.clf.predict(self.X_test)
        #dot_data = tree.export_graphviz(self.clf, out_file=None, feature_names=self.X.columns,class_names=[ 'real', 'simulation'], filled=True, rounded=True)
        return metrics.accuracy_score(y, y), string
    

    def plotConfusionMatrix(self):
        disp = metrics.plot_confusion_matrix(self.clf, self.X_test, self.y_test,display_labels=['real', 'simulation'],cmap=plt.cm.Blues)
        disp.ax_.set_title("Confusion Matrix")
        plt.savefig('confusion_matrix.jpg')
        plt.show()

    def feature_importances(self):
        for name, val in zip(self.columnsTrain, self.clf.feature_importances_):
            if val>0.1:
                print(name + "->" + str(val))

    def plotTree(self, name,save=True):
        dot_data = tree.export_graphviz(self.clf, out_file=None, feature_names=self.X.columns,class_names=[ 'real', 'simulation'], filled=True, rounded=True) 
        graph = graphviz.Source(dot_data) 
        graph.render(name)
        y = self.dataset.Log
        viz = dtreeviz(self.clf, self.X, y, feature_names=self.X.columns, class_names=["Real event log", "Simulated event log"], scale=1, label_fontsize= 20, ticks_fontsize= 16)  
        viz.view()
