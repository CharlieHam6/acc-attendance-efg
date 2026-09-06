# NBA-attendance-efg
Controlling for opponent strength, does home attendance relate to shooting efficiency in the NBA?

Attendance at NBA games can sometimes feel like the make or break. How loud a crowd is, how much spirit they bring, what they chant, cheer and boo — all of that should matter, shouldn't it? I found no detectable relationship between home attendance and shooting efficiency. Even taken at face value, the estimated effect was tiny — on the order of half a point of eFG% between a quiet arena and a packed one, smaller than normal game-to-game noise. Opponent quality, however, had a strong negative relationship with home shooting efficiency — better opponents suppress it — which gave me confidence the method was capable of finding a real signal when one existed.

## Data
I used Basketball Reference data for all 30 NBA teams during the 2025-26 regular season. The final dataset contains 1,228 home games. I pulled:

- Team game logs for shooting data
- Team schedules for attendance
- Simple Rating System (SRS) ratings for opponent quality

The CSV files were exported by hand from Basketball Reference and saved in `data/`. I cleaned the files, standardized team and date fields, and merged the sources into one game-level dataset — game logs to schedules on date within each team, then SRS onto each game by opponent code. Two teams show 40 true home games rather than 41 because of neutral-site NBA Cup games (more on that below).

##Results

I estimated two linear regression models. The first looks only at attendance and home-team eFG%. The second adds opponent SRS as a control for opponent quality.
The attendance coefficient was both statistically insignificant and very small in practical terms. Teams shot differently against stronger opponents, and that relationship was statistically strong. I believe the attendance null is more credible because the same model was able to detect that much clearer basketball effect.
