from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.util import sorting
from pm4py.objects.log.util import func

from pm4py.util import constants
import pandas as pd

from sklearn import tree 
from sklearn.model_selection import train_test_split 
from sklearn import metrics
from matplotlib import pyplot as plt
import numpy as np


class time_start_complete():

    def __init__(self, log, real_log, df):
        self.log=log
        self.real_log=real_log
        self.df=df
        self.size=len(df)
        self.type=type

    def timeProcess(self):
        timeProcess=[]
        for trace in self.log:
            start=trace[0]['start:timestamp']
            end=trace[len(trace)-1]['time:timestamp']
            diff=end-start
            minuti=round(diff.total_seconds()/3600)
            timeProcess.append(minuti)
        self.df['timeProcess']=timeProcess

    def days_hours_minutes(self, td):
        return td.days, td.seconds//3600, (td.seconds//60)%60

    def find_task(self):
        tasks=set()
        for i,c in enumerate(self.real_log):
            for j,e in enumerate(c):
                tasks.add(self.real_log[i][j]['concept:name'])
        return tasks

    def create_dfTime(self):
        data=dict()
        for elem in self.find_task():
            column="time:" + elem
            data[column]=[-1] * self.size
        timedf= pd.DataFrame(data=data, dtype='object')   
        return timedf


    def timeTask_Process(self):
        #self.timeProcess()
        i=0
        timedf=self.create_dfTime()
        for trace in self.log:
            for event in trace:
                start=event['start:timestamp']
                complete=event['time:timestamp']
                diff=complete-start
                column="time:"+event['concept:name']
                minuti=diff.total_seconds()
                timedf[column][i]=round(minuti)
            i=i+1
        self.df=pd.concat([self.df, timedf], axis=1)
        return self.df


class timeConstraint():

    def __init__(self, path_costraints, df, path_log):
        try:
            self.constraints = pd.read_csv(path_costraints, sep=',')
            self.df=df
            self.log=xes_importer.apply(path_log)
            print(self.log[0])
        except FileNotFoundError:
            print("ERROR: File not found")

    def addTimeConstraint(self):
        self.target_activation()
        return self.constraint()

    def target_activation(self):
        self.vincoli=dict()
        for i in range(len(self.constraints)):
            key=self.constraints['Constraint'][i]
            self.vincoli[key]=(self.constraints['Activation'][i], self.constraints['Target'][i])
    
    def create_dfTime(self):
        data=dict()
        for key in self.vincoli:
            column="time:" + key
            data[column]=[-1] * len(self.df)
        timeV= pd.DataFrame(data=data, dtype='object') 
        print(timeV.columns)
        return timeV

    def constraint(self):
        timeV=self.create_dfTime() 
        for key in self.vincoli:
            for trace in range(0, len(self.df)):
                if self.df[key][trace]==False:
                    timeV["time:"+key][trace]=-1
                else:
                    minuti=0
                    activation=self.vincoli[key][0]
                    target=self.vincoli[key][1]
                    timeA=-1
                    timeB=-1
                    j=0
                    while j<len(self.log[trace]):
                        if self.log[trace][j]['concept:name']==activation and timeA==-1:
                            timeA_complete=self.log[trace][j]['time:timestamp']
                            timeA_start=self.log[trace][j]['start:timestamp']
                            timeA=0
                        if self.log[trace][j]['concept:name']==target and timeB==-1:
                            timeB_complete=self.log[trace][j]['time:timestamp']
                            timeB_start=self.log[trace][j]['start:timestamp']
                            timeB=0
                        j=j+1

                    if timeB==-1 or timeA==-1:
                        timeV["time:"+key][trace]=-1
                    else:
                        if timeA_complete>timeB_complete:
                            diff=timeA_start-timeB_complete
                            minuti=diff.total_seconds()
                        else: 
                            diff=timeB_start-timeA_complete
                            minuti=diff.total_seconds()
                        if minuti<0:
                            minuti=round(minuti*-1)
                        timeV["time:"+key][trace]=round(minuti)
        
        self.df = pd.concat([self.df, timeV], axis=1)
        return self.df
    