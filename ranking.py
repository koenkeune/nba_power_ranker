import pandas as pd
import datetime
from static import *
from calculations import *

# get the ranking of a team from a certain date
def rankTeams(season, date):
    # starting point of the ranking:
    e = winPctLastSeason(season - 1)
    r = {}
    for team in TEAMS:
        r[team] = getEloFromE(e[team], 1500) # assumes balanced schedule with enough games played
        
    rSorted = sorted(r.items(), key=lambda x: x[1], reverse=True)
        
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
        rNew = {} 
        for team in TEAMS:
            game = games[team][games[team]['GAME_DATE'] == currentDate]
            if not(game.empty):
                matchup = game['MATCHUP'].to_string()
                opponent = matchup[-3:]
                if matchup.find('@') > -1:
                    homeTeam = opponent
                else:
                    homeTeam = team
                mov = int(game['PLUS_MINUS']) # margin of victory
                s1 = .5
                if mov > 0:
                    s1 = 1
                else:
                    s1 = 0
                rNew[team] = getElo(r[team], r[opponent], s1, 20, mov, homeTeam, team)
        for team in rNew.keys(): # to prevent adjusting the same game with different r's
            r[team] = rNew[team]
        currentDate += datetime.timedelta(days = 1)
    
    return(r)
    
    
    
# there should have been at least one game played    
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