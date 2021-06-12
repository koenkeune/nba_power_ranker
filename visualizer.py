from static import *

def printRanking(ranking):
    for i in range(len(ranking)):
        print(i+1, TEAMS_INFO[ranking[i][0]][5])