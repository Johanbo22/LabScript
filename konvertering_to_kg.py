def calculate_kg_ha(koncentration, vandindhold, bulk, dybde):
    # Konvert koncentration til mg/mL
    koncentration_mg = koncentration / 1000

    # Definer væsken 
    væske = 250  # i mL

    # Udregne hvor meget C der er i væsken i mg
    c_i_væske = koncentration_mg * væske

    # Konverter til gram
    c_g = c_i_væske / 1000

    # Jordmængden og konverter til kg
    jord = 10  # i gram
    jord_kg = jord / 1000

    # Vandets vægt i kg
    vand_vægt = jord_kg * (vandindhold / 100)

    # Korrigeret jord for vand vægt
    corr_jord = jord_kg - vand_vægt

    # Koncentration af c i jorden i g/kgjord
    c_jord = c_g / corr_jord

    # Volumenvægt
    bulk_kg = bulk * 1000  # i kg/m³

    # Tykkelsen af dybden 
    dybde_m = dybde / 100  # i meter

    # Hektar og volumen af tykkelsen givet ud fra 1 ha.
    ha = 10000  # i m² 
    tyk_vol = ha * dybde_m  # i m³

    # mængden af jord i dybde intervallet (tykkelsen)
    jord_tyk = tyk_vol * bulk_kg  # i kg

    # Total koncentration i g/ha
    g_ha = jord_tyk * c_jord

    # Konverter g/ha til kg/ha
    kg_ha = g_ha / 1000

    return f"Restultat er {kg_ha:.2f}"


