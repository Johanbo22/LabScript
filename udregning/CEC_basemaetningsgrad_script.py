import pandas as pd
from tabulate import tabulate

sheet_name = "CEC_basemaet"
sheet_id = "1h7mYkvkY5C6MjakeSv8ZGoMcU_yI_tIsN869vdWr75k"  
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

df = pd.read_csv(url, decimal=",")

print(df.head())

df["base_kationer"] = df[['ca', 'mg', 'k', 'na', 'mn']].sum(axis=1)
df["sure_kationer"] = df[['h', 'al']].sum(axis=1)

# udregner Cation Exchange Capacity (CEC)
df['CEC (cmol(+)/kg)'] = df["base_kationer"] + df['sure_kationer']

# udregner basemætningsgraden 
df["Basemætningsgrad (%)"] = (df['base_kationer'] / df['CEC (cmol(+)/kg)']) * 100

print("\n")
print(tabulate(df[["ID", "CEC (cmol(+)/kg)", "Basemætningsgrad (%)"]], headers=["ID", "CEC (cmol(+)/kg)", "Basemætningsgrad (%)"], tablefmt="fancy_grid"))