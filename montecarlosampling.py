import pandas as pd
import numpy as np

# ---------------------------------------------------
# 1. Load dataset
# ---------------------------------------------------
file_path = r"C:\Users\Lenovo\Documents\UGRP2-Emission factors\Summary_Results.xlsx"

df = pd.read_excel(file_path)

# ---------------------------------------------------
# 2. Define gases (columns with EF values)
# ---------------------------------------------------
gases = [
    "CO___statALL",
    "CO2__statALL",
    "CH4__statALL",
    "Nox__statALL",
    "HCHO_statALL",
    "PM25_statALL",
    "BCFr_statALL"
]

fuel_col = "fuelName"

# ---------------------------------------------------
# 3. Monte Carlo settings
# ---------------------------------------------------
n_iter = 50000
results = []

# ---------------------------------------------------
# 4. Loop through fuels
# ---------------------------------------------------
fuels = df[fuel_col].unique()

for i in fuels:

    fuel_data = df[df[fuel_col] == i]

    # ---------------------------------------------------
    # 5. Loop through gases
    # ---------------------------------------------------
    for j in gases:

        value = fuel_data[j].values[0]

        if pd.isna(value):
            continue

        # ---------------------------------------------------
        # 6. Split "mean±std"
        # ---------------------------------------------------
        mean_str, std_str = str(value).split("±")

        mean_val = float(mean_str)
        std_val = float(std_str)

        # avoid zero std
        if std_val == 0:
            continue

        # ---------------------------------------------------
        # 7. Convert to lognormal parameters
        # ---------------------------------------------------
        sigma = np.sqrt(np.log(1 + (std_val**2 / mean_val**2)))
        mu = np.log(mean_val) - (sigma**2) / 2

        # ---------------------------------------------------
        # 8. Monte Carlo sampling
        # ---------------------------------------------------
        mc_samples = np.random.lognormal(mu, sigma, n_iter)

        mc_mean = np.mean(mc_samples)
        mc_std = np.std(mc_samples)

        results.append({
            "Fuel": i,
            "Gas": j,
            "Monte Carlo Mean EF": mc_mean,
            "Monte Carlo Std EF": mc_std
        })

# ---------------------------------------------------
# 9. Convert results to dataframe
# ---------------------------------------------------
results_df = pd.DataFrame(results)

print(results_df)

# Save output
results_df.to_excel("MC_EmissionFactors_SummaryResults.xlsx", index=False)