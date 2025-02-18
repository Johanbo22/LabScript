from typing import MutableMapping
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress
from matplotlib.ticker import MultipleLocator


# Data

data_co2 = pd.DataFrame({
    "Tid (sek)": [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300],
    "0-5cm": [72.77, 75.94, 79.53, 82.83, 86.14, 89.17, 92.21, 95.24, 97.86, 101.03, 103.92]
})

# Funktion

def plot_linear_regression(data, x_columns, y_columns, title, xlabel, ylabel):
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams["font.serif"] = "Times New Roman"
    plt.figure(figsize=(8, 4), facecolor="#FFFFFF")

    for column in y_columns:
        x = data[x_columns]
        y = data[column]

        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        line = slope * x + intercept
        r_squared = r_value**2

        plt.scatter(x, y, color="grey")
        plt.plot(x, line, color="black", label=f"y = {slope:.4f}x + {intercept:.2f}\n" f"R² = {r_squared:.4f}")


    #plt.title(title, fontsize=12, pad=5, fontweight="bold") # formattering
    
    plt.xlabel(xlabel, fontsize=10)
    plt.xticks(np.arange(0, 301, 50)) # formattering
    ax = plt.gca()
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    plt.ylabel(ylabel, fontsize=10)
    plt.gca().set_facecolor("white") # farven af akse-displayet
    plt.gca().tick_params(direction="out", which="both")
    plt.subplots_adjust(right=0.75)
    legend = plt.legend(
        #bbox_to_anchor=(0.5, -0.1)
        loc="best",
        fontsize=12,
        title_fontsize=8,
        frameon=False,
        facecolor="white",
        edgecolor="black",
        shadow=False,
        fancybox=False,
        borderpad=1,
        labelspacing=1.0,
        handlelength=2,
        handleheight=1,
        ncol=1 # antal kolonner til legend
    )
    #plt.grid(axis="both", linestyle="--", alpha=0.1, color="#000000")

    for spine in plt.gca().spines.values(): # formattering af kanten på akserne
        spine.set_visible(True)
        spine.set_linewidth(0.5)
        spine.set_edgecolor("black")

    plt.tight_layout(rect=[0, 0, 0.75, 1]) # formattering
    plt.show() 
                 
plot_linear_regression(data_co2, "Tid (sek)", ["0-5cm"], "CO₂ produktion for dybden 0-5cm", "Sekunder", "CO₂ (µg CO₂-C g⁻¹ t⁻¹)")
