import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress


# Data

data_co2 = pd.DataFrame({
    "Tid (sek)": [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300],
    "0-5cm": [72.77, 75.94, 79.53, 82.83, 86.14, 89.17, 92.21, 95.24, 97.86, 101.03, 103.92]
})

# Funktion

def plot_linear_regression(data, x_columns, y_columns, title, xlabel, ylabel):
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams["font.serif"] = "Times New Roman"
    plt.figure(figsize=(10, 6), facecolor="#FFFFFF")

    for column in y_columns:
        x = data[x_columns]
        y = data[column]

        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        line = slope * x + intercept
        r_squared = r_value**2

        plt.scatter(x, y, color="darkorange")
        plt.plot(x, line, color="black", label=f"y = {slope:.4f}x + {intercept:.2f}\n" f"R² = {r_squared:.4f}")


    plt.title(title, fontsize=12, pad=5, fontweight="bold") # formattering
    
    plt.xlabel(xlabel, fontsize=8, fontweight="bold")
    plt.xticks(np.arange(0, 301, 50)) # formattering
    plt.ylabel(ylabel, fontsize=8, fontweight="bold")
    plt.gca().set_facecolor("#F0F0F0") # farven af akse-displayet
    plt.gca().tick_params(direction="in", which="both")
    plt.subplots_adjust(right=0.75)
    legend = plt.legend(
        bbox_to_anchor=(0.5, -0.1),
        loc="upper center",
        fontsize=7,
        title_fontsize=8,
        frameon=True,
        facecolor="#F0F0F0",
        edgecolor="black",
        shadow=True,
        fancybox=True,
        borderpad=1,
        labelspacing=1.5,
        handlelength=2,
        handleheight=1.5,
        ncol=1 # antal kolonner til legend
    )
    plt.grid(axis="both", linestyle="--", alpha=0.1, color="#000000")

    for spine in plt.gca().spines.values(): # formattering af kanten på akserne
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_edgecolor("black")

    plt.tight_layout(rect=[0, 0, 0.75, 1]) # formattering
    plt.show() 
                 
plot_linear_regression(data_co2, "Tid (sek)", ["0-5cm"], "CO₂ produktion for dybden 0-5cm", "Tid (sek)", "CO₂ (µg CO₂-C t⁻¹)")
