import sys
import datetime
from ranking import *
from visualizer import *

if len(sys.argv) == 1: # then today
    today =  datetime.date.today()
    date = datetime.date(today.year, today.month, today.day)
elif len(sys.argv) == 2: 
    date = converToDateFormat(sys.argv[1])
else:
    sys.exit('first (optional) argument should be the date in yyyy-mm-dd format')

season = 2022 # should be read from date

r = rankTeams(season, date)

standings = getStandings(season, date)
printRanking(r, standings)

