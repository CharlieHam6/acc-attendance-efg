import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf   # import can live at the top with the others
import os

# Cup semifinals, T-Mobile Arena, Las Vegas — verified vs NYK box score
NEUTRAL_SITE = {
    ("thunder", 2026): ["2025-12-13"],
    ("magic", 2026): ["2025-12-13"],   # ← the date you find in step 2
}

def load_team_season(team, season):
    # Stage 1: Load
    sched = pd.read_csv(f"data/{team}_{season}_schedule.csv")
    log = pd.read_csv(f"data/{team}_{season}_gamelog.csv")

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
    assert len(df) == len(log), f"{team}: merge changed rows {len(log)} -> {len(df)}"

    # Stage 4: filter to home games, compute eFG
    # road-designated Cup games arrive marked "@" and are excluded by the filter; home-designated ones arrive blank and are dropped via NEUTRAL_SITE.
    home = df[df["loc"].isna()].copy()
    home["efg"] = (home["FG"] + 0.5 * home["3P"]) / home["FGA"]
    
    for d in NEUTRAL_SITE.get((team, season), []):
        home = home[home["Date"] != pd.Timestamp(d)]
    
    # stamp and return
    home["team"] = team
    home["season"] = season
    return home


# --- main script ---
teams = ["lakers", "celtics", "knicks", "pistons", "wizards", "raptors", "philly", "nets", "thunder", "nuggets", "timberwolves", "trailblazers", "jazz", "bucks", "bulls", "cavaliers", "pacers", "suns", "warriors", "kings","clippers", "hawks","hornets", "magic", "heat", "spurs", "rockets", "pelicans", "mavericks", "grizzlies"] 

for team in teams:
    for kind in ["schedule", "gamelog"]:
        path = f"data/{team}_2026_{kind}.csv"
        assert os.path.exists(path), f"missing: {path}"
frames = []
for team in teams:
    print("loading", team)
    frames.append(load_team_season(team, 2026))

all_games = pd.concat(frames, ignore_index=True)
print(all_games.groupby("team").size())
print(sorted(all_games["Opp"].unique()))



print(len(all_games))
print(all_games.groupby("team")["Attend."].mean().sort_values().round(0))

#load SRS and name change
NAME_TO_CODE = {
    "Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BRK",
    "Charlotte Hornets": "CHO", "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN", "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW", "Houston Rockets": "HOU", "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA", "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP", "New York Knicks": "NYK", "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHO",
    "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR", "Utah Jazz": "UTA", "Washington Wizards": "WAS",
}

srs = pd.read_csv("data/srs_2026.csv")
srs["Team"] = srs["Team"].str.replace("*", "", regex=False).str.strip()
srs["Opp"] = srs["Team"].map(NAME_TO_CODE)
srs = srs[["Opp", "SRS"]]


#merge and interrogate
before = len(all_games)
all_games = all_games.merge(srs, on="Opp", how="left")
assert len(all_games) == before, "SRS merge changed row count"
assert all_games["SRS"].notna().all(), f"missing SRS for: {sorted(all_games[all_games['SRS'].isna()]['Opp'].unique())}"


#PLEASE
print(all_games[["Date", "team", "Opp", "Attend.", "efg", "SRS"]].head(10))
print(all_games["SRS"].describe())

all_games = all_games.rename(columns={"Attend.": "attendance"})
all_games["attend_k"] = all_games["attendance"] / 1000


naive = smf.ols("efg ~ attend_k", data=all_games).fit()
controlled = smf.ols("efg ~ attend_k + SRS", data=all_games).fit()

print("--- naive ---")
print(naive.params)
print(naive.pvalues)
print("--- controlled ---")
print(controlled.params)
print(controlled.pvalues)

#Da Scatter Plot script
plt.scatter(all_games["attendance"], all_games["efg"], s=8, alpha=0.4)
plt.xlabel("Attendance")
plt.ylabel("eFG%")
plt.title(f"Home attendance vs eFG%, {all_games['team'].nunique()} teams, 2025-26")
plt.savefig("league_scatter.png")