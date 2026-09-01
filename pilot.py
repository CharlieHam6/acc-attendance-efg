import pandas as pd
import matplotlib.pyplot as plt

# Games designated "home" but played at a neutral site (NBA Cup, Las Vegas).
# bbref leaves loc blank for the home-designated team, so they'd count as home games.
NEUTRAL_SITE = {
    ("thunder", 2026): ["2025-12-13"],
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
    # neutral-site NBA Cup games excluded — marked "@" by bbref; some teams have 40 true home games
    home = df[df["loc"].isna()].copy()
    home["efg"] = (home["FG"] + 0.5 * home["3P"]) / home["FGA"]
    
    for d in NEUTRAL_SITE.get((team, season), []):
        home = home[home["Date"] != pd.Timestamp(d)]
    
    # stamp and return
    home["team"] = team
    home["season"] = season
    return home


# --- main script ---
teams = ["lakers", "celtics", "knicks", "pistons", "wizards", "raptors", "philly", "nets", "thunder", "nuggets", "timberwolves", "trailblazers", "jazz", "bucks", "bulls", "cavaliers", "pacers", "suns", "warriors", "kings","clippers", "hawks","hornets", "magic", "heat"] 
frames = []
for team in teams:
    print("loading", team)
    frames.append(load_team_season(team, 2026))

all_games = pd.concat(frames, ignore_index=True)
print(all_games.groupby("team").size())

plt.scatter(all_games["Attend."], all_games["efg"])
plt.xlabel("Attendance")
plt.ylabel("eFG%")
plt.title("Home attendance vs eFG%, 5 teams, 2025-26")
plt.savefig("five_team_scatter.png")