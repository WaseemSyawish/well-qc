import pandas as pd

df = pd.read_csv("production.csv")
df["date"] = pd.to_datetime(df["date"])

issues = []

def flag(rows, issue):
    for _, r in rows.iterrows():
        issues.append({"well_id": r["well_id"],
                       "date": r["date"].strftime("%Y-%m-%d"),
                       "error_type": issue})

flag(df[df.duplicated(subset=["well_id", "date"], keep="first")], "duplicate")

flag(df[df["oil_rate_bopd"] == -999], "sentinel_-999")

flag(df[(df["oil_rate_bopd"] < 0) & (df["oil_rate_bopd"] != -999)], "negative_rate")

flag(df[df["rate_unit"] != "bbl/d"], "unit_mismatch")

all_dates = pd.date_range(df["date"].min(), df["date"].max())
for well_id, g in df.groupby("well_id"):
    for d in all_dates.difference(pd.DatetimeIndex(g["date"])):
        issues.append({"well_id": well_id,
                       "date": d.strftime("%Y-%m-%d"),
                       "error_type": "missing_row"})

found = pd.DataFrame(issues)
found.to_csv("qc_report.csv", index=False)

# compare against the answer key
key = pd.read_csv("injected_errors.csv")
check = key.merge(found, on=["well_id", "date", "error_type"], how="left", indicator=True)
print(check["_merge"].value_counts())