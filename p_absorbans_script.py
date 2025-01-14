import numpy as np
import matplotlib.pyplot as plt 
from tabulate import tabulate
import pandas as pd

# Sheet og sheet-id fra Google sheet
sheet_name = "p_absorbans"
sheet_id = "1h7mYkvkY5C6MjakeSv8ZGoMcU_yI_tIsN869vdWr75k"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# læs data  
data = pd.read_csv(url, decimal=",")
print("Importeret data")
print(data.head()) # udskriver data for tjek

# ekstrahering af data
abs_standard = data['abs_standard'].dropna().astype(float).tolist()
p_standard_væske = data['p_standard_væske'].dropna().astype(float).tolist()
sample_ids = data['sample_id'].dropna().tolist()
abs_samples = data["abs_prøve"].dropna().astype(float).tolist()
sample_types = data["sample_type"].dropna().tolist()

# Tjeksummering
print("\nEkstraheret data:")
print(f"Absorbans for standard: {abs_standard}")
print(f"Standard koncentration væske: {p_standard_væske}")
print(f"Pr\u00f8ve IDs: {sample_ids}")
print(f"Absorbans Pr\u00f8ver: {abs_samples}")
print(f"Pr\u00f8ve Type: {sample_types}")

# definering af P analyse funktion
def p_analyse(abs_standard, p_standard_væske, sample_ids, abs_samples, sample_types):
    # koncentrationen af P i standard_opløsningen og samlet væske volumen
    p_koncentration_mg_ml = 2 / 1000 # 2 mg/L omregnet til mg/ml
    total_væske = 2.84 # total væskevolumen i mL
    
    # beregner mængden af p i hver standard opløsning
    p_mængde_ml_standard = (np.array(p_standard_væske) * p_koncentration_mg_ml) / total_væske
    
    # linear regression
    x = np.array(p_mængde_ml_standard)
    y = np.array(abs_standard)
    coefficients = np.polyfit(x, y, 1)
    slope, intercept = coefficients
    
    # plot af standardkurven
    plt.scatter(x, y, label="Standardrække", color="blue")
    plt.plot(x, slope * x + intercept, label=f"y = {slope:.4f}x + {intercept:.4f}", color="red")
    plt.xlabel("Koncentration af P (mg/mL)")
    plt.ylabel("Absorbans")
    plt.title("Standardkurve")
    plt.legend()
    plt.show()
    
    # beregner fosfor koncentrationer for prøverne baseret på standardrækken
    abs_samples = np.array(abs_samples)
    p_koncetrationer = ((abs_samples - intercept) / slope) * 1000
    
    print("\nResultater: ")
    results = [] # liste til at gemme resultaterne
    for i, p in enumerate(p_koncetrationer):
        results.append([sample_ids[i], sample_types[i], abs_samples[i], round(p, 3)])
        print(f"Pr\u00f8ve ID: {sample_ids[i]}, Type: {sample_types[i]}, Absorbans {abs_samples[i]}, Fosfor (mg/L): {p:.3f}")
    
    # filtrering af uorganisk og total p
    uorganisk_p = [p for (sample, stype), p in zip(zip(sample_ids, sample_types), p_koncetrationer) if stype == "uorg"]
    total_p = [p for (sample, stype), p in zip(zip(sample_ids, sample_types), p_koncetrationer) if stype == "tot"]
    
    # udgrening af organisk p
    organisk_p = np.array(total_p) - np.array(uorganisk_p)
    
    # tabel til resultaterne for u- og organisk p
    table_data = [["Uorganisk P", val] for val in uorganisk_p] + [["Organisk P", val] for val in organisk_p]
    print("\nTabel:")
    print(tabulate(table_data, headers=["Type", "P Koncetration (mg/L"], tablefmt="fancy_grid"))

# funktions kald    
p_analyse(abs_standard, p_standard_væske, sample_ids, abs_samples, sample_types)