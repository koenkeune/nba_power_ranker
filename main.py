import sys
from ranking import *
from visualizer import *

if len(sys.argv) == 1:
    date = '2021-02-15'
elif len(sys.argv) == 2:
    date = int(sys.argv[1])
else:
    sys.exit('first (optional) argument should be the date in yyyy-mm-dd format')

season = 2020
r = rankTeams(season, date)

standings = getStandings(season, date)
printRanking(r, standings)

