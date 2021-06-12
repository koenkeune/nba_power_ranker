import pandas as pd
import datetime
from static import *

# look at games played in the season
def rankTeam(team, season, date1):
    first_week = 52
    last_week = 19
    
    
    fileName = 'files\\'+ team + str(season) + '.csv'
    games = pd.read_csv(fileName)
    
        
    
    dateFormat = converToDateFormat(date1)
    
    
    
    # games['GAME_DATE'] = pd.to_datetime(games['GAME_DATE'], format='%Y-%m-%d')
    # games['GAME_DATE'] = games['GAME_DATE'].map(converToDateFormat) # in date format
    
    dates_after = games['GAME_DATE'][games['GAME_DATE'] > games['GAME_DATE'][5]]
    dates_before = games['GAME_DATE'][games['GAME_DATE'] < dateFormat]
    
    
    # print(START_OF_SEASON_2020)
    # print(dateFormatStart.isocalendar()[1])
    # print(dateFormatEnd.isocalendar()[1])
    
    # give score of game
    # penalize based on how far back the game was
    
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
    
def getStrengthOfOpponents(standings):
    # average winning percentage of opponents played (and opponents opponents)
    # look at home vs away

    return(1)
    
def scoreGame(game):
    # look up ranking other team
    # look up difference game
    
    # return score
    return(1)
    
    
def penalizeScore(gamesBack, season):
    # a function that lowers the score based on how far back the game was
    return(1)
    
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

date = '2020-12-22'
# rankTeam('ATL', 2020, date)

wP = winPctLastSeason(2019)
wPSorted = sorted(wP.items(), key=lambda x: x[1])
print(wPSorted)
#standings = getStandings(2020, END_OF_SEASON_2020)
