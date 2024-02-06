from datetime import datetime
import json
import logging
import time
import pandas as pd
from tqdm import tqdm


from utls import get_json_from_url


def get_npb_standings_by_game(season: int, save_results=False):
    """
    """
    standings_df = pd.DataFrame()
    cl_df = pd.DataFrame()
    pl_df = pd.DataFrame()

    url_1 = f"https://spaia.jp/baseball/npb/api/official_stats_history?GameAssortment=1&Year={season}"
    url_2 = f"https://spaia.jp/baseball/npb/api/official_stats_history?GameAssortment=2&Year={season}"

    # Central League (1)
    json_data_cl = get_json_from_url(url=url_1)
    cl_df = pd.DataFrame(json_data_cl)
    cl_df['league'] = "central"

    # Pacific League (2)
    json_data_pl = get_json_from_url(url=url_2)
    pl_df = pd.DataFrame(json_data_pl)
    cl_df['league'] = "pacific"

    standings_df = pd.concat([cl_df, pl_df], ignore_index=True)
    if save_results == True and len(standings_df) > 0:
        standings_df.to_csv(f"standings/{season}_game_standings.csv",index=False)
        standings_df.to_parquet(
            f"standings/{season}_game_standings.parquet",index=False)
        with open (f"standings/{season}_pacific_league_game_standings.json","w+") as f:
            f.write(json.dumps(json_data_pl,indent=4))
        with open (f"standings/{season}_central_league_game_standings.json","w+") as f:
            f.write(json.dumps(json_data_cl,indent=4))

    elif len(standings_df) == 0:
        logging.warning("No data was found. Returning empty dataframe.")

    return standings_df

    
if __name__ == "__main__":
    now = datetime.now()

    f_year = now.year - 2
    c_year = now.year + 1

    print("Getting NPB Standings data.")
    for i in tqdm(range(2018,c_year)):
        get_npb_standings_by_game(
            season=i,
            save_results=True
        )
        time.sleep(1)
    
