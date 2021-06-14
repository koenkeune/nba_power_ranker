import numpy as np

def getExpectedWinPct(r1, r2):
    e = 1 / (1 + 10 ** ((r2 - r1)/400))
    
    return(e)
    
def getMOVMultiplier(r1, r2, mov):
    movM = ((abs(mov) + 3) ** .8) / (7.5 + 0.006 * (r1 - r2))
    
    return(movM)

def getHomeAdv(team):
    homeAdv = 100

    return(homeAdv)
    
def getElo(r1, r2, s1, k, mov, homeTeam, team):
    if homeTeam == 'team1':
        r1 + getHomeAdv(team)
    elif homeTeam == 'team2':
        r2 + getHomeAdv(team)
    e1 = getExpectedWinPct(r1, r2)
    r1New = r1 + k * (s1  - e1)
    movM = getMOVMultiplier(r1, r2, mov)
    r1New = r1 + movM * k * (s1 - e1)
    
    return(r1New)

def getEloFromE(e, r2):
    delta = 400 * (np.log10(1/e - 1))
    r1 = r2 - delta
    
    return(r1)
    
def getEFromWP(p1,p2): # get expected win pct against another team from their expected win pct against all teams
    return(p1*(1-p2) / (p1*(1-p2) + p2*(1-p1)))

def winPCTCorrection(p, n):
    return(p - (p - .5)/(n - 1))
    