import sys
from static import *
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import teamyearbyyearstats
import pandas as pd

def saveNBAData(saveType, season = 0):
    for nba_team in TEAMS:
        team_id = TEAMS_INFO[nba_team][0]
        team_name = TEAMS_INFO[nba_team][1]
        if saveType == 'games':
            saveGames(team_id, team_name, season)
        elif saveType == 'teamStats':
            saveTeamStats(team_id, team_name)
        
def saveGames(team_id, team_name, season):
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
    games = gamefinder.get_data_frames()[0]
    games_2020 = games[games.SEASON_ID.str[-4:] == str(season-1)] # the api counts the season 2021-2022 as 2021 instead of 2022
    fileName = 'files\\'+ team_name + str(season) + '.csv'
    games_2020.to_csv(fileName, index=False, header=True)
    
def saveTeamStats(team_id, team_name):
    teamyearbyyear = teamyearbyyearstats.TeamYearByYearStats(team_id)
    teamStats = teamyearbyyear.get_data_frames()
    teamStats = pd.DataFrame(teamStats[0]) # get_data_frames doesn't work fully for this
    fileName = 'files\\'+ team_name +'_teamStats' + '.csv'
    teamStats.to_csv(fileName, index=False, header=True)


if len(sys.argv) == 1:
    season = 2022
elif len(sys.argv) == 2:
    season = int(sys.argv[1])
else:
    sys.exit('first (optional) argument should be the season of the ranking in yyyy format')

saveNBAData('games', season - 1) # you need the previous season to get the ranking of the current season
saveNBAData('games', season) 
saveNBAData('teamStats')