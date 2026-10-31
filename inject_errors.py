import numpy as np
import pandas as pd

rng = np.random.default_rng(7)

df = pd.read_csv("production_clean.csv")
df["rate_unit"] = "bbl/d"          # new column: everything starts in barrels/day
log = []                            # answer key: one entry per injected error

def record(rows, error_type):
    for _, r in rows.iterrows():
        log.append({"well_id": r["well_id"], "date": r["date"], "error_type": error_type})

# 1. Unit mix-up: all of W-017 reported in m3/d instead of barrels/d
mask = df["well_id"] == "W-017"
df.loc[mask, "oil_rate_bopd"] = (df.loc[mask, "oil_rate_bopd"] * 0.158987).round(1)
df.loc[mask, "rate_unit"] = "m3/d"
record(df[mask], "unit_mismatch")

# 2. Pick 45 different rows (not from W-017) and split them between the error types
eligible = df.index[~mask]
picks = rng.choice(eligible, size=45, replace=False)
neg_idx, sent_idx, dup_idx, gap_idx = picks[:5], picks[5:15], picks[15:25], picks[25:]

# 3. Negative rates
df.loc[neg_idx, "oil_rate_bopd"] = -df.loc[neg_idx, "oil_rate_bopd"]
record(df.loc[neg_idx], "negative_rate")

# 4. Sentinel values
df.loc[sent_idx, "oil_rate_bopd"] = -999
record(df.loc[sent_idx], "sentinel_-999")

# 5. Duplicate rows
record(df.loc[dup_idx], "duplicate")
df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)

# 6. Missing rows (gaps), done last
record(df.loc[gap_idx], "missing_row")
df = df.drop(gap_idx)

df.to_csv("production.csv", index=False)
pd.DataFrame(log).to_csv("injected_errors.csv", index=False)

print(df.shape)
print(pd.DataFrame(log)["error_type"].value_counts())