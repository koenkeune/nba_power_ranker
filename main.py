import sys
import datetime
from ranking import *
from visualizer import *

if len(sys.argv) == 1:
    date = END_OF_SEASON_2020
elif len(sys.argv) == 2:
    date = int(sys.argv[1])
else:
    sys.exit('first (optional) argument should be the date in yyyy-mm-dd format')

season = 2020
date = converToDateFormat(date)
r = rankTeams(season, date)

standings = getStandings(season, date)
printRanking(r, standings)

