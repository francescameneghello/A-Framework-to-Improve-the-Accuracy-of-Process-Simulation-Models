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

from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.footprints import algorithm as footprints_discovery
import pandas as pd

class createDataset():

    def __init__(self, path_real, path_sim):
        try:
            self.real=xes_importer.apply(path_real)
            self.sim=xes_importer.apply(path_sim)
            self.sizeReal=len(self.real)
            self.sizeSim=len(self.sim)
            self.attrib=set()
        except FileNotFoundError:
            print("ERROR: File not found")

    def discovery_features_xes(self, log):
        for trace in log:
            for event in range(len(trace)-1):
                column=trace[event]['concept:name']+'>'+trace[event+1]['concept:name']
                self.attrib.add(column)
    
    def addTask(self, log):
        for i,c in enumerate(log):
            for j,e in enumerate(c):
                self.attrib.add(log[i][j]['concept:name'])


    def discovery(self):
        self.discovery_features_xes(self.real)
        self.discovery_features_xes(self.sim)
        self.addTask(self.real)
        self.addTask(self.sim)
    
    def create_empty_df(self, size):
        data=dict()
        for elem in self.attrib:
            data[elem]=[0] * size
        return pd.DataFrame(data=data)

    def create_df(self, log, size):
        self.discovery()
        dataframe=self.create_empty_df(size)
        i=0
        for trace in log:
            for event in range(len(trace)):
                if event<len(trace)-1:
                    column=trace[event]['concept:name']+'->'+ trace[event+1]['concept:name']
                    dataframe[column][i]=dataframe[column][i]+1
                task=trace[event]['concept:name']
                dataframe[task][i]=dataframe[task][i]+1
            i=i+1
        return dataframe
    
    def dataset(self, name1, name2):
        real=self.create_df(self.real, self.sizeReal)
        real["Log"]=[0]*self.sizeReal
        sim=self.create_df(self.sim, self.sizeSim)
        sim["Log"]=[1]*self.sizeSim
        deleteAnd=self.delete_and()
        real=real.drop(deleteAnd, axis=1)
        sim=sim.drop(deleteAnd, axis=1)
        self.write_csv(real, name1)
        self.write_csv(sim, name2)
        return real, sim
    
    def find_relation(self, task):
        set_relation=set()
        for key in self.attrib:
            if task in key and '->' in key:
                set_relation.add(key)
        return set_relation

    def delete_and(self):
        fp_real = footprints_discovery.apply(self.real, variant=footprints_discovery.Variants.ENTIRE_EVENT_LOG)
        fp_sim = footprints_discovery.apply(self.sim, variant=footprints_discovery.Variants.ENTIRE_EVENT_LOG)
        delete_and=set()
        intersection=list(fp_real['parallel'].intersection(fp_sim['parallel']))
        for i in range(len(intersection)):
            task1=intersection[i][0]
            task2=intersection[i][1]
            delete_and.add(task1+'->'+task2)
        return list(delete_and)


    def write_csv(self, df, name):
        df.to_csv(name, index=False)


    def getReal(self):
        return self.real

    def getSim(self):
        return self.sim