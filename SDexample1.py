# -*- coding: utf-8 -*-

# reference:
# transetis labs. (2020). BPTK_PY Docs 1.1: A simple Python library for system dynamics. Retrieved from https://bptk.transentis-labs.com/en/latest/docs/sd-dsl/in-depth/in_depth_sd_dsl/in_depth_sd_dsl.html 

from BPTK_Py import Model
from BPTK_Py import sd_functions as sd

model = Model(starttime=0.0,stoptime=120.0,dt=1.0,name='SimpleProjectManagement')

# define elements
openTasks = model.stock("openTasks")
closedTasks = model.stock("closedTasks")
staff = model.stock("staff")
completionRate = model.flow("completionRate")
currentTime = model.converter("currentTime")
remainingTime = model.converter("remainingTime")
schedulePressure = model.converter("schedulePressure")
productivity = model.converter("productivity")
deadline = model.constant("deadline")
effortPerTask = model.constant("effortPerTask")
initialStaff = model.constant("initialStaff")
initialOpenTasks = model.constant("initialOpenTasks")

# initialize stocks
closedTasks.initial_value = 0.0
staff.initial_value = initialStaff
openTasks.initial_value = initialOpenTasks

# define constants
deadline.equation = 100.0
effortPerTask.equation = 1.0
initialStaff.equation = 1.0
initialOpenTasks.equation = 100.0

# define converters
currentTime.equation= sd.time()
remainingTime.equation = deadline - currentTime
schedulePressure.equation = sd.min((openTasks*effortPerTask)/(staff*sd.max(remainingTime,1)),2.5)
model.points["productivity"] = [
    [0,0.4],
    [0.25,0.444],
    [0.5,0.506],
    [0.75,0.594],
    [1,1],
    [1.25,1.119],
    [1.5,1.1625],
    [1.75,1.2125],
    [2,1.2375],
    [2.25,1.245],
    [2.5,1.25]
]
productivity.equation = sd.lookup(schedulePressure,"productivity")

# define stocks (positive for inflow, negative for outflow)
openTasks.equation = -completionRate
closedTasks.equation = completionRate

# define flows
completionRate.equation = sd.max(0.0, sd.min(openTasks, staff*(productivity/effortPerTask)))

# plots for first stage
model.plot_lookup("productivity")
closedTasks.plot()

## MODEL COMPLETE ##
## CREATE FRAMEWORK ##

import BPTK_Py
bptk = BPTK_Py.bptk()

# create scenario manager
scenario_manager = {
    "smSimpleProjectManagementDSL":{

    "model": model,
    "base_constants": {
        "deadline": 100.0,
        "initialStaff": 1.0,
        "effortPerTask": 1.0,
        "initialOpenTasks": 100.0,

    },
    "base_points":{
            "productivity": [
                [0.0,0.4],
                [0.25,0.444],
                [0.5,0.506],
                [0.75,0.594],
                [1,1],
                [1.25,1.119],
                [1.5,1.1625],
                [1.75,1.2125],
                [2,1.2375],
                [2.25,1.245],
                [2.5,1.25]
            ]
    }
 }
}

# register scenario manager
bptk.register_scenario_manager(scenario_manager)

# create a scenario
bptk.register_scenarios(
    scenarios =
        {
            "scenario80": {
                "constants": {
                    "initialOpenTasks": 80.0
                }
            }
        }
    ,
    scenario_manager="smSimpleProjectManagementDSL")

# plot the scenario
bptk.plot_scenarios(
    scenarios="scenario80",
    scenario_managers="smSimpleProjectManagementDSL",
    equations="openTasks")

# register a few more scenarios
bptk.register_scenarios(
    scenarios =
    {
         "scenario100": {

        },
        "scenario120": {
            "constants": {
                "initialOpenTasks" : 120.0
            }
        }
    },
    scenario_manager="smSimpleProjectManagementDSL")

# compare scenarios
bptk.plot_scenarios(
    scenarios="scenario80,scenario100,scenario120",
    scenario_managers="smSimpleProjectManagementDSL",
    equations="openTasks",
    series_names={
        "smSimpleProjectManagementDSL_scenario80_openTasks":"scenario80",
        "smSimpleProjectManagementDSL_scenario100_openTasks":"scenario100",
        "smSimpleProjectManagementDSL_scenario120_openTasks":"scenario120"
    }
)