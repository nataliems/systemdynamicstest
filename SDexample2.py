# -*- coding: utf-8 -*-

# reference:
# Pruyt, E., 2013. Small System Dynamics Models for Big Issues: Triple Jump towards Real-World Complexity. Delft: TU Delft Library. 324p.
# Exercise 6.6: Gangs and Arm Races

# the plots below should fit the escalation archetype on page 45 - why don't they?

## CREATE MODEL ##

from BPTK_Py import Model
from BPTK_Py import sd_functions as sd
import matplotlib.pyplot as plt

# time is measured in months
model = Model(starttime=0.0,stoptime=100.0,dt=1.0,name='ArmsRace')

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
obsolescense_ofA.equation = 0.10 # obsolescence rate is 10%
obsolescense_ofB.equation = 0.10 # obsolescence rate is 10%

# define converters
relative_A.equation = (overassessment_ofBbyA * obsolescense_ofA * armsstock_B) - (obsolescense_ofA * armsstock_A)
relative_B.equation = (overassessment_ofAbyB * obsolescense_ofB * armsstock_A) - (obsolescense_ofB * armsstock_B)

# define stocks (positive for inflow, negative for outflow)
armsstock_A.equation = arming_A
armsstock_B.equation = arming_B

# define flows
arming_A.equation = sd.max(0.0,(autonomous_A + relative_A)) # flows must be nonnegative
arming_B.equation = sd.max(0.0,(autonomous_B + relative_B)) # flows must be nonnegative

# What are the differencees between A and B? ONLY the overassessment rate!

## CREATE FRAMEWORK ##

import BPTK_Py
bptk = BPTK_Py.bptk()

# create scenario manager
scenario_manager = {
    "smArmsRace":{

    "model": model,
    "base_constants": {
        "autonomous_A": 0.05,
        "autonomous_B": 0.05,
        "overassessment_ofBbyA": 1.10,
        "overassessment_ofAbyB": 1.0,
        "obsolescense_ofA": 0.1,
        "obsolescense_ofB": 0.1,

    },
 }
}

# register scenario manager
bptk.register_scenario_manager(scenario_manager)

## QUESTION 1 ##

# create the base scenario
bptk.register_scenarios(
    scenarios =
        {
            "basescenario": {

            }
        },
    scenario_manager="smArmsRace")

# plot the scenario and create dataframe
bptk.plot_scenarios(
    scenarios="basescenario",
    scenario_managers="smArmsRace",
    equations=["armsstock_A", "armsstock_B"])

plt.savefig('basescenarioplot.png')

question1 = bptk.plot_scenarios(
    scenarios="basescenario",
    scenario_managers="smArmsRace",
    equations=["armsstock_A", "armsstock_B"],
    return_df = True)

question1[0:10]

## QUESTION 2 ##

# create the new scenario
bptk.register_scenarios(
    scenarios =
        {
            "newscenario": {
                "constants": {
                    "overassessment_ofBbyA": 0.5,
                }
            }
        }
    ,
    scenario_manager="smArmsRace")

# plot the scenario and create dataframe
bptk.plot_scenarios(
    scenarios="newscenario",
    scenario_managers="smArmsRace",
    equations=["armsstock_A", "armsstock_B"])

plt.savefig('newscenarioplot.png')

question2 = bptk.plot_scenarios(
    scenarios="newscenario",
    scenario_managers="smArmsRace",
    equations=["armsstock_A", "armsstock_B"],
    return_df = True)

question2[0:10]

## CREATE DASHBOARD ##

# reference: 
# https://bptk.transentis-labs.com/en/latest/docs/general/how-to/how_to_interactive_dashboards/how_to_interactive_dashboards.html
# NOTE: It is important to mention that everytime you move a slider/checkbox, the underlying model equations are modified. This means, the results of the scenario will also deviate in other plots of the same scenario. You may reuse the modifications to the model in further plots. If this is not what you want, a quick workaround is to initiliaze another instance of BPTK_Py and run the dashboard function independently from the other instance(s).

# NOTE 2: can't actually run bptk dashboards in Spyder - requires Jupyter widgets!
# https://stackoverflow.com/questions/45826404/cannot-import-widget-from-ipython-html-widgets-in-spyder

bptk.dashboard(scenario_managers=["smArmsRace"],
                                scenarios=["basescenario"],
                                kind="area",
                                equations=["armsstock_A","armsstock_B"],
                                stacked=False,
                                strategy=False,
                                freq = "D",
                                title="Interactive Plotting",
                                x_label="Month",
                                y_label="Arms Stock",
                                constants=[
                                    ("slider","overassessment_ofBbyA",0,1),
                                    ("slider","overassessment_ofAbyB",0,1)]
                                )


