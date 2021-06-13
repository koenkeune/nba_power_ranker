import pandas as pd
import datetime
from static import *

# get the ranking of a team from a certain date
def rankTeams(season, date):
    # starting point of the ranking:
    e = winPctLastSeason(season - 1)
    r = {}
    for team in TEAMS:
        r[team] = getEloFromE(e[team])
    
    # pre-load the needed data:
    games = {} 
    for team in TEAMS:
        fileName = 'files\\'+ team + str(season) + '.csv'
        teamGames = pd.read_csv(fileName)
        teamGames['GAME_DATE'] = teamGames['GAME_DATE'].map(converToDateFormat) # in date format
        games[team] = teamGames
    
    # get ranks:
    currentDate = converToDateFormat(START_OF_PRESEASON_2020)
    endDate = converToDateFormat(date)
    while currentDate <= endDate:
        print(currentDate)

        for team in TEAMS:
            game = games[team][games[team]['GAME_DATE'] == currentDate]
            if not(game.empty):
                opponent = game['MATCHUP'].to_string()[-3:]
                mov = int(game['PLUS_MINUS'])
                s1 = .5
                if mov > 0:
                    s1 = 1
                else:
                    s1 = 0
                r1 = r[team]
                r2 = r[opponent]


        currentDate += datetime.timedelta(days = 1)
        
            
    # fileName = 'files\\'+ team + str(season) + '.csv'
    # games = pd.read_csv(fileName)
    
    
    
    
    
# there should have at least one game been played    
def getStandings(season, date):
    startDateFormat = converToDateFormat(START_OF_SEASON_2020)
    endDateFormat = converToDateFormat(date)
    standings = {}
    for team in TEAMS:
        fileName = 'files\\'+ team + str(season) + '.csv'
        allGames = pd.read_csv(fileName)
        allGames['GAME_DATE'] = allGames['GAME_DATE'].map(converToDateFormat) # in date format
        games = allGames[allGames['GAME_DATE'] <= endDateFormat]
        games = games[games['GAME_DATE'] >= startDateFormat]
        gamesPlayed = len(games)
        wins = len(games[games['WL'] == 'W'])
        losses = len(games[games['WL'] == 'L'])
        winPct = wins / gamesPlayed
        last_10_games = games.head(10)
        wins_10 = len(last_10_games[last_10_games['WL'] == 'W'])
        losses_10 = len(last_10_games[last_10_games['WL'] == 'L'])
        
        streakC = 0 # streak compare
        streak = 1 # streak
        lastWL = games['WL'].iloc[0]
        if gamesPlayed > 1:
            while games['WL'].iloc[streakC] == games['WL'].iloc[streak]:
                streakC += 1
                streak += 1
        elif gamesPlayed == 0:
            j = 0
            lastWL = 'none'
        
        standings[team] = (gamesPlayed, wins, losses, winPct, (wins_10, losses_10), (lastWL, streak))
    
    return(standings)
    
def getExpectedWinPct(r1, r2):
    e = 1 / (10 ^ ((r2 - r1)/400))
    
    return(e)
    
def getMOVMultiplier(mov):
    movM = ((mov + 3) ^ .8) / (7.5 + 0.006 * (r1 - r2))
    
    return(movM)

def getHomeAdv(team):
    
    return(100)
    
def getElo(r1, r2, s1, k, mov, homeTeam, team):
    if homeTeam == 'team1':
        r1 + getHomeAdv(team)
    elif homeTeam == 'team2':
        r2 + getHomeAdv(team)
    e1 = getExpectedWinPct(r1, r2)
    r1New = r1 + k * (s1  - e1)
    r1New = getMovMultiplier(r1, r2, mov)
    
    return(r1New)

def getEloFromE(e):
    r = 1
    return(r)

def converToDateFormat(date):
    date = date.split('-')
    return(datetime.date(int(date[0]), int(date[1]), int(date[2])))
    
def winPctLastSeason(season):
    wP = {} # winning percentage
    for team in TEAMS:
        fileName = 'files\\'+ team + '_teamStats' + '.csv'
        teamStats = pd.read_csv(fileName)
        year = str(season) + '-' + str(season - 2000 + 1)
        wP[team] = float(teamStats[teamStats['YEAR'] == year]['WIN_PCT'])
    return(wP)