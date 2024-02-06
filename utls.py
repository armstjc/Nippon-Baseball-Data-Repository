from datetime import datetime
import requests


def get_json_from_url(url: str):
    """ """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pass
    elif response.status_code == 401:
        raise ConnectionRefusedError(
            f"Could not connect. The connection was refused.\nHTTP Status Code 401."
        )
    else:
        raise ConnectionError(
            f"Could not connect.\nHTTP Status code {response.status_code}"
        )

    json_data = response.json()

    return json_data


def convert_numeric(value: str):
    if "." in value:
        try:
            return float(value)
        except ValueError as e:
            print(f"Error: {e}")
    else:
        try:
            return int(value)
        except ValueError as e:
            print(f"Error: {e}")


def get_latest_season_year():
    curr_date = datetime.now()
    curr_month = curr_date.month

    season_start_month = 3
    season_end_month = 10

    latest_season_year = (
        curr_date.year if curr_month >= season_start_month else curr_date.year - 1
    )

    return latest_season_year


def team_ids_list():
    team_ids = {
        "巨人": 1,  # Yomiuri Giants
        "ヤクルト": 2,  # Tokyo YakultSwallows
        "DeNA": 3,  # Yokohama DeNA Bay Stars
        "中日": 4,  # Chunichi Dragons
        "阪神": 5,  # Hanshin Tigers
        "広島": 6,  # Hiroshima Toyo Carp
        "西武": 7,  # Saitama Seibu Lions
        "日本ハム": 8,  # Hokkaido Nippon-Ham Fighters
        "ロッテ": 9,  # Chiba Lotte Marines
        "オリックス": 11,  # Orix Buffaloes
        "ソフトバンク": 12,  # Fukuoka SoftBank Hawks
        "楽天": 376,  # Tohoku Rakuten Golden Eagles
    }
    return team_ids
