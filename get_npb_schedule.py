from datetime import datetime, timedelta
import time
import pandas as pd
import requests
from tqdm import tqdm


from utls import get_json_from_url


def get_npb_schedule(season: int, save_results=False):
    """

    """
    sched_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = f"https://spaia.jp/baseball/npb/api/schedules?Year={season}"
    json_data = get_json_from_url(url=url)

    for game in tqdm(json_data):
        game_id = game['GameID']
        row_df = pd.DataFrame(
            {"game_id":game_id},
            index=[0]
        )
        row_df['game_kind_id'] = game['Year']

        date_str = f"{game['DateJPN']} {game['TimeJPN']}"
        game_date = datetime.strptime(date_str, "%Y%m%d %H%M")
        del date_str
        row_df['season'] = game['Year']
        row_df['game_datetime_jpn'] = game_date
        row_df['game_datetime_iso'] = game_date - timedelta(hours=9)
        row_df['stadium_id'] = game['StadiumID']
        row_df['stadium_name_jp'] = game['StadiumName']
        row_df['round'] = game['Round']
        row_df['dhf'] = game['DhF']
        row_df['game_state'] = game['GameState']
        row_df['game_result'] = game['GameResult']
        row_df['home_score'] = game['HScore']
        row_df['away_score'] = game['VScore']
        
        row_df['home_team_id'] = game['HTeamID']
        row_df['home_team_short_name'] = game['HTeamNameS']
        row_df['home_team_en_name'] = game['HomeTeamNameE']
        row_df['home_team_initial'] = game['VisitorTeamInitial']
        row_df['home_team_en_initial'] = game['HomeTeamNameES']
        
        row_df['away_team_id'] = game['VTeamID']
        row_df['away_team_short_name'] = game['VTeamNameS']
        row_df['away_team_en_name'] = game['VisitorTeamNameE']
        row_df['away_team_initial'] = game['VisitorTeamInitial']
        row_df['away_team_en_initial'] = game['VisitorTeamNameES']
        
        row_df['stadium_short_name'] = game['StadiumNameS'] # ?

        row_df['home_wins'] = game['Win']
        row_df['home_losses'] = game['Lose']
        row_df['home_draws'] = game['Draw']
        row_df['home_batting_avg'] = game['Avg']
        row_df['home_pitching_era'] = game['Era']
        row_df['home_section'] = game['Home_Section']
        row_df['home_jp_description'] = game['Home_TextArea']

        row_df['away_wins'] = game['Visitor_Win']
        row_df['away_losses'] = game['Visitor_Lose']
        row_df['away_draws'] = game['Visitor_Draw']
        row_df['away_batting_avg'] = game['Visitor_Avg']
        row_df['away_pitching_era'] = game['Visitor_Era']
        row_df['away_section'] = game['Visitor_Section']
        row_df['away_jp_description'] = game['Visitor_TextArea']
        
        row_df['last_updated'] = game['UpdatedAt']
        sched_df = pd.concat([sched_df,row_df],ignore_index=True)

    if save_results == True:
        sched_df.to_csv(f"schedules/{season}_npb_schedule.csv", index=False)
        sched_df.to_parquet(
            f"schedules/{season}_npb_schedule.parquet", index=False)

    return sched_df


if __name__ == "__main__":
    now = datetime.now()
    for i in range(2017, now.year+1):
        df = get_npb_schedule(
            season=i,
            save_results=True
        )
        time.sleep(1)
