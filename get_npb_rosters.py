from datetime import datetime
import logging
import time
from os import mkdir
from os.path import exists

import cutlet
import pandas as pd
from tqdm import tqdm

from utls import get_json_from_url, team_ids_list


def get_npb_team_roster(team_id: int, season: int) -> pd.DataFrame:
    """ """
    katsu = cutlet.Cutlet()

    def translate_stuff(input_str: str) -> str:
        """ """
        return katsu.romaji(input_str, title=True)

    roster_df = pd.DataFrame()
    roster_url = (
        "https://spaia.jp/baseball/npb/api/players_by_team?" +
        f"team_id={team_id}&year={season}"
    )

    if exists(f"rosters/individual_rosters/{season}_{team_id}.csv"):
        df = pd.read_csv(f"rosters/individual_rosters/{season}_{team_id}.csv")
        return df

    time.sleep(1)
    logging.info("Getting Roster data for team ID #%s.", team_id)

    roster_json = get_json_from_url(roster_url)

    roster_df = pd.json_normalize(roster_json)
    roster_df.rename(
        columns={
            "PersonInfoID": "person_id",
            "PlayerName":   "player_name",
            "PlayerNameK":  "player_name_kanji",
            "BackNumber":   "player_jersey_number",
            "TeamID":       "team_id",
            "TeamName":     "team_name",
            "PositionType": "position_type_id",
            "RosterName":   "roster_name",
            "StaffKind":    "staff_kind_id",
            "StaffTitle":   "staff_title",
            "AnnounceDate": "announce_date",
            "MovementID": "movement_id",
            "MovementName": "movement_name",
        },
        inplace=True
    )
    roster_df["season"] = season
    roster_df["player_name_romaji"] = roster_df["player_name"].map(
        translate_stuff
    )
    roster_df = roster_df.astype(
        {
            "season": "UInt16",
            "person_id": "UInt64",
            "player_name": "str",
            "player_name_kanji": "str",
            "player_jersey_number": "str",
            "team_id": "Int32",
            "team_name": "str",
            "position_type_id": "Int8",
            "roster_name": "str",
            "staff_kind_id": "UInt32",
            "staff_title": "str",
            "announce_date": "str",
            "movement_id": "UInt32",
            "movement_name": "str",
            "order_id": "UInt8"
        }
    )
    roster_df.to_csv(
        f"rosters/individual_rosters/{season}_{team_id}.csv",
        index=False
    )
    return roster_df


def get_season_npb_rosters(season: int):
    """ """
    # now = datetime.now()
    roster_df = pd.DataFrame()
    roster_df_arr = []
    temp_df = pd.DataFrame()
    team_ids_arr = team_ids_list()

    try:
        mkdir("rosters/individual_rosters")
    except FileExistsError:
        logging.info("`pbp/individual_rosters` already exists")
    except Exception as e:
        raise e

    if (
        exists(f"rosters/{season}_npb_rosters.parquet")
    ):
        df = pd.read_parquet(f"rosters/{season}_npb_rosters.parquet")
        return df

    for team_abv, team_id in tqdm(team_ids_arr.items()):

        temp_df = get_npb_team_roster(season=season, team_id=team_id)
        roster_df_arr.append(temp_df)
        del temp_df

    roster_df = pd.concat(roster_df_arr, ignore_index=True)

    roster_df["player_name"] = roster_df[
        "player_name"
    ].str.replace("　", " ")

    roster_df["player_name"] = roster_df[
        "player_name"
    ].str.replace("\u3000", "")

    roster_df["player_name_kanji"] = roster_df[
        "player_name_kanji"
    ].str.replace("　", "")

    roster_df["player_name_kanji"] = roster_df[
        "player_name_kanji"
    ].str.replace("\u3000", "")

    roster_df["player_jersey_number"] = roster_df[
        "player_jersey_number"
    ].astype("str")

    roster_df.to_csv(
        f"rosters/{season}_npb_rosters.csv",
        index=False
    )

    roster_df.to_parquet(
        f"rosters/{season}_npb_rosters.parquet",
        index=False
    )
    return roster_df


def main():
    """ """
    now = datetime.now()
    for i in range(2026, 2017, -1):
        get_season_npb_rosters(i)
    # get_season_npb_rosters(now.year)


if __name__ == "__main__":
    main()
