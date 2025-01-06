def calculate_kg_ha(koncentration, vandindhold, bulk, dybde):
    # Konvert koncentration til mg/mL
    koncentration_mg_mL = koncentration / 1000

    # Definer væsken 
    væske = 250  # i mL

    # Udregne hvor meget af stoffet der er i væsken i mg
    stof_i_væske = koncentration_mg * væske

    # Konverter til gram
    stof_g = stof_i_væske / 1000

    # Jordmængden og konverter til kg
    jord = 10  # i gram
    jord_kg = jord / 1000

    # Vandets vægt i kg
    vand_vægt = jord_kg * (vandindhold / 100)

    # Korrigeret jord for vand vægt
    corr_jord = jord_kg - vand_vægt

    # Koncentration af c i jorden i g/kgjord
    stof_jord = stof_g / corr_jord

    # Volumenvægt konverteres til kg/m^3
    bulk_kg = bulk * 1000  # i kg/m³

    # Tykkelsen af jordlagene. Denne tykkelse bliver konverteret til meter.
    dybde_m = dybde / 100  # i meter

    # Hektar og volumen af tykkelsen givet ud fra hektar.
    ha = 10000  # i m² 
    tyk_vol = ha * dybde_m  # i m³

    # mængden af jord i dybde intervallet (tykkelsen)
    jord_tyk = tyk_vol * bulk_kg  # i kg

    # Total mængde i g/ha
    g_ha = jord_tyk * stof_jord

    # Konverter g/ha til kg/ha
    kg_ha = g_ha / 1000

    return f"Restultat er {kg_ha:.2f}"


