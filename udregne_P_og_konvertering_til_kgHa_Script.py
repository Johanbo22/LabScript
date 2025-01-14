import numpy as np
import matplotlib.pyplot as plt 
from tabulate import tabulate
from openpyxl import Workbook

# sætter en con for omkring P skal implementeres
udregne_P = input("Skal der udrgnes fosfor koncentrationer? (ja/nej): ").strip().upper()
if udregne_P == "JA":
    abs_standard = [] # tom liste til input
    standard_rows = ['Blank', 1, 2, 3, 4, 5] # standardrækken
    for row in standard_rows:
        abs_value = float(input(f"Absorbans for standardopløsning {row}: ")) # indtast absorbans
        abs_standard.append(abs_value) # tilføjer de indtastet værdier til den tomme liste
        
    sample_ids = [] # tom liste til input
    abs_prøve = [] # tom list til input
    while True:
        sample_id = input("Indtast PrøveID ('done' når færdig): ") 
        if sample_id.lower() == "done": 
            break # så while-loopet kan afslutte
        sample_type = input(f"Indtast typen af prøven for PrøveID {sample_id} ('uorg' / 'tot'): ")
        abs_value = float(input(f"Indtast absorbans for PrøveID {sample_id}: "))
        sample_ids.append((sample_id, sample_type))
        abs_prøve.append(abs_value)
        
    def p_analyse(abs_standard, standard_rows, sample_ids, abs_prøve):
        p_koncentration = 2 # koncentrationen af P i mg/L i P-standarden
        p_koncentration_mg_ml = p_koncentration / 1000 # konvertering til mg/ml
        
        total_væske = 2.84 # den totale væske i cuvetten
        p_standard_væske = np.array([0.0, 0.1, 0.3, 0.5, 0.7, 0.9]) # mænngden af p_standard i standardrækkerne

        # den samlede mængde p i hver standardrække
        p_mængde_ml_standard = (p_standard_væske * p_koncentration_mg_ml) / total_væske

        # numpy arrays til at kunne arbejde med lister figurativt og matematisk
        x = np.array(p_mængde_ml_standard)
        y = np.array(abs_standard)
        coefficients = np.polyfit(x, y, 1)
        slope, intercept = coefficients

        # regressionsplotttet for figuren. 
        plt.scatter(x, y, label="Standardrække", color="blue")
        plt.plot(x, slope * x + intercept, label=f"y = {slope:.4f}x + {intercept:.4f}", color="red")
        plt.xlabel("Koncentration af P (mg/mL)")
        plt.xlim(0, max(x)*1.1)
        plt.ylabel("AbsStandard")
        plt.ylim(0, max(y)*1.1)
        plt.title("Standardkurve")
        plt.legend()
        plt.show()

        # ligningen for plottet
        print(f"Lineær regression: y = {slope:.4f}x + {intercept:.4f}")

        # egne prøver absorbans
        abs_prøve = np.array(abs_prøve)
        p_koncentration_prøver = ((abs_prøve - intercept) / slope) * 1000 # koncentrationen af p udfra standardrækken. 
        
        print("\nData")
        print("PrøveID\t\tAbsPrøve\t\tKoncentration (mg/L)")
        for i, p in enumerate(p_koncentration_prøver):
            print(f"{sample_ids[i]}\t\t{abs_prøve[i]}\t\t{p:.3f}")

        # giver hver type af p
        uorganisk_p = [koncentration for (sample, type), koncentration in zip(sample_ids, p_koncentration_prøver) if type == "uorg"]
        total_p = [koncentration for (sample, type), koncentration in zip(sample_ids, p_koncentration_prøver) if type == "tot"]

        # konvertering til en numpy array
        uorganisk_p = np.array(uorganisk_p)
        total_p = np.array(total_p)

        # mængden af organisk p
        organisk_p = total_p - uorganisk_p 
        
        koncentrations_af_p = {
            "uorganisk_p": uorganisk_p.tolist(),
            "organisk_p": organisk_p.tolist()
        }
        
        return koncentrations_af_p

    # printes i en tabel
    koncentrations_af_p = p_analyse(abs_standard, standard_rows, sample_ids, abs_prøve)
    table_data = []
    for key, values in koncentrations_af_p.items():
        for val in values:
            table_data.append([key,val])
    headers = ["Type Fosfor", "Koncentration (mg/L)"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    # sender data til excel-fil i CD
    create_excel_from_table = False
    if create_excel_from_table:
        file_name = "fosfor_koncentration.xlsx"
        wb = Workbook()
        ws = wb.active
        ws.title = "Fosfor Koncentrationer"
        ws.append(headers)
        for row in table_data:
            ws.append(row)
        wb.save(file_name)


# En funktion der udregner stof mængden i kg/ha ud fra en givet stof, koncentration (mg/L), jordmængden (g), vandindhold (%), volumenvægt (g/cm^3) og dybde (cm)
def calculate_kg_to_ha(stof, koncentration, jordmængde, vandindhold, bulk_density, dybde):
    # Fælles variabler
    # jordmængden omregnes fra g til kg
    jord_kg = jordmængde / 1000
    
    # Vægten af vandet i jordmængden
    vand_vægt = jord_kg * (vandindhold / 100)
    
    # Korrektion af jordmængden for vandvægten
    corr_jord = jord_kg - vand_vægt
    
    # Volumenvægten i kg/m³
    bulk_kg = bulk_density * 1000
    
    # Tykkelsen af jordlaget i meter
    dybde_m = dybde / 100
    
    # Hektar i m²
    ha = 10000
    
    # Volumen af tykkelsen givet ud fra hektar
    jord_tyk_vol = ha * dybde_m
    
    # Mængden af jord i dybde intervallet (tykkelsen)
    jord_tyk = jord_tyk_vol * bulk_kg
    
    if stof != "P": # Udregner hvis stoffet er C eller N
        # Koncentrationen omregnes fra mg/L til mg/mL
        koncentration_mg_ml = koncentration / 1000
        
        # Væsken i mL
        væske = 250
        
        # Mængden af stoffet i væsken i mg
        stof_i_væske = koncentration_mg_ml * væske
        
        # Konverter til gram
        stof_g = stof_i_væske / 1000
        
        # Koncentration af stoffet i jorden i g/kgjord 
        stof_jord = stof_g / corr_jord
    else: # Udregner hvis stoffet er P
        # Koncentrationen af cuvette 
        cuvette_væske = 2.84*10**-3
        # Koncentrationen af P i cuvetten
        koncentration_cuvette = koncentration * cuvette_væske
        
        # Koncentrationen i pipetten
        pipette_væske = 0.04 * 10**-3
        # Koncentrationen af P i pipetten.
        koncentration_pipette = koncentration_cuvette / pipette_væske
        
        # Koncentrationen i prøve beholderen
        beholder_væske = 0.025
        koncentration_prv_mg = koncentration_pipette * beholder_væske
        
        # Koncentrationen i prøve i gram
        koncentration_prv_g = koncentration_prv_mg / 1000
        
        # Koncentration af stoffet i jorden i g/kgjord
        stof_jord = koncentration_prv_g / corr_jord
    
    # Total mængde i g/ha
    g_ha = jord_tyk * stof_jord
    # Total mængde i kg/ha
    kg_ha = g_ha / 1000
    
    if stof == "P":
        return f"Resultatet er {kg_ha:.4f} kg {stof}/ha"
    else:
        return f"Resultatet er {kg_ha:.4f} kg {stof}/ha"
    
# Bruger input.
try:
    stof = input("Indtast stof (C, N eller P): ").strip().upper()
    if stof not in ["C", "N", "P"]:
        raise ValueError("Input stoffet skal være enten 'C', 'N' eller 'P'")
    koncentration = float(input("Indtast koncentration (mg/mL): "))
    jordmængde = float(input("Indtast jordmængde (g): "))
    vandindhold = float(input("Indtast vandindhold (%): "))
    bulk_density = float(input("Indtast bulk density (g/cm³): "))
    dybde = float(input("Indtast dybde (cm): "))
    
    result = calculate_kg_to_ha(stof, koncentration, jordmængde, vandindhold, bulk_density, dybde)
    print(result)
except ValueError as e:
    print(f"Fejl: {e}")
    
