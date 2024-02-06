import json
import logging
import os
import pandas as pd
from tqdm import tqdm
from utls import (
    get_json_from_url,
    convert_numeric,
    get_latest_season_year,
    team_ids_list,
)

logging.basicConfig(level=logging.WARNING)


def get_ids_from_pa(team_id: int, pa: int, find_batter: bool = True) -> list[str]:
    "get a list of ids of players in a team with plate appearance >= pa"
    logging.info("Get list of ids")

    id_list = []

    player_type = "batter" if find_batter else "pitcher"
    latest_season = get_latest_season_year()

    url = f"https://spaia.jp/baseball/npb/api/{player_type}_list?team={team_id}&year={latest_season}"
    players_json = get_json_from_url(url)
    for player in players_json:
        player_pa = player.get("PlateAppearance")
        try:
            if player_pa and int(player_pa) >= pa:
                id_list.append(player["PlayerCD"])
        except:
            print(player.get("Name"), player_pa)

    return id_list


def get_player_stats(id_list: list[str], save_path: str):
    "get player's data for all available seasons"
    logging.info("Get player stats")

    metrics = [
        "TeamCD",
        "BattingAverage",
        "Game",
        "PlateAppearance",
        "AtBat",
        "Run",
        "Hit",
        "Double",
        "Triple",
        "Homerun",
        "Base",
        "RunsBattingIn",
        "StrikeOut",
        "BaseOnBall",
        "HitByPitch",
        "SacrificeHit",
        "SacrificeFly",
        "StolenBase",
        "CaughtStealing",
        "DoublePlay",
        "Error",
        "Slugging",
        "OnBase",
        "Ops",
    ]

    organized_data = {}

    for player_id in id_list:
        url = f"https://spaia.jp/baseball/npb/api/hitting_stats_by_year?player_id={player_id}"
        json_data = get_json_from_url(url)
        player_dict = {"name": json_data[0]["Name"], "stats": {}}

        for seasonal_stat in json_data:
            stats = {}
            for metric in metrics:
                val = seasonal_stat[metric]
                if "ID" in metric or "CD" in metric:
                    stats[metric] = val
                elif val == "-":
                    stats[metric] = None
                else:
                    stats[metric] = convert_numeric(val)
            player_dict["stats"][seasonal_stat["Year"]] = stats

        organized_data[player_id] = player_dict

    logging.info("Data extracted")

    if save_path:  # save if save_path is non-empty
        with open(save_path, "w") as json_file:
            json.dump(organized_data, json_file, indent=4)


if __name__ == "__main__":
    team_ids = team_ids_list()

    for team_name, team_id in tqdm(team_ids.items()):
        logging.info(f"===== {team_name} ======")
        player_ids = get_ids_from_pa(team_id, 100)
        get_player_stats(player_ids, f"player_stats/{team_name}.json")
