# -*- coding: utf-8 -*-

# reference:
# Pruyt, E., 2013. Small System Dynamics Models for Big Issues: Triple Jump towards Real-World Complexity. Delft: TU Delft Library. 324p.
# Exercise 6.6: Gangs and Arm Races

from BPTK_Py import Model
from BPTK_Py import sd_functions as sd

# time is measured in months
model = Model(starttime=0.0,stoptime=100.0,dt=1.0,name='SimpleProjectManagement')

# define elements
armsstock_A = model.stock("armsstock_A")
armsstock_B = model.stock("armsstock_B")
arming_A = model.flow("arming_A")
arming_B = model.flow("arming_B")
relative_A = model.converter("relative_A")
relative_B = model.converter("relative_B")
autonomous_A = model.constant("autonomous_A")
autonomous_B = model.constant("autonomous_B")
overassessment_ofBbyA = model.constant("overassessment_ofBbyA")
overassessment_ofAbyB = model.constant("overassessment_ofAbyB")
obsolescense_ofA = model.constant("obsolescense_ofA")
obsolescense_ofB = model.constant("obsolescense_ofB")

# initialize stocks
armsstock_A.initial_value = 1.0 #100% of weapons required to destroy B
armsstock_B.initial_value = 1.0 #100% of weapons required to destroy A

# define constants
autonomous_A.equation = 0.05
autonomous_B.equation = 0.05
overassessment_ofBbyA.equation = 1.10
overassessment_ofAbyB.equation = 1.0 # correctly assessed, so factor of 1
obsolescense_ofA.equation = 0.90 # obsolescence rate is 10%
obsolescense_ofB.equation = 0.90 # obsolescence rate is 10%

# define converters
relative_A.equation = (overassessment_ofBbyA * obsolescense_ofA * armsstock_B) - (obsolescense_ofA * armsstock_A)
relative_B.equation = (overassessment_ofAbyB * obsolescense_ofB * armsstock_A) - (obsolescense_ofB * armsstock_B)

# define stocks (positive for inflow, negative for outflow)
armsstock_A.equation = arming_A
armsstock_B.equation = arming_B

# define flows
arming_A.equation = sd.max(0.0, (autonomous_A + relative_A))
arming_B.equation = sd.max(0.0, (autonomous_B + relative_B))



