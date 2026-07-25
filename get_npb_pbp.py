"""
File: get_npb_pbp.py
Purpose: Download and parse Play by Play (PBP) data for the NPB.
"""

import json
import logging
import time
from datetime import datetime
from os import mkdir
from os.path import exists

import cutlet
import pandas as pd
from tqdm import tqdm

from get_npb_schedule import get_npb_schedule
from utls import convert_arm_id, get_json_from_url


def get_npb_pbp_by_game(game_id: int):
    """ """
    katsu = cutlet.Cutlet()
    # now = datetime.now
    player_mapper_arr = {}
    # x = float('nan')

    # def player_mapper(player_name: str = None) -> int:
    #     """ """
    #     if player_name == x:
    #         return np.nan
    #     # if player_name not in player_mapper_arr:
    #     #     return np.nan

    #     check = player_mapper_arr[player_name]
    #     print()
    #     return check

    def translate_stuff(input_str: str) -> str:
        """ """
        return katsu.romaji(input_str, title=True)

    def extract_ball_num_from_pbp(input_str: str) -> int:
        """ """

        if "球目:" in input_str:
            ball_num = input_str.split("球目:")[0]
            ball_num = int(ball_num)
            return ball_num
        else:
            return 0

    stats_columns = [
        "season",
        "game_id",
        "game_date",
        "play_id",
        "page",
        "game_round",
        "game_type_id",
        "game_type_name",
        "inning",
        # "game_state_id",
        "game_state_name",
        "inning_ab_num",
        "umpire_home",
        "umpire_first",
        "umpire_second",
        "umpire_third",
        "umpire_left",
        "umpire_right",
        "H_HV",
        "home_team_id",
        "home_team_name",
        "home_team_abv",
        "home_total_runs",
        "away_team_id",
        "away_team_name",
        "away_team_abv",
        "away_total_runs",
        "result_id",
        "end_time",
        "win_pitcher",
        "loss_pitcher",
        "save_pitcher",
        "description_jap",
        "description",
        "PlayInfo_SeqNo",
        "PlayInfo_AB",
        "PlayInfo_PlayerID",
        "PlayInfo_PlayerName",
        "atBatBallCount",
        "fiveDigitSerialNumber",
        "pitch_number",
        "release_speed_kmh",
        "release_speed_mph",
        "pitch_id",
        "plate_x",
        "plate_y",
        "presult",
        "bresult",
        "pitcher",
        "batter",
        "hc_x",
        "hc_y",
        "fielder",
        "fielder_name",
        "hit_location",
        "ballCatcherNum",
        "addedRuns",
        "pitcher_hand",
        "batter_hand",
        "strikes",
        "balls",
        "outs_when_up",
        "on_1b",
        "on_1b_name",
        "on_2b",
        "on_2b_name",
        "on_3b",
        "on_3b_name",
        "fielder_1",
        "fielder_1_name",
        "fielder_2",
        "fielder_2_name",
        "fielder_3",
        "fielder_3_name",
        "fielder_4",
        "fielder_4_name",
        "fielder_5",
        "fielder_5_name",
        "fielder_6",
        "fielder_6_name",
        "fielder_7",
        "fielder_7_name",
        "fielder_8",
        "fielder_8_name",
        "fielder_9",
        "fielder_9_name",
        "UpdatedAt",
        "CreatedAt",
        "is_double_header_finale",
        "game_attendance",
        "stadium_id",
        "stadium_name",
    ]

    if exists(f"pbp/individual_games/{game_id}.csv"):
        df = pd.read_csv(f"pbp/individual_games/{game_id}.csv")
        return df

    if game_id == 2021000953:
        # known bad game
        return pd.DataFrame()

    # stats_df = get_game_stats(game_id=game_id)
    time.sleep(1)
    logging.info("Getting PBP data for game ID #%s.", game_id)
    # roster_df = pd.DataFrame()
    pbp_df = pd.DataFrame()

    pitch_box_location_url = (
        "https://spaia.jp/baseball/npb/api/" +
        f"flash_atbat_history?gameId={game_id}"
    )
    pbp_text_url = (
        f"https://spaia.jp/baseball/npb/api/game_text_pbp?GameID={game_id}"
    )
    strike_ball_count_url = (
        f"https://spaia.jp/baseball/npb/api/ball_count?gameId={game_id}"
    )
    on_base_url = f"https://spaia.jp/baseball/npb/api/runner?gameId={game_id}"
    fielders_url = (
        f"https://spaia.jp/baseball/npb/api/position?gameId={game_id}"
    )

    pbp_json = get_json_from_url(pbp_text_url)
    if len(pbp_json) == 0:
        return pd.DataFrame()
    pbp_df = pd.json_normalize(pbp_json)
    pbp_df["atBatBallCount"] = pbp_df["TextInfo_Bat_Text"].map(
        extract_ball_num_from_pbp
    )
    pbp_df["page"] = (
        pbp_df["Inning"].str.pad(2, fillchar="0")  # inning number
        + pbp_df["TB"]  # Top/Bottom key
        + pbp_df["TextInfo_Bat_No"].str.pad(2, fillchar="0")  # Inning AB
        + pbp_df["atBatBallCount"]
        .astype("str")
        .str.pad(2, fillchar="0")  # pitch number
    )
    pbp_df["game_date"] = pd.to_datetime(
        pbp_df["GameDate"].astype("str") +
        pbp_df["StartTime"],
        format="%Y%m%d%H%M"
    )
    pbp_df["game_date"] = pbp_df["game_date"].dt.tz_localize("Asia/Tokyo")
    # season = pd.DatetimeIndex(pbp_df["game_date"]).year
    pbp_df["season"] = pd.DatetimeIndex(pbp_df["game_date"]).year
    # season = pbp_df["season"].iloc[0]

    # roster_df = get_season_npb_rosters(season)
    # roster_df["player_name"] = roster_df["player_name"].str.replace(" ","")
    directory_url = "https://spaia.jp/baseball/npb/api/directory"

    if (
        exists("rosters/player_directory/directory.json")
    ):
        with open("rosters/player_directory/directory.json", "r") as f:
            json_str = f.read()
        player_directory = json.loads(json_str)
        del json_str
    else:
        player_directory = get_json_from_url(directory_url)
        # with open("rosters/player_directory/directory.json", "w+") as f:
        #     f.write(json.dumps(player_directory))

    del directory_url

    for p in player_directory:
        # p_name = p["PlayerName"]
        # p_name = p_name.replace(" ", "")
        # p_name = p_name.replace("　", "")
        # p_name = p_name.replace("\u3000", "")
        p_first_name = p["DelivFirstName"]
        p_last_name = p["DelivLastName"]
        p_name = f"{p_first_name}{p_last_name}"
        p_id = p["PersonInfoID"]
        p_id = int(p_id)

        player_mapper_arr[p_name] = p_id

        del p_first_name, p_last_name
        del p_id, p_name

    # r_name = roster_df["player_name"].to_list()
    # p_id = roster_df["person_id"].to_list()
    # player_mapper_arr = dict(
    #     zip(r_name, p_id)
    # )
    pbp_df.drop(
        columns=[
            "GameDate",
            "GameTime",
            "StartTime",
            "TB",
            "TextInfo_Bat_Text_No",
            "TextInfo_Bat_Text_Seq",
            "TextInfo_Bat_Text_F",
            "TextInfo_Bat_Text_Sec",
            "H_R",
            "H_H",
            "H_E",
            "H_Relief",
            "H_Homerun",
            "V_HV",
            # "V_ID",
            # "V_NameS",
            # "V_NameES",
            "V_R",
            "V_H",
            "V_E",
            "V_Relief",
            "V_Homerun",
        ],
        inplace=True,
    )
    pbp_df.rename(
        columns={
            "ID": "play_id",
            "GameID": "game_id",
            "Round": "game_round",
            "GameKindID": "game_type_id",
            "GameKindName": "game_type_name",
            "StadiumID": "stadium_id",
            "StadiumName": "stadium_name",
            "DoubleHeaderF": "is_double_header_finale",
            "Attendance": "game_attendance",
            "UmpireChief": "umpire_home",
            "UmpireFirst": "umpire_first",
            "UmpireSecond": "umpire_second",
            "UmpireThird": "umpire_third",
            "UmpireLeft": "umpire_left",
            "UmpireRight": "umpire_right",
            "GameStateID": "game_state_id",
            "Inning": "inning",
            "H_ID": "home_team_id",
            "H_NameS": "home_team_name",
            "H_NameES": "home_team_abv",
            "H_R": "home_total_runs",
            "V_ID": "away_team_id",
            "V_NameS": "away_team_name",
            "V_NameES": "away_team_abv",
            "V_R": "away_total_runs",
            "ResultID": "result_id",
            "EndTime": "end_time",
            "WinPitcher": "win_pitcher",
            "LosePitcher": "loss_pitcher",
            "SavePitcher": "save_pitcher",
            "TextInfo_ID": "game_state_id",
            "TextInfo_Name": "game_state_name",
            "TextInfo_Bat_No": "inning_ab_num",
            "TextInfo_Bat_Text": "description_jap",
        },
        inplace=True,
    )
    # print(pbp_df.columns)
    pbp_df = pbp_df.astype(
        {
            # "ID":"Int64",
            "game_id": "Int64",
            "game_round": "UInt8",
            "game_type_id": "UInt16",
            "game_type_name": "str",
            # "game_type_name": "str",
            "stadium_id": "UInt64",
            "stadium_name": "str",
            "is_double_header_finale": "UInt8",
            "game_attendance": "UInt32",
            "umpire_home": "str",
            "umpire_first": "str",
            "umpire_second": "str",
            "umpire_third": "str",
            "umpire_left": "str",
            "umpire_right": "str",
            # "game_state_id": "UInt8",
            "inning": "UInt8",
            "H_HV": "UInt8",
            "home_team_id": "UInt16",
            "home_team_name": "str",
            "home_team_abv": "str",
            "away_team_id": "UInt16",
            "away_team_name": "str",
            "away_team_abv": "str",
            "result_id": "str",
            "end_time": "str",
            "win_pitcher": "str",
            "loss_pitcher": "str",
            "save_pitcher": "str",
            "game_state_id": "UInt16",
            "game_state_name": "str",
            "inning_ab_num": "UInt8",
            "description_jap": "str",
            # "description": "str",
            "PlayInfo_SeqNo": "str",
            "PlayInfo_AB": "str",
            "PlayInfo_PlayerID": "str",
            "PlayInfo_PlayerName": "str",
            "page": "str",
            "atBatBallCount": "Int16",
            "UpdatedAt": "datetime64[ms, UTC]",
            "CreatedAt": "datetime64[ms, UTC]",
        }
    )

    pitch_box_location_json = get_json_from_url(pitch_box_location_url)
    pitch_location_df = pd.json_normalize(pitch_box_location_json)

    pitch_location_df = pitch_location_df.astype(
        {
            "ID": "Int64",
            "gameId": "Int64",
            "atBatBallCount": "Int16",
            "ballSpeed": "Int16",
            "ballKind": "Int16",
            "x": "Int16",
            "y": "Int16",
            "presult": "Int16",
            "bresult": "Int16",
            "pitId": "Int64",
            "pitLR": "Int16",
            "batId": "Int64",
            "batLR": "Int16",
            "battedX": "Int16",
            "battedY": "Int16",
            "ballCatcherId": "Int64",
            "ballCatcherName": "str",
            "ballCatcherPositionId": "Int8",
            "ballCatcherNum": "Int16",
            "addedRuns": "Int8",
            "UpdatedAt": "datetime64[ms, UTC]",
            "CreatedAt": "datetime64[ms, UTC]",
        }
    )
    pitch_location_df["page"] = pitch_location_df[
        "fiveDigitSerialNumber"
    ] + pitch_location_df[
        "atBatBallCount"
    ].astype("str").str.pad(2, fillchar="0")

    pitch_location_df["pitcher_hand"] = pitch_location_df[
        "pitLR"
    ].map(convert_arm_id)
    pitch_location_df["batter_hand"] = pitch_location_df[
        "batLR"
    ].map(convert_arm_id)
    pitch_location_df.rename(
        columns={
            "gameId": "game_id",
            "atBatBallCount": "pitch_number",
            "ballSpeed": "release_speed_kmh",
            "ballKind": "pitch_id",
            "x": "plate_x",
            "y": "plate_y",
            "pitId": "pitcher",
            "batId": "batter",
            "battedX": "hc_x",
            "battedY": "hc_y",
            "ballCatcherId": "fielder",
            "ballCatcherName": "fielder_name",
            "ballCatcherPositionId": "hit_location",
        },
        inplace=True,
    )

    pitch_location_df.loc[
        pitch_location_df["release_speed_kmh"] < 1,
        "release_speed_kmh"
    ] = (
        None
    )
    pitch_location_df["release_speed_mph"] = (
        pitch_location_df["release_speed_kmh"] / 1.609
    )
    pitch_location_df.loc[pitch_location_df["pitch_id"] < 1, "pitch_id"] = None
    pitch_location_df.loc[pitch_location_df["plate_x"] < 0, "plate_x"] = None
    pitch_location_df.loc[pitch_location_df["plate_y"] < 0, "plate_y"] = None
    pitch_location_df.loc[pitch_location_df["hc_x"] < 0, "hc_x"] = None
    pitch_location_df.loc[pitch_location_df["hc_y"] < 0, "hc_y"] = None
    pitch_location_df.loc[pitch_location_df["fielder"] < 0, "fielder"] = None
    pitch_location_df.loc[
        pitch_location_df["hit_location"] < 0,
        "hit_location"
    ] = None
    pitch_location_df.drop(
        columns=["ID", "UpdatedAt", "CreatedAt", "batLR", "pitLR"],
        inplace=True
    )
    pbp_df = pbp_df.merge(
        right=pitch_location_df,
        on=["game_id", "page"],
        how="left"
    )

    strike_ball_count_json = get_json_from_url(strike_ball_count_url)
    strike_ball_count_df = pd.json_normalize(strike_ball_count_json)

    strike_ball_count_df.rename(
        columns={
            "gameId": "game_id",
            "strike": "strikes",
            "ball": "balls",
            "out": "outs_when_up",
        },
        inplace=True,
    )
    strike_ball_count_df.drop(
        columns=["ID", "timingId", "UpdatedAt", "CreatedAt"], inplace=True
    )
    strike_ball_count_df = strike_ball_count_df.astype(
        {
            "game_id": "UInt64",
            "page": "str",
            "strikes": "UInt8",
            "balls": "UInt8",
            "outs_when_up": "UInt8",
        }
    )
    pbp_df = pbp_df.merge(
        right=strike_ball_count_df, on=["game_id", "page"], how="left"
    )

    on_base_json = get_json_from_url(on_base_url)
    on_base_df = pd.json_normalize(on_base_json)

    on_base_df.drop(
        columns=["ID", "timingId", "UpdatedAt", "CreatedAt"],
        inplace=True
    )
    on_base_df.rename(
        columns={
            "gameId": "game_id",
            "firstRunnnerName": "on_1b_name",
            "secondRunnnerName": "on_2b_name",
            "thirdRunnnerName": "on_3b_name",
        },
        inplace=True,
    )
    on_base_df = on_base_df.astype(
        {
            "game_id": "UInt64",
            "on_1b_name": "str",
            "on_2b_name": "str",
            "on_3b_name": "str",
        }
    )

    pbp_df = pbp_df.merge(right=on_base_df, on=["game_id", "page"], how="left")

    fielders_json = get_json_from_url(fielders_url)
    fielders_df = pd.json_normalize(fielders_json)

    fielders_df.drop(
        columns=["ID", "timingId", "UpdatedAt", "CreatedAt", "dhPlayerName"],
        inplace=True,
    )
    fielders_df.rename(
        columns={
            "gameId": "game_id",
            "pitcherPlayerPlayerName": "fielder_1_name",
            "catcherPlayerName": "fielder_2_name",
            "firstPlayerName": "fielder_3_name",
            "secondPlayerName": "fielder_4_name",
            "thirdPlayerName": "fielder_5_name",
            "shortPlayerName": "fielder_6_name",
            "leftPlayerName": "fielder_7_name",
            "centerPlayerName": "fielder_8_name",
            "rightPlayerName": "fielder_9_name",
        },
        inplace=True,
    )
    fielders_df = fielders_df.astype(
        {
            "game_id": "UInt64",
            "fielder_1_name": "str",
            "fielder_2_name": "str",
            "fielder_3_name": "str",
            "fielder_4_name": "str",
            "fielder_5_name": "str",
            "fielder_6_name": "str",
            "fielder_7_name": "str",
            "fielder_8_name": "str",
            "fielder_9_name": "str",
        }
    )
    pbp_df = pbp_df.merge(
        right=fielders_df,
        on=["game_id", "page"],
        how="left"
    )
    # pbp_df["description"] = pbp_df["description_jap"].map(translate_stuff)
    pbp_df.drop(columns=["game_state_id"], inplace=True)

    for c in pbp_df.columns:
        if c not in stats_columns:
            raise IndexError(f"Unhandled column `{c}`")
    pbp_df = pbp_df.reindex(columns=stats_columns)
    pbp_df["description"] = pbp_df["description_jap"].map(translate_stuff)

    del pitch_box_location_json
    del strike_ball_count_json
    del on_base_json
    del fielders_json

    del pitch_location_df
    del strike_ball_count_df
    del on_base_df
    del fielders_df

    # player ID mapper
    pbp_df["on_1b"] = pbp_df["on_1b_name"].map(player_mapper_arr)
    pbp_df["on_2b"] = pbp_df["on_2b_name"].map(player_mapper_arr)
    pbp_df["on_3b"] = pbp_df["on_3b_name"].map(player_mapper_arr)
    pbp_df.loc[pbp_df["on_1b_name"] == "", "on_1b_name"] = None
    pbp_df.loc[pbp_df["on_2b_name"] == "", "on_2b_name"] = None
    pbp_df.loc[pbp_df["on_3b_name"] == "", "on_3b_name"] = None

    pbp_df["fielder_1"] = pbp_df["fielder_1_name"].map(player_mapper_arr)
    pbp_df["fielder_2"] = pbp_df["fielder_2_name"].map(player_mapper_arr)
    pbp_df["fielder_3"] = pbp_df["fielder_3_name"].map(player_mapper_arr)
    pbp_df["fielder_4"] = pbp_df["fielder_4_name"].map(player_mapper_arr)
    pbp_df["fielder_5"] = pbp_df["fielder_5_name"].map(player_mapper_arr)
    pbp_df["fielder_6"] = pbp_df["fielder_6_name"].map(player_mapper_arr)
    pbp_df["fielder_7"] = pbp_df["fielder_7_name"].map(player_mapper_arr)
    pbp_df["fielder_8"] = pbp_df["fielder_8_name"].map(player_mapper_arr)
    pbp_df["fielder_9"] = pbp_df["fielder_9_name"].map(player_mapper_arr)

    pbp_df = pbp_df.astype(
        {
            "on_1b": "UInt64",
            "on_2b": "UInt64",
            "on_3b": "UInt64",
            "fielder_1": "UInt64",
            "fielder_2": "UInt64",
            "fielder_3": "UInt64",
            "fielder_4": "UInt64",
            "fielder_5": "UInt64",
            "fielder_6": "UInt64",
            "fielder_7": "UInt64",
            "fielder_8": "UInt64",
            "fielder_9": "UInt64"
        }
    )

    pbp_df.to_csv(f"pbp/individual_games/{game_id}.csv", index=False)
    return pbp_df


def get_npb_pbp_by_season(season: int, month: int = None):
    """ """
    pbp_df = pd.DataFrame()
    pbp_df_arr = []
    game_df = pd.DataFrame()
    now = datetime.now()
    try:
        mkdir("pbp/individual_games")
    except FileExistsError:
        logging.info("`pbp/individual_games` already exists")
    except Exception as e:
        raise e

    logging.info("Getting the NPB schedule for the %s season.", season)

    sched_df = get_npb_schedule(season=season)
    sched_df = sched_df.sample(frac=1)
    sched_df = sched_df[
        (sched_df["home_score"] > 0) |
        (sched_df["away_score"] > 0)
    ]

    game_ids_arr = sched_df["game_id"].to_numpy()

    sched_df["month"] = pd.DatetimeIndex(sched_df["game_date"]).month

    if month is not None:
        sched_df = sched_df[sched_df["month"] == month]

    month_arr = list(set(sched_df["month"].to_list()))
    for m in month_arr:
        pbp_df_arr = []

        temp_df = sched_df[sched_df["month"] == m]
        game_ids_arr = temp_df["game_id"].to_numpy()

        print(f"Getting {season}-{m:02} NPB PBP data")

        del temp_df

        for game_id in tqdm(game_ids_arr):

            game_df = get_npb_pbp_by_game(game_id=game_id)
            pbp_df_arr.append(game_df)
            # time.sleep(1)
            # pbp_df = pd.concat([pbp_df,game_df],ignore_index=True)
            del game_df

        # If there's nothing here, there's nothing to save.
        if len(pbp_df_arr) > 0:
            pbp_df = pd.concat(pbp_df_arr, ignore_index=True)
            pbp_df["last_updated"] = now.isoformat()
            pbp_df.to_csv(f"pbp/{season}-{m:02}_pbp.csv", index=False)
        else:
            pass

    # return pbp_df


if __name__ == "__main__":
    now = datetime.now()

    f_year = now.year - 2
    c_year = now.year + 1

    # # print("Getting NPB Standings data.")
    # for i in range(2026, c_year):
    #     get_npb_pbp_by_season(season=i)
    #     time.sleep(1)

    # If first or second day of the month,
    # get the previous month's PBP data
    if now.day <= 2:
        get_npb_pbp_by_season(
            season=now.year,
            month=(now.month - 1)
        )

    get_npb_pbp_by_season(
        season=now.year,
        month=now.month
    )
