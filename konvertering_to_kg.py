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
    dybde = int(input("Indtast dybde (cm): "))
    
    result = calculate_kg_to_ha(stof, koncentration, jordmængde, vandindhold, bulk_density, dybde)
    print(result)
except ValueError as e:
    print(f"Fejl: {e}")
    
