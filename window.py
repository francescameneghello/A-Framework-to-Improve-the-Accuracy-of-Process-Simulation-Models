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


import tkinter as tk
from tree import decisionTree
import pandas as pd
from dtreeviz.trees import dtreeviz 
import numpy
import math
import sys


# python3 window.py real.csv sim.csv
# python window.py real_timeConstraint.csv sim_timeConstraint.csv

def delete_features(data):
    delete=[]
    for key in data:
        if "time" not in key and key!='Log':
        #if key not in constraint and key!='Log':
            delete.append(key)
    
    data=data.drop(delete, axis=1)
    
    return data

def select_risorse(data):
    delete=[]
    for key in data:
        if "R:" not in key and key!='Log':
            delete.append(key)
    
    data=data.drop(delete, axis=1)
    
    return data

def select_constraint(data):
    delete=[]
    for key in data:
        if "Analyze Request for Quotation" in key or "Create Request for Quotation" in key:
            delete.append(key)
            
    data=data.drop(delete, axis=1)
    
    return data

print("Input Argument", str(sys.argv))

data1=pd.read_csv(sys.argv[1], sep=',')

data2=pd.read_csv(sys.argv[2], sep=',')

tree= decisionTree(data1, data2)
accuracy, f_selected=tree.classifier()
print(f_selected)

tree.plotTree("path", save=True)