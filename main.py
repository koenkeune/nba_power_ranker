from ranking import *
from visualizer import *

date = '2020-12-22'
# rankTeam('ATL', 2020, date)

wP = winPctLastSeason(2019)
# print(wP.items())
wPSorted = sorted(wP.items(), key=lambda x: x[1], reverse=True)
# print(wPSorted)

printRanking(wPSorted)

#standings = getStandings(2020, END_OF_SEASON_2020)
