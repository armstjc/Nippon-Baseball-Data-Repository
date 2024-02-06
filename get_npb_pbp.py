from datetime import datetime
import json
import logging
import time
import pandas as pd
from tqdm import tqdm
from get_npb_schedule import get_npb_schedule


from utls import get_json_from_url

def get_npb_pbp_by_game(game_id:int):
    """
    """
    logging.info(f"Getting PBP data for game ID #{game_id}.")
    

def get_npb_pbp_by_season(season: int, save_results=False):
    """
    """
    pbp_df = pd.DataFrame()
    game_df = pd.DataFrame()

    logging.info(f"Getting the NPB schedule for the {season} season.")
    
    sched_df = get_npb_schedule(season=season)
    game_ids_arr = sched_df['game_id'].to_numpy()

    for game_id in game_ids_arr:
        
        game_df = get_npb_pbp_by_game(game_id=game_id)
        pbp_df = pd.concat([pbp_df,game_df],ignore_index=True)

    return pbp_df
    
if __name__ == "__main__":
    now = datetime.now()

    f_year = now.year - 2
    c_year = now.year + 1

    print("Getting NPB Standings data.")
    for i in tqdm(range(2018,c_year)):
        get_npb_pbp_by_season(
            season=i,
            save_results=True
        )
        time.sleep(1)
    
