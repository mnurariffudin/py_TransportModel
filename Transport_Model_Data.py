import pandas as pd

class Data:

    excel_file = "Input_TransportProblem.xlsx"
    df_sheets = ["Location","Distance","Cost"]

    df_location = pd.read_excel(excel_file,df_sheets[0])
    df_distance = pd.read_excel(excel_file,df_sheets[1])
    df_cost = pd.read_excel(excel_file,df_sheets[2])

    #Variables
    S_Locations = df_location.Location.to_list()

    #Parameters
    P_Availability = df_location.set_index("Location").Supply.to_dict()
    P_Demand = df_location.set_index("Location").Demand.to_dict()
    P_Price = df_location.set_index("Location").Price.to_dict()
    P_Cost = df_cost.iloc[0,1]
    P_Distance = df_distance.set_index(["Origin","Destination"]).Distance.to_dict()
