import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

days = 60
n_wells = 30
dates = pd.date_range(start="2026-01-01", periods=days)
day_number = np.arange(days)

frames = []

for i in range(1, n_wells + 1):          
    well_id = f"W-{i:03d}"               
    start_rate = rng.uniform(500, 3000)  
    decline = rng.uniform(0.001, 0.006)  

    oil_rate = start_rate * np.exp(-decline * day_number) + rng.normal(0, 15, size=days)
    water_cut = np.linspace(rng.uniform(5, 20), rng.uniform(25, 50), days)
    whp = np.linspace(rng.uniform(800, 1000), rng.uniform(600, 780), days)

    well_df = pd.DataFrame({
        "date": dates,
        "well_id": well_id,
        "oil_rate_bopd": oil_rate.round(1),
        "water_cut_pct": water_cut.round(1),
        "whp_psi": whp.round(1),
    })
    frames.append(well_df)               

df = pd.concat(frames, ignore_index=True) 
df.to_csv("production_clean.csv", index=False)

print(df.shape)
print(df.head())