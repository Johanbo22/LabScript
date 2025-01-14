import pandas as pd
from tabulate import tabulate

# data fra sheets
sheet_name = "cmol"
sheet_id = "1h7mYkvkY5C6MjakeSv8ZGoMcU_yI_tIsN869vdWr75k"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# data
df = pd.read_csv(url, decimal=",")

# konstanter
fortyndingsfaktor = 10 # x
jordvægt = 2.5 # i gram
valens = {"Mg": 0.2, "K": 0.1, "Ca": 0.2, "Na": 0.1, "Mn": 0.2} # cmol/mmol
molvægt = {"Mg": 24.305, "K": 39.098, "Ca": 40.078, "Na": 22.99, "Mn": 54.938} # g/mol

# funktion der beregner cmol(+)/kg ud fra formel 7.7 
def udregne_cmol(A, ion):
    if A < 0: # ignorer negative værdier
        return 0
    C = valens[ion]
    D = molvægt[ion]
    return (A * fortyndingsfaktor * 100 * C * 1000 * 1000) / (jordvægt * D * 1000 * 1000)

for ion in ["Mg", "K", "Ca", "Na", "Mn"]:
    if ion in df.columns: 
        df[f"{ion} cmol(+)/kg"] = df[ion].apply(lambda x: udregne_cmol(x, ion))

# sæt til True, hvis der ønskes data til en ny fil.
print_to_excel = False
if print_to_excel:
    df.to_excel('cmol_resultater.xlsx')

# resultater
print("Resultater:")
print(tabulate(df, headers='keys', tablefmt="fancy_grid"))

