# Opdateret matrix som viser en talværdi for korrelationen inde i selve matrixen.

# Importering af biblioteker
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import seaborn as sns
import statsmodels.api as sm

# Import af data fra Excel filen. For Johan: ændre brugeren til og fra joha4 til Johan og omvendt (PC og Laptop). 
#data = pd.read_excel(r'C:\Users\Johan\OneDrive\Skrivebord_LapTop\Resultater_Lab.xlsx', decimal=",")

# Dette er stien på google sheets dokumentet
sheet_name = "Resultater_Lab"
sheet_id = "1h7mYkvkY5C6MjakeSv8ZGoMcU_yI_tIsN869vdWr75k" # unik Google Sheets ID
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

data = pd.read_csv(url, decimal=",")

# Opgraderet Korrelationsmatrix:
# Udvælg kun numeriske kolonner for korrelationsberegning
numerical_data = data.select_dtypes(include=[np.number])

# Udregn korrelationsmatrixen
correlation_matrix = numerical_data.corr()

# Visualisering af korrelationsmatrix med korrekt placerede etiketter
plt.figure(figsize=(20, 18))  # Figurstørrelse
plt.title("Korrelationsmatrix mellem parametre", fontsize=24)  

# Heatmap med korrekte korrelationsværdier og etiketter
sns.heatmap(
    correlation_matrix,
    annot=True,                # Viser korrelationsværdier i cellerne
    fmt=".1f",                 # Én decimal for at gøre det mere kompakt
    cmap="coolwarm",           # Farveskala
    cbar_kws={"label": "Korrelationskoefficient"},  # Label til farveskalabar
    square=True,               # Kvadratiske celler
    annot_kws={"size": 12},    # Tekststørrelse for annoteringer
    xticklabels=correlation_matrix.columns,  # Cellerne matcher kolonnenavne
    yticklabels=correlation_matrix.columns
)

# Justerer placeringen af etiketterne
plt.xticks(
    rotation=45,              # Roterer etiketterne for at give plads
    fontsize=12,              # Justerer skriftstørrelsen
    ha='right'                # Justerer placeringen til højre for mere præcision
)
plt.yticks(
    fontsize=12,              # Justerer skriftstørrelsen
    rotation=0,               # Holder etiketterne lodrette
    va='center'               # Centrer lodret justering
)

# Tilpasser layout for at sikre, at alle etiketter og heatmap vises korrekt
plt.tight_layout()

# Vis plottet
plt.show()



# Plot af udvalgt korrelation: 
# Funktion til scatterplots med regressionslinje og ligning/r^2
def scatter_with_regression(data, x_col, y_col, title=None):
    plt.figure(figsize=(10, 6))
    
    # Fjern manglende værdier for både x og y
    clean_data = data[[x_col, y_col]].dropna()
    x = clean_data[x_col]
    y = clean_data[y_col]
    x = sm.add_constant(x)  # Tilføj konstant for intercept
    
    # Udfør lineær regression
    model = sm.OLS(y, x).fit()
    slope = model.params.iloc[1]
    intercept = model.params.iloc[0]
    r_squared = model.rsquared
    

    
    # Tegn scatterplot og regression
    sns.regplot(
        x=x_col,
        y=y_col,
        data=clean_data,
        scatter_kws={"alpha": 0.6},
        line_kws={"color": "red", "lw": 2}
    )
    
    # Vis ligning og r^2 på plottet
    equation = f"$y = {slope:.2f}x + {intercept:.2f}$\n$R^2 = {r_squared:.2f}$"
    plt.text(0.05, 0.95, equation, fontsize=12, transform=plt.gca().transAxes,
             verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
    
    # Titel og akseformattering
    plt.title(title if title else f"{x_col} vs {y_col}", fontsize=20, pad=20, fontweight="bold")
    plt.xlabel(x_col, fontsize=12, fontweight="bold")
    plt.ylabel(y_col, fontsize=12, fontweight="bold")
    plt.gca().set_facecolor("#F0F0F0")
    plt.gca().tick_params(direction="in", which="both")

    plt.grid(axis="both", linestyle="--", alpha=0.1, color="000000")
    for spine in plt.gca().spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.9)
        spine.set_edgecolor("black")
    plt.show()

# Laver liste over relevante udvalgte korrelationspar 
relevant_pairs = [
    ("Porøsitet (%)", "Volumenvægt (g/cm³)"),  # Stærk negativ korrelation
    ("Indhold af organisk kulstof (%)", "Porøsitet (%)"),  # Positiv korrelation
    ("Reaktionstal", "pH CaCl2"),  # Stærk positiv korrelation
    ("pH H2O", "Gravimetrisk vandindhold (%)")  # Negativ korrelation
]

# Generer scatterplots for de valgte par
for x_col, y_col in relevant_pairs:
    scatter_with_regression(
        data=data,
        x_col=x_col,
        y_col=y_col,
        title=f"{x_col} vs {y_col}"
    )

