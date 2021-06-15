from static import *
from calculations import getExpectedWinPct

def printRanking(r, standings):
    rSorted = sorted(r.items(), key=lambda x: x[1], reverse=True)
    for i in range(len(rSorted)):
        abr = rSorted[i][0]
        win_pct = rSorted[i][1]
        team = TEAMS_INFO[abr][5]
        streak = 'none'
        if standings[abr][5][0] == 'W':
            streak = 'wins'
            if standings[abr][5][1] == 1:
                streak = 'win' 
        elif standings[abr][5][0] == 'L':
            streak = 'losses'
            if standings[abr][5][1] == 1:
                streak = 'loss'
        print(i+1, team, '  Record:', standings[abr][1], '-', standings[abr][2], 
              ', exp win pct:', round(getExpectedWinPct(rSorted[i][1], 1500) * 100), ', win pct:', 
              round(standings[abr][3] * 100), ', last 10:', standings[abr][4], ', streak:', 
              standings[abr][5][1], streak)
        
            