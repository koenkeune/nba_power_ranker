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

r = rankTeams(date)
standings = getStandings(date)

printRanking(r, standings)

