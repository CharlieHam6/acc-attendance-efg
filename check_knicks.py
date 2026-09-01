import pandas as pd

log = pd.read_csv("data/thunder_2026_gamelog.csv")
sched = pd.read_csv("data/thunder_2026_schedule.csv")
sched = sched.rename(columns={"Unnamed: 5": "loc"})
sched = sched[sched["Date"] != "Date"]
sched["Date"] = pd.to_datetime(sched["Date"])

# same cleaning as the pipeline
log = log.rename(columns={"Unnamed: 3": "loc"})
log = log[log["Date"] != "Date"]
log["Date"] = pd.to_datetime(log["Date"])

print("rows before dropna:", len(log))
log = log.dropna(subset=["Date"])
print("rows after dropna:", len(log))

# every game that is NOT a road game
not_away = log[log["loc"] != "@"]
print("non-away games:", len(not_away))
print(not_away[["Date", "loc", "Opp"]].to_string())


dec = log[(log["loc"] == "@") & (log["Date"].between("2025-12-08", "2025-12-18"))]
print(dec[["Date", "loc", "Opp"]])

print("sched rows:", len(sched), " log rows:", len(log))
print("sched dates:", sched["Date"].min(), "to", sched["Date"].max())
print("log dates:  ", log["Date"].min(), "to", log["Date"].max())
print(log[log["Date"].duplicated(keep=False)][["Date", "Opp"]])