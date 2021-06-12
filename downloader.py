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
    games_2020 = games[games.SEASON_ID.str[-4:] == str(season)]
    fileName = 'files\\'+ team_name + str(season) + '.csv'
    games_2020.to_csv(fileName, index=False, header=True)
    
def saveTeamStats(team_id, team_name):
    teamyearbyyear = teamyearbyyearstats.TeamYearByYearStats(team_id)
    teamStats = teamyearbyyear.get_data_frames()
    teamStats = pd.DataFrame(teamStats[0]) # get_data_frames doesn't work fully for this
    fileName = 'files\\'+ team_name +'_teamStats' + '.csv'
    teamStats.to_csv(fileName, index=False, header=True)


# saveNBAData('games', 2019)
# saveNBAData('games', 2020) # you need 2 seasons to get the power ranking of 1 full season
# saveNBAData('teamStats')

    
    


    
    


