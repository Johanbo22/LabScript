import pandas as pd

sheet_name = "CNP_konc"  
sheet_id = "1h7mYkvkY5C6MjakeSv8ZGoMcU_yI_tIsN869vdWr75k"  
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

df = pd.read_csv(url, decimal=",")

# Læser data for sikre tjeksum
print(df.head())

# funktion 
def calculate_kg_to_ha(stof, koncentration, jordmængde, vandindhold, bulk_density, dybde):
    stof = stof.upper()
    # Konverterer jordmængden til kg
    jord_kg = jordmængde / 1000
    
    # Vandets vægt ud fra vandindholdet
    vand_vægt = jord_kg * (vandindhold / 100)
    
    # Korrigerer jordens vægt for vand
    corr_jord = jord_kg - vand_vægt
    
    # Volumenvægt konverteres til kg/m³
    bulk_kg = bulk_density * 1000
    
    # Tykkelsen af jordlag i meter
    dybde_m = dybde / 100
    
    # 1 hektar i m²
    ha = 10000
    
    # Volumen af jordlaget ud fra 1 hektar og tykkelsen af jordlaget
    jord_tyk_vol = ha * dybde_m
    
    # mængden af jord i tykkelsen 
    jord_tyk = jord_tyk_vol * bulk_kg
    
    if stof != "P": # ud regner hvis stoffet er c eller n
        # Konverterer koncentrationen fra mg/L til mg/mL
        koncentration_mg_ml = koncentration / 1000
        
        # væsken volumen i mL
        væske = 250
        
        # Mængden af stoffet i mg
        stof_i_væske = koncentration_mg_ml * væske
        
        # Konverter til gram
        stof_g = stof_i_væske / 1000
        
        # Mængden af stoffet i gram per kg jord
        stof_jord = stof_g / corr_jord
    else: # udregner hvis stoffet er P
        cuvette_væske = 2.84*10**-3
        koncentration_cuvette = koncentration * cuvette_væske
        pipette_væske = 0.04 * 10**-3
        koncentration_pipette = koncentration_cuvette / pipette_væske
        beholder_væske = 0.025
        koncentration_prv_mg = koncentration_pipette * beholder_væske
        koncentration_prv_g = koncentration_prv_mg / 1000
        stof_jord = koncentration_prv_g / corr_jord
    
    # Mængden i g/ha
    g_ha = jord_tyk * stof_jord
    # Mængden i kg/ha
    kg_ha = g_ha / 1000
    
    return f"Resultatet er {kg_ha:.4f} kg {stof}/ha"

# udfører funktionen på alle rækker i datasættet
df['Result'] = df.apply(lambda row: calculate_kg_to_ha(row['stof'], row['koncentration'], row['jord_vægt'], row['vandindhold'], row['bulk_density'], row['tykkelse']), axis=1)

# udskriver resultatet
print(df[['prøveid', 'Result']])
