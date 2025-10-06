import pandas as pd

df = pd.read_excel("datasetprj.xlsx")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df_2012 = df[df['Date'].dt.year == 2012]
df_2012.to_excel("datasetprj_2012.xlsx", index=False)
print(df.head(5))
