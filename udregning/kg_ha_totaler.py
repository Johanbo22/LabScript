from unicodedata import numeric # ????
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

sheet_name = "kg_ha_totals"
sheet_id = "1h7mYkvkY5C6MjakeSv8ZGoMcU_yI_tIsN869vdWr75k" # unik Google Sheets ID
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

data = pd.read_csv(url, decimal=",")
print(data.head())
df = pd.DataFrame(data)

# grupperer og summerer ud fra lokalitet. 
grouped_summeret = df.groupby("Lokalitet").sum(numeric_only=True).reset_index()
grouped_summeret_gns = df.groupby("Lokalitet").mean(numeric_only=True).reset_index()
print("\n")
print("Resultater: Summeret for hver lokalitet")
print(tabulate(grouped_summeret, headers="keys", tablefmt="fancy_grid"))
print("\n")
print("Resultater: Summeret for hver lokalitet og gennemsnit for hver")
print(tabulate(grouped_summeret_gns, headers="keys", tablefmt="fancy_grid"))


# grupperer og summerer ud fra arealanvendelse
df["Lokalitet"] = df["Lokalitet"].replace({"Brakmark (Bund)": "Brakmark", "Dyrket mark (Bund)": "Dyrket mark", "Dyrket mark (Top)": "Dyrket Mark"})
df["Lokalitet"] =df["Lokalitet"].str.strip().str.title()

grouped_summeret2 = df.groupby("Lokalitet", as_index=False).sum(numeric_only=True)
grup_sum_mean2 = df.groupby("Lokalitet", as_index=False).mean(numeric_only=True)
print("\n")
print("Resultater: Grupperet og summeret ud fra arealanvendelsen")
print(tabulate(grouped_summeret2, headers="keys", tablefmt="fancy_grid"))
print("\n")
print("Resultater: Grupperet, summeret og gennemsnittet af areal anvendelsen")
print(tabulate(grup_sum_mean2, headers="keys", tablefmt="fancy_grid"))

# laver et excel ark baseret på dette data. 
excel = True
if excel:
    with pd.ExcelWriter("summeret_kg_ha.xlsx") as writer:
        grouped_summeret.to_excel(writer, sheet_name="Summeret_Lokalitet", index=False)
        grouped_summeret_gns.to_excel(writer, sheet_name="Summeret_Lokalitet_gns", index=False)
        grouped_summeret2.to_excel(writer, sheet_name="Summeret_Arealanvendelse", index=False)
        grup_sum_mean2.to_excel(writer, sheet_name="Summeret_Arealanv_gns", index=False)




# et søjlediagram. ikke er særligt brugbar. 
def søjlediagram(data):
    numeric_columns = data.select_dtypes(include="number").columns
    lokaliter = data["Lokalitet"].unique()

    x_positions = range(len(lokaliter))

    for column in numeric_columns:
        plt.figure(figsize=(12, 6))

        for i, lokalitet in enumerate(lokaliter):
            subset = data[data["Lokalitet"] == lokalitet]
            plt.bar(x_positions[i], subset[column].sum(), width=0.9, label=lokalitet)
    
        plt.ylabel(f"{column} \n kg/ha")
        plt.xlabel("Lokalitet")
        plt.xticks([])
        plt.gca().get_xaxis().set_visible(False)
        plt.legend(title="Lokalitet")
        plt.tight_layout()
        plt.show()


#søjlediagram(grouped_summeret)
