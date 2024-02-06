from datetime import datetime
import json
import logging
import time
import pandas as pd
from tqdm import tqdm


from utls import get_json_from_url


def get_npb_schedule(season: int, save_results=False) -> pd.DataFrame():
    """

    """
    sched_df = pd.DataFrame()
    columns = [
        'season',
        'ID',
        'SeqNo',
        'game_id',
        'game_kind_id',
        'date_jpn',
        'time_jpn',
        'week_day_jpn',
        'stadium_id',
        'stadium_name_jpn',
        'round',
        'DhF',
        'game_state',
        'game_result',

        'home_score',
        'home_team_id',
        'home_team_short_name',
        'home_team_name_en',
        'home_team_name_en_short',
        'home_team_initial',
        'home_section',
        'home_text_area',

        'away_score',
        'away_team_id',
        'away_team_short_name',
        'away_team_name_en',
        'away_team_name_en_short',
        'away_team_initial',
        'away_section',
        'away_text_area',

        'stadium_name_short',
        'last_updated',
        'creation_date'
    ]

    url = f"https://spaia.jp/baseball/npb/api/schedules?Year={season}"
    json_data = get_json_from_url(url=url)

    sched_df = pd.DataFrame(json_data)

    sched_df.rename(
        columns={
            "GameID": "game_id",
            "GameKindID": "game_kind_id",
            "DateJPN": "date_jpn",
            "TimeJPN": "time_jpn",
            "WeekDayJPN": "week_day_jpn",
            "StadiumID": "stadium_id",
            "StadiumName": "stadium_name_jpn",
            "Round": "round",
            "GameState": "game_state",
            "GameResult": "game_result",
            "HScore": "home_score",
            "VScore": "away_score",
            "HTeamID": "home_team_id",
            "HTeamNameS": "home_team_short_name",
            "VTeamID": "away_team_id",
            "VTeamNameS": "away_team_short_name",
            "StadiumNameS": "stadium_name_short",
            "HomeTeamNameE": "home_team_name_en",
            "HomeTeamNameES": "home_team_name_en_short",
            "HomeTeamInitial": "home_team_initial",
            "VisitorTeamNameE": "away_team_name_en",
            "VisitorTeamNameES": "away_team_name_en_short",
            "VisitorTeamInitial": "away_team_initial",
            "Home_Section": "home_section",
            "Home_TextArea": "home_text_area",
            "Visitor_Section": "away_section",
            "Visitor_TextArea": "away_text_area",
            "UpdatedAt": "last_updated",
            "Year": "season",
            "CreatedAt": "creation_date"
        }, inplace=True
    )

    sched_df = sched_df[columns]

    if save_results == True and len(sched_df) > 0:
        sched_df.to_csv(f"schedules/{season}_npb_schedule.csv", index=False)
        sched_df.to_parquet(
            f"schedules/{season}_npb_schedule.parquet", index=False)
        with open (f"schedules/{season}_npb_schedule.json","w+") as f:
            f.write(json.dumps(json_data,indent=4))
    elif len(sched_df) == 0:
        logging.warning("No data was found. Returning empty dataframe.")

    return sched_df


if __name__ == "__main__":
    now = datetime.now()

    f_year = now.year - 2
    c_year = now.year + 1

    print("Getting NPB schedule data.")
    for i in tqdm(range(f_year,c_year)):
        df = get_npb_schedule(
            season=i,
            save_results=True
        )
        print(df)
        time.sleep(1)
