from nba_api.stats.static import players 
from nba_api.stats.static import teams 
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.endpoints import leaguegamelog
import pickle
import pandas as pd
import os
import time

# Functions
def Delay():
    time.sleep(0.5)

def GetAllFormattedPlayerGameLogs(player_ids):
    full_player_logs = []
    print("Collecting player game logs...")
    for player in player_ids:
        Delay()
        player_game_log = playergamelogs.PlayerGameLogs(player_id_nullable=player, season_nullable="2023-24").get_data_frames()[0]
        player_game_log.drop(columns=player_game_log.columns[33:69], inplace=True, axis=1)
        player_game_log.drop(columns=player_game_log.columns[[0, 2, 3, 5, 6, 8, 9]], inplace=True, axis=1) 
        full_player_logs.append(player_game_log)
        print("*", end='', flush=True) # Progress Bar

    
    print("\nCollected player game logs!")
    return full_player_logs

def PrintDataFramesToFile(filename, data):
    pickle_file_path = f"{artifacts_path}\\{filename}.pkl"
    with open(pickle_file_path, "wb") as f:
        pickle.dump(data, f)

def GetDataFramesFromFile(filename):
    pickle_file_path = f"{artifacts_path}\\{filename}.pkl"
    with open(pickle_file_path, "rb") as f:
        pickle_player_ids = pickle.load(f)

    print(f"Saved {filename}!")
    return pickle_player_ids

def GetUserModeInput():
    update_database = "error"

    while ((update_database != "y") and (update_database != "n")):
        update_database = input("Update Database? (y or n): ")

    return update_database

# OS interfacing
cwd = os.getcwd() 
artifacts_path = f"{os.path.dirname(cwd)}\\artifacts"
artifacts_path_debug = f"{cwd}\\artifacts"

# Players
current_players = players._get_active_players()
current_player_ids = [player["id"] for player in current_players]
current_player_names =  [player["full_name"] for player in current_players]

# Get Game IDs
league_game_log = leaguegamelog.LeagueGameLog(season="2023-24").get_data_frames()[0]
game_ids = league_game_log['GAME_ID']
game_ids = game_ids.drop_duplicates()

# Teams
current_teams = teams._get_teams()
current_team_names = [team['full_name'] for team in current_teams]
current_team_ids = [team['id'] for team in current_teams]

# Get Script Mode
answer = GetUserModeInput()

if answer == "y":
    # Get all player game logs
    all_player_game_logs = GetAllFormattedPlayerGameLogs(current_player_ids)

    # Save data to files
    PrintDataFramesToFile("player_ids", current_player_ids)
    PrintDataFramesToFile("game_ids", game_ids)
    PrintDataFramesToFile("all_player_game_logs", all_player_game_logs)

# Use database in main program

print("Script Completed. Goodbye!")

    



