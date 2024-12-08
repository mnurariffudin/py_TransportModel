import pandas as pd

#class Data:

excel_file = "Input_TransportProblem.xlsx"
df_sheets = ["Location","Distance","Cost"]

df_location = pd.read_excel(excel_file,df_sheets[0])
df_distance = pd.read_excel(excel_file,df_sheets[1])
df_cost = pd.read_excel(excel_file,df_sheets[2])

#Variables
location_list = df_location.Location.to_list()

#Parameters
availability = df_location.set_index("Location").Supply.to_dict()
demand = df_location.set_index("Location").Demand.to_dict()
price = df_location.set_index("Location").Price.to_dict()
cost = df_cost.iloc[0,1]
distance = df_distance.set_index(["Origin","Destination"]).Distance.to_dict()
