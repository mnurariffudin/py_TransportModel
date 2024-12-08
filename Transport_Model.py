import gurobipy
from gurobipy import GRB
import pandas as pd
from Transport_Model_Data import Data

# Model
model = gurobipy.Model("Transport Model")

# Variables
V_Flow = model.addVars(
            Data.S_Locations,Data.S_Locations, name="Flow")

# Constraints
# Supply Availability
C_SupplyAvailability = model.addConstrs(
    (
        gurobipy.quicksum(
            V_Flow[i_origin,i_destination]
            for i_destination in Data.S_Locations
            if Data.P_Distance[i_origin,i_destination]>0
        )
        <= Data.P_Availability[i_origin]
        for i_origin in Data.S_Locations
    ),
    name = 'C_SupplyAvailability'
)

# Demand Fulfilment
C_DemandFulfilment = model.addConstrs(
    (
        gurobipy.quicksum(
            V_Flow[i_origin,i_destination]
        for i_origin in Data.S_Locations
        if Data.P_Distance[i_origin,i_destination]>0
        )
        >= Data.P_Demand[i_destination]
        for i_destination in Data.S_Locations
    ),
    name = 'C_DemandFulfilment'
)

# Objective Function
V_Obj = gurobipy.quicksum(
    ((Data.P_Price[i_origin]
    + Data.P_Distance[i_origin,i_destination] 
    * Data.P_Cost) 
    * V_Flow[i_origin, i_destination]
    )
    for i_origin in Data.S_Locations
    for i_destination in Data.S_Locations
    if Data.P_Distance[i_origin,i_destination]>0
)

model.setObjective(V_Obj, GRB.MINIMIZE)

# Run

model.optimize()
model.printAttr("X")

if model.status == GRB.OPTIMAL:
    P_Supply = [(i_origin,i_destination,
        V_Flow[i_origin,i_destination].X)
            for i_origin in Data.S_Locations
            for i_destination in Data.S_Locations
    ]

    df_Supply = pd.DataFrame(P_Supply, columns=["Origin","Destination","Supply"])
    df_Supply_Pivot = df_Supply.groupby("Destination")["Supply"].sum().reset_index()
