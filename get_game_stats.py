# import json
import logging
# import time
from datetime import datetime
from os import mkdir
from os.path import exists
from random import shuffle

import cutlet
import pandas as pd
from tqdm import tqdm

from get_npb_schedule import get_npb_schedule
from utls import get_json_from_url


def get_game_stats(game_id: int, game_date: str = None):
    """ """
    katsu = cutlet.Cutlet()

    def translate_stuff(input_str: str) -> str:
        """ """
        return katsu.romaji(input_str, title=True)

    stats_columns = [
        "season",
        "game_id",
        "game_date",
        "player_id",
        "player_name_jap",
        "player_name",
        "player_jersey_number",
        "position",
        "team_id",
        "batting_G",
        "batting_GS",
        "batting_PA",
        "batting_AB",
        "batting_R",
        "batting_H",
        "batting_2B",
        "batting_3B",
        "batting_HR",
        "batting_RBI",
        "batting_SB",
        "batting_CS",
        "batting_BB",
        "batting_SO",
        "batting_HBP",
        "batting_SH",
        "batting_SF",
        "batting_E",
        "pitcher_order_number",
        "pitching_G",
        "pitching_GS",
        "pitching_W",
        "pitching_L",
        "pitching_ERA",
        "pitching_IP",
        "pitching_IP_str",
        "pitching_CG",
        "pitching_SHO",
        "pitching_SV",
        "pitching_H",
        "pitching_R",
        "pitching_ER",
        "pitching_HR",
        "pitching_IBB",
        "pitching_BB",
        "pitching_SO",
        "pitching_HBP",
        "pitching_BK",
        "pitching_BF",
        "pitching_PI",
    ]
    if exists(f"game_stats/individual_games/{game_id}.csv"):
        df = pd.read_csv(f"game_stats/individual_games/{game_id}.csv")
        return df

    batting_url = (
        "https://spaia.jp/baseball/npb/api/" +
        f"both_batter_game_stats?matchday={game_date}&gameId={game_id}"
    )
    pitching_url = (
        "https://spaia.jp/baseball/npb/api/" +
        f"both_pitcher_game_stats?gameId={game_id}"
    )
    batting_json = get_json_from_url(batting_url)
    pitching_json = get_json_from_url(pitching_url)

    batting_df = pd.json_normalize(batting_json)

    batting_df.rename(
        columns={
            "playerId": "player_id",
            "playerName": "player_name_jap",
            "teamId": "team_id",
            "shortNameTeam": "team_name",
            "arm": "arm_id",
            "number": "player_jersey_number",
            # "number": "player_jersey_number",
            "avg": "batting_AVG",
            "ops": "batting_OPS",
            "pa": "batting_PA",
            "ab": "batting_AB",
            "h": "batting_H",
            "hr": "batting_HR",
            "rbi": "batting_RBI",
            "r": "batting_R",
            "h2b": "batting_2B",
            "h3b": "batting_3B",
            "so": "batting_SO",
            "hp": "batting_HBP",
            "bb": "batting_BB",
            "sb": "batting_SB",
            "cs": "batting_CS",
            "sh": "batting_SH",
            "sf": "batting_SF",
            "e": "batting_E",
        },
        inplace=True,
    )

    if len(batting_df) == 0:
        return pd.DataFrame()

    batting_df = batting_df.astype(
        {
            "player_id": "Int64",
            "player_name_jap": "str",
            "player_jersey_number": "Int16",
            "position": "str",
            "team_id": "UInt16",
            # "team_name": "str",
            "rowno": "UInt16",
            "seqno": "UInt8",
            # "batting_AVG":"Float32",
            "batting_PA": "UInt16",
            "batting_AB": "UInt16",
            "batting_H": "UInt16",
            "batting_HR": "UInt16",
            "batting_RBI": "UInt16",
            "batting_R": "UInt16",
            "batting_2B": "UInt16",
            "batting_3B": "UInt16",
            "batting_SO": "UInt16",
            "batting_BB": "UInt16",
            "batting_HBP": "UInt16",
            "batting_SH": "UInt16",
            "batting_SF": "UInt16",
            "batting_E": "UInt16",
            "batting_SB": "UInt16",
        }
    )
    batting_df["player_name_jap"] = batting_df[
        "player_name_jap"
    ].str.replace("　", " ")
    batting_df["batting_G"] = 1
    batting_df["batting_GS"] = batting_df["seqno"]
    batting_df.loc[batting_df["batting_GS"] > 1, "batting_GS"] = 0

    batting_df.drop(
        columns=[
            "batting_OPS",
            "batting_AVG",
            "condition",
            "battingResult",
            "rowno",
            "seqno",
        ],
        inplace=True,
    )
    pitching_df = pd.json_normalize(pitching_json)

    pitching_df.rename(
        columns={
            "playerId": "player_id",
            "playerName": "player_name_jap",
            "teamId": "team_id",
            "shortNameTeam": "team_name",
            "arm": "arm_id",
            "number": "player_jersey_number",
            "no": "pitcher_order_number",
            "nopg": "pitching_PI",
            "ip": "ip_innings",
            "ip3": "ip_partial_innings",
            "bf": "pitching_BF",
            "h": "pitching_H",
            "hr": "pitching_HR",
            "so": "pitching_SO",
            "bb": "pitching_BB",
            "hbp": "pitching_HBP",
            "r": "pitching_R",
            "er": "pitching_ER",
            "totalEra": "pitching_ERA",
            "totalWin": "pitching_W",
            "totalLose": "pitching_L",
            "totalSave": "pitching_SV",
        },
        inplace=True,
    )
    pitching_df = pitching_df.astype(
        {
            "player_id": "Int64",
            "player_name_jap": "str",
            "team_id": "UInt16",
            "team_name": "str",
            "arm_id": "UInt8",
            "player_jersey_number": "Int16",
            "pitcher_order_number": "UInt8",
            "pitching_PI": "UInt16",
            "ip_innings": "UInt8",
            "ip_partial_innings": "UInt8",
            "pitching_BF": "UInt16",
            "pitching_H": "UInt16",
            "pitching_HR": "UInt16",
            "pitching_SO": "UInt16",
            "pitching_BB": "UInt16",
            "pitching_HBP": "UInt16",
            "pitching_ER": "UInt16",
            # "pitching_ERA": "Float32",
            "pitching_W": "UInt16",
            "pitching_L": "UInt16",
            "pitching_SV": "UInt16",
        }
    )
    pitching_df["player_name_jap"] = pitching_df[
        "player_name_jap"
    ].str.replace(
        "　", " "
    )
    pitching_df["player_name"] = pitching_df["player_name_jap"].map(
        translate_stuff
    )
    pitching_df["pitching_G"] = 1
    pitching_df["pitcher_order_number"] = pitching_df["pitcher_order_number"]
    pitching_df.loc[pitching_df["pitcher_order_number"] > 1, "pitching_GS"] = 0

    pitching_df["ip_partial_innings"] = pitching_df[
        "ip_partial_innings"
    ].fillna(0)
    pitching_df["pitching_IP"] = pitching_df["ip_innings"] + (
        pitching_df["ip_partial_innings"] / 3
    )
    pitching_df["pitching_IP_str"] = (
        pitching_df["ip_innings"].astype("str")
        + "."
        + pitching_df["ip_partial_innings"].astype("str")
    )

    pitching_df.drop(
        columns=[
            "team_name",
            "ip_innings",
            "ip_partial_innings",
            "condition",
            "winLoseSaveHoldFlag",
            "arm_id",
        ],
        inplace=True,
    )
    stats_df = batting_df.merge(
        right=pitching_df,
        how="outer",
        on=[
            "player_id",
            "player_name_jap",
            "team_id",
            # "team_name",
            "player_jersey_number",
        ],
    )

    for c in stats_df.columns:
        if c not in stats_columns:
            raise IndexError(f"Unhandled column `{c}`")
    stats_df = stats_df.reindex(columns=stats_columns)
    game_date = datetime.strptime(f"{game_date}", "%Y%m%d")
    stats_df["game_id"] = game_id
    stats_df["game_date"] = game_date
    stats_df["season"] = game_date.year
    stats_df.to_csv(f"game_stats/individual_games/{game_id}.csv", index=False)
    return stats_df


def get_season_game_stats(season: int, month: int = None):
    """ """
    game_stats_df = pd.DataFrame()
    game_df = pd.DataFrame()

    try:
        mkdir("game_stats/individual_games")
    except FileExistsError:
        logging.info(
            "`game_stats/individual_games` already exists"
        )
    except Exception as e:
        raise e

    logging.info(
        "Getting the NPB schedule for the %s season.",
        season
    )

    sched_df = get_npb_schedule(season=season)
    sched_df = sched_df.sample(frac=1)
    sched_df = sched_df[
        (sched_df["home_score"] > 0) |
        (sched_df["away_score"] > 0)
    ]
    sched_df["month"] = pd.DatetimeIndex(sched_df["game_date"]).month
    if month is not None:
        sched_df = sched_df[sched_df["month"] == month]

    month_arr = list(set(sched_df["month"].to_list()))

    for m in month_arr:
        game_stats_df_arr = []

        temp_df = sched_df[sched_df["month"] == m]
        game_ids_arr = temp_df["game_id"].to_numpy()
        game_dates_arr = temp_df["date_jpn"].to_numpy()
        print(f"Getting {season}-{m:02} NPB game stats.")

        del temp_df
        shuffle(game_ids_arr)
        for i in tqdm(range(0, len(game_ids_arr))):
            game_id = game_ids_arr[i]
            game_date = game_dates_arr[i]
            game_df = get_game_stats(game_id=game_id, game_date=game_date)
            game_df["player_name_jap"] = game_df[
                "player_name_jap"
            ].str.replace(
                "　", " "
            )
            game_stats_df_arr.append(game_df)
            del game_df

        game_stats_df = pd.concat(game_stats_df_arr, ignore_index=True)
        game_stats_df.to_csv(
            f"game_stats/{season}-{m:02}_game_stats.csv",
            index=False
        )
    return game_stats_df


def main():
    """ """
    now = datetime.now()

    # f_year = now.year - 2
    # c_year = now.year + 1

    print("Getting NPB game stats data.")
    # for i in range(f_year, c_year):
    #     get_season_game_stats(season=i)
    #     # time.sleep(1)
    if now.day <= 2:
        get_season_game_stats(
            season=now.year,
            month=(now.month - 1)
        )

    get_season_game_stats(
        season=now.year,
        month=now.month
    )


if __name__ == "__main__":
    main()
