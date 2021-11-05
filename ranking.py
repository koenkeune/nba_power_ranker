import pandas as pd
import datetime
from static import *
from calculations import *

# get the ranking of a team from a certain date
def rankTeams(date):
    season = getSeasonFromDate(date)
    k = 30 # how quick should the algorithm react to changes (20 is standard)
    k_pre = k/2 # preseason k

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
    preseasonDate = 'START_OF_PRESEASON_' + str(season)
    loopDate = converToDateFormat(SCHEDULE_DATES[preseasonDate])
    startSeasonDate = 'START_OF_SEASON_' + str(season)
    startSeasonDate = converToDateFormat(SCHEDULE_DATES[startSeasonDate])
    endSeasonDate = 'END_OF_SEASON_' + str(season)
    endSeasonDate =  converToDateFormat(SCHEDULE_DATES[endSeasonDate])
    while (loopDate <= date) and (loopDate <= endSeasonDate):
        rNew = {} 
        for team in TEAMS:
            game = games[team][games[team]['GAME_DATE'] == loopDate]
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
                if  loopDate < startSeasonDate:
                    rNew[team] = getElo(r[team], r[opponent], s1, k_pre, mov, homeTeam, team)
                else:
                    rNew[team] = getElo(r[team], r[opponent], s1, k, mov, homeTeam, team)
                
        for team in rNew.keys(): # to prevent adjusting the same game with different r's
            r[team] = rNew[team]
        loopDate += datetime.timedelta(days = 1)
    
    return(r)
    
# there should have been at least one game played    
def getStandings(date):
    season = getSeasonFromDate(date)
    startSeasonDate = 'START_OF_SEASON_' + str(season)
    startDate = converToDateFormat(SCHEDULE_DATES[startSeasonDate])
    standings = {}
    for team in TEAMS:
        fileName = 'files\\'+ team + str(season) + '.csv'
        allGames = pd.read_csv(fileName)
        allGames['GAME_DATE'] = allGames['GAME_DATE'].map(converToDateFormat) # in date format
        games = allGames[allGames['GAME_DATE'] <= date]
        games = games[games['GAME_DATE'] >= startDate]
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
        year = str(season - 1) + '-' + str(season - 2000)
        wP[team] = float(teamStats[teamStats['YEAR'] == year]['WIN_PCT'])
    return(wP)

def getSeasonFromDate(date):
    season = int(date.year)
    preseasonDate = 'START_OF_PRESEASON_' + str(season + 1)
    if date > converToDateFormat(SCHEDULE_DATES[preseasonDate]):
        return(season + 1)
    else:
        return(season)
    
    