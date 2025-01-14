import pandas as pd

# Google Sheets URL (Replace with your actual sheet ID and sheet name)
sheet_name = "CNP_konc"  # Ensure this is the correct sheet name
sheet_id = "1h7mYkvkY5C6MjakeSv8ZGoMcU_yI_tIsN869vdWr75k"  # Replace with your sheet ID
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# Read the data from the Google Sheet
df = pd.read_csv(url, decimal=",")

# Ensure the columns match the data format you provided
# If necessary, you may need to adjust the column names to match exactly with your sheet
# For example, if column names are in Danish or have extra spaces, clean them

# Checking the first few rows of the imported data to ensure it's correct
print(df.head())

# Function definition (as you provided it)
def calculate_kg_to_ha(stof, koncentration, jordmængde, vandindhold, bulk_density, dybde):
    stof = stof.upper()
    # Convert jordmængde from grams to kg
    jord_kg = jordmængde / 1000
    
    # Calculate the weight of water in the soil
    vand_vægt = jord_kg * (vandindhold / 100)
    
    # Adjust the soil weight for the water content
    corr_jord = jord_kg - vand_vægt
    
    # Bulk density in kg/m³
    bulk_kg = bulk_density * 1000
    
    # Thickness of the soil layer in meters
    dybde_m = dybde / 100
    
    # Area of one hectare in m²
    ha = 10000
    
    # Volume of the soil layer for one hectare
    jord_tyk_vol = ha * dybde_m
    
    # Amount of soil in the depth interval (layer thickness)
    jord_tyk = jord_tyk_vol * bulk_kg
    
    if stof != "P": # Calculate if the substance is C or N
        # Convert concentration from mg/L to mg/mL
        koncentration_mg_ml = koncentration / 1000
        
        # Volume of the liquid (in mL)
        væske = 250
        
        # Amount of substance in the liquid in mg
        stof_i_væske = koncentration_mg_ml * væske
        
        # Convert to grams
        stof_g = stof_i_væske / 1000
        
        # Concentration of the substance in soil in g/kg soil
        stof_jord = stof_g / corr_jord
    else: # Calculate if the substance is P
        cuvette_væske = 2.84*10**-3
        koncentration_cuvette = koncentration * cuvette_væske
        pipette_væske = 0.04 * 10**-3
        koncentration_pipette = koncentration_cuvette / pipette_væske
        beholder_væske = 0.025
        koncentration_prv_mg = koncentration_pipette * beholder_væske
        koncentration_prv_g = koncentration_prv_mg / 1000
        stof_jord = koncentration_prv_g / corr_jord
    
    # Total amount in g/ha
    g_ha = jord_tyk * stof_jord
    # Total amount in kg/ha
    kg_ha = g_ha / 1000
    
    return f"Resultatet er {kg_ha:.4f} kg {stof}/ha"

# Apply the function to each row of the DataFrame
df['Result'] = df.apply(lambda row: calculate_kg_to_ha(row['stof'], row['koncentration'], row['jord_vægt'], row['vandindhold'], row['bulk_density'], row['tykkelse']), axis=1)

# Print the results
print(df[['prøveid', 'Result']])
