import pandas as pd

# Stage 1: Load data
sched = pd.read_csv("data/lakers_2026_schedule.csv")
log = pd.read_csv("data/lakers_2026_gamelog.csv")

# Stage 2: Clean
sched = sched.rename(columns={"Unnamed: 5": "loc"})
log = log.rename(columns={"Unnamed: 3": "loc"})

sched = sched[sched["Date"] != "Date"]
log = log[log["Date"] != "Date"]

sched["Date"] = pd.to_datetime(sched["Date"])
log["Date"] = pd.to_datetime(log["Date"])

log = log.dropna(subset=["Date"])

# Stage 3: Merge attendance onto game log
df = log.merge(sched[["Date", "Attend."]], on="Date", how="inner")
assert len(df) == len(log), "merge changed row count"


# Stage 4: filter and compute
home = df[df["loc"].isna()].copy()


home["efg"] = (home["FG"] + 0.5 * home["3P"]) / home["FGA"]


# Stage 5: scatter 
import matplotlib.pyplot as plt

plt.scatter(home["Attend."], home["efg"])
plt.xlabel("Attendance")
plt.ylabel("eFG%")
plt.title("Lakers 2025-26: home attendance vs eFG%")
plt.savefig("lakers_pilot.png")

plt.show()