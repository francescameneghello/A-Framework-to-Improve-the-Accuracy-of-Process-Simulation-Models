import tkinter as tk
from tree import decisionTree
import pandas as pd
from dtreeviz.trees import dtreeviz 
import numpy
import math
import sys


# python3 window.py real.csv sim.csv
# python window.py real_timeConstraint.csv sim_timeConstraint.csv

constraint=['time:AlternatePrecedence(Traer informacion estudiante - banner, Cancelar Solicitud)', 'time:AlternatePrecedence(Radicar Solicitud Homologacion, Evaluacion curso)',
'time:AlternatePrecedence(Traer informacion estudiante - banner, Evaluacion curso)',
'time:AlternatePrecedence(Radicar Solicitud Homologacion, Homologacion por grupo de cursos)',
'time:AlternatePrecedence(Traer informacion estudiante - banner, Homologacion por grupo de cursos)', 
'time:AlternatePrecedence(Radicar Solicitud Homologacion, Notificacion estudiante cancelacion soli)',
'time:AlternatePrecedence(Traer informacion estudiante - banner, Notificacion estudiante cancelacion soli)',
'time:AlternatePrecedence(Traer informacion estudiante - banner, Revisar curso)',
'time:CoExistence(Radicar Solicitud Homologacion, Traer informacion estudiante - banner)',
'time:AlternatePrecedence(Radicar Solicitud Homologacion, Revisar curso)', 
'time:AlternatePrecedence(Traer informacion estudiante - banner, Validar solicitud)', 'time:CoExistence(Radicar Solicitud Homologacion, Traer informacion estudiante - banner)', 
'time:CoExistence(Homologacion por grupo de cursos, Validar solicitud)', 
'time:CoExistence(Notificacion estudiante cancelacion soli, Cancelar Solicitud)']

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
#data1= delete_features(data1)
#data1=select_risorse(data1)
#data1=select_constraint(data1)
#data1=data1.drop(['time:Amend Request for Quotation', 'time:Settle Dispute With Supplier'], axis=1)
'''
data1=data1.drop(['time:AlternatePrecedence(Traer informacion estudiante - banner, Cancelar Solicitud)', 'time:AlternatePrecedence(Radicar Solicitud Homologacion, Evaluacion curso)',
'time:AlternatePrecedence(Traer informacion estudiante - banner, Evaluacion curso)',
'time:AlternatePrecedence(Radicar Solicitud Homologacion, Homologacion por grupo de cursos)',
'time:AlternatePrecedence(Traer informacion estudiante - banner, Homologacion por grupo de cursos)', 
'time:AlternatePrecedence(Radicar Solicitud Homologacion, Notificacion estudiante cancelacion soli)',
'time:AlternatePrecedence(Traer informacion estudiante - banner, Notificacion estudiante cancelacion soli)',
'time:AlternatePrecedence(Traer informacion estudiante - banner, Revisar curso)',
'time:CoExistence(Radicar Solicitud Homologacion, Traer informacion estudiante - banner)',
'time:AlternatePrecedence(Radicar Solicitud Homologacion, Revisar curso)', 
'time:AlternatePrecedence(Traer informacion estudiante - banner, Validar solicitud)', 'time:CoExistence(Radicar Solicitud Homologacion, Traer informacion estudiante - banner)', 
'time:CoExistence(Homologacion por grupo de cursos, Validar solicitud)', 
'time:CoExistence(Notificacion estudiante cancelacion soli, Cancelar Solicitud)'], axis=1)
'''

data2=pd.read_csv(sys.argv[2], sep=',')
#data2=select_risorse(data2)
#data2=select_constraint(data2)
#data2= delete_features(data2)
#print(data2['time:Create Purchase Requisition'])
#data2=data2.drop(['time:AlternateResponse(Create Purchase Requisition, Analyze Request for Quotation)'], axis=1)
#data2=data2.drop(['time:Amend Request for Quotation', 'time:Settle Dispute With Supplier'], axis=1)


'''
data2=data2.drop(['time:AlternatePrecedence(Traer informacion estudiante - banner, Cancelar Solicitud)', 'time:AlternatePrecedence(Radicar Solicitud Homologacion, Evaluacion curso)',
'time:AlternatePrecedence(Traer informacion estudiante - banner, Evaluacion curso)',
'time:AlternatePrecedence(Radicar Solicitud Homologacion, Homologacion por grupo de cursos)',
'time:AlternatePrecedence(Traer informacion estudiante - banner, Homologacion por grupo de cursos)', 
'time:AlternatePrecedence(Radicar Solicitud Homologacion, Notificacion estudiante cancelacion soli)',
'time:AlternatePrecedence(Traer informacion estudiante - banner, Notificacion estudiante cancelacion soli)',
'time:CoExistence(Radicar Solicitud Homologacion, Traer informacion estudiante - banner)',
'time:AlternatePrecedence(Radicar Solicitud Homologacion, Revisar curso)','time:AlternatePrecedence(Traer informacion estudiante - banner, Revisar curso)', 
'time:AlternatePrecedence(Traer informacion estudiante - banner, Validar solicitud)', 'time:CoExistence(Radicar Solicitud Homologacion, Traer informacion estudiante - banner)', 
'time:CoExistence(Homologacion por grupo de cursos, Validar solicitud)', 
'time:CoExistence(Notificacion estudiante cancelacion soli, Cancelar Solicitud)'], axis=1)
''' 
tree= decisionTree(data1, data2)
accuracy, f_selected=tree.classifier()
print(f_selected)

tree.plotTree("C:/Users/fmeneghello/Desktop/purchaseExample/tempo2/font", save=True)