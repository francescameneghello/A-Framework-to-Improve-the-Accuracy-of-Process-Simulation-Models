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

from tree import decisionTree
from createDataset import *
from Resource import resource
from tqdm import tqdm
from Declare import checkCostraints
from Temporal_start_complete import time_start_complete, timeConstraint
import sys


# python training_dataset.py real_log.xes simulated_log.xes constraint_Minerful.csv C/T/CT

print("Input Argument", str(sys.argv))


data= createDataset(sys.argv[1], sys.argv[2])
real, sim= data.dataset("real.csv", "sim.csv")


conR=checkCostraints(sys.argv[3], real, data.getReal())
data1=conR.insertCostraints()

conS=checkCostraints(sys.argv[3],sim, data.getSim())
data2=conS.insertCostraints()


if sys.argv[4]=='C':
    data1.to_csv("controlflow_real.csv", index=False)
    data2.to_csv("controlflow_sim.csv", index=False)

if sys.argv[4]=='T':
    timeR= time_start_complete(data.getReal(),data.getReal(), data1)
    data1=timeR.timeTask_Process()
    data1.to_csv("time_real.csv", index=False)

    timeS=time_start_complete(data.getSim(),data.getReal(), data2)
    data2=timeS.timeTask_Process()
    data2.to_csv("time_sim.csv", index=False)


if sys.argv[4]=='CT':
    timeConstraintReal=timeConstraint(sys.argv[3], data1, sys.argv[1])
    data1=timeConstraintReal.addTimeConstraint()
    data1.to_csv("controlTime_real.csv", index=False)

    timeConstraintSim=timeConstraint(sys.argv[3], data2, sys.argv[2])
    data2=timeConstraintSim.addTimeConstraint()
    data2.to_csv("controlTime_sim.csv", index=False)

