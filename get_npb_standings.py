from datetime import datetime
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
    json_data = get_json_from_url(url=url_1)
    cl_df = pd.DataFrame(json_data)

    # Pacific League (2)
    json_data = get_json_from_url(url=url_2)
    pl_df = pd.DataFrame(json_data)

    standings_df = pd.concat([cl_df, pl_df], ignore_index=True)
    if save_results == True:
        standings_df.to_csv(f"standings/{season}_game_standings.csv",index=False)
        standings_df.to_parquet(
            f"standings/{season}_game_standings.parquet",index=False)

    return standings_df

    
if __name__ == "__main__":
    now = datetime.now()
    f_year = now.year - 2
    c_year = now.year + 1
    for i in tqdm(range(f_year,c_year)):
        df =get_npb_standings_by_game(
            season=i,
            save_results=True
        )
    print(df)
