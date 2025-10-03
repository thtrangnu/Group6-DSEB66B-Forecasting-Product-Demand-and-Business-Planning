import pandas as pd
import os 
df = pd.read_excel("/Users/thuytrangneee/Downloads/Historical Product Demand.xlsx")
warehouses = ["Whse_J"]   
df_subset = df[df["Warehouse"].isin(warehouses)]

products = df_subset["Product_Code"].unique()[:5]  
df_subset = df_subset[df_subset["Product_Code"].isin(products)]

df_subset = df_subset.reset_index(drop=True)

df_subset.to_excel("datasetprj.xlsx", index=False)
downloads = "/Users/thuytrangneee/Downloads"
file_path = os.path.join(downloads, "datasetprj.xlsx")
df_subset.to_excel(file_path, index=False)
file_path 
