from ranking import *
from visualizer import *

date = '2021-02-15'
r = rankTeams(2020, date)

rSorted = sorted(r.items(), key=lambda x: x[1], reverse=True)





printRanking(rSorted)

#standings = getStandings(2020, END_OF_SEASON_2020)
