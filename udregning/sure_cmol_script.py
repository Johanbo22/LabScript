import pandas as pd 
import numpy as np
from tabulate import tabulate

sheet_name = "sure_cmol"
sheet_id = "1h7mYkvkY5C6MjakeSv8ZGoMcU_yI_tIsN869vdWr75k"  
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

df = pd.read_csv(url, decimal=",")

# tjeksummering
print("\nInput data")
print(df.head())

# udregning af sure kationer
def calculate(titration, naoh, jordvægt):
    return (titration * naoh / jordvægt) * 1000 # for at få det i cmol(+)/kg

results = []
for index, row in df.iterrows():
    result = calculate(row['titmængde'], row['naoh_konc'], row['jordvægt'])
    results.append(result)


results_df = pd.DataFrame({
    "ID": df['ID'],
    "cmol(+)/kg": results
})

# resultaterne af titrering
print("\nResultater")
print(results_df)

# Deler resultaterne op efter ID (A1, B1, C1) & (A2, B2, C2)
gruppe1 = results_df[results_df['ID'].str.endswith('1')].copy()
gruppe2 = results_df[results_df['ID'].str.endswith('2')].copy()

# Ekstraherer base-id (A, B, C)
gruppe1['Base_ID'] = gruppe1['ID'].str[:-1]
gruppe2['Base_ID'] = gruppe2['ID'].str[:-1]

# Samler de to grupper
samlet = pd.merge(gruppe2, gruppe1, on="Base_ID", suffixes=('_2', '_1'))

# udregner Al3+ ud fra kendte resultater af H+
samlet['Al3+ (cmol(+)/kg)'] = samlet['cmol(+)/kg_2'] - samlet['cmol(+)/kg_1']

# presentation af resultat
endelig_resultat = samlet[['Base_ID', 'ID_2', 'ID_1', 'cmol(+)/kg_2', "cmol(+)/kg_1", "Al3+ (cmol(+)/kg)"]]

# presentation af resultat
print("\n\t\t\t\tH+ og Al3+ samlet\tH+\t\tAl3+")
print(tabulate(endelig_resultat, headers="keys", tablefmt="rst"))
