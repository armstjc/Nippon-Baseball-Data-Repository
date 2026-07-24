"""
Original idea for this came from
[annatakegawa](https://github.com/annatakegawa),
and
[from her fork](
https://github.com/annatakegawa/NPB-data-analysis/blob/main/data_collection/get_salary_data.py
).
"""

from datetime import datetime
import json
import os
from os.path import exists

import pandas as pd
import requests
from bs4 import BeautifulSoup

from utls import get_json_from_url


# combined into function
def create_team_dict() -> dict:
    """
    Original idea for this came from
    [annatakegawa](https://github.com/annatakegawa),
    and
[from her fork](
https://github.com/annatakegawa/NPB-data-analysis/blob/main/data_collection/get_salary_data.py).

    Creates a team dictionary that can be used
    to help identify teams in the NPB.
    """
    url = 'https://sp.baseball.findfriends.jp/?pid=db'
    player_page = requests.get(url)
    player_soup = BeautifulSoup(player_page.content, 'html.parser')
    team_ul_elements = player_soup.find_all('ul', class_='db_team_select_box')

    team_dict = {}

    for team_ul in team_ul_elements:
        league_name = team_ul.find('li').text.strip()
        team_links = [a['href'] for a in team_ul.find_all('a')]
        team_names = [a.text for a in team_ul.find_all('a')]

        for link, name in zip(team_links, team_names):
            team_dict[name] = {
                'url': link,
                'league': 'C' if league_name == 'セ･リーグ' else 'P'
            }

    return team_dict


def create_player_data_df(url: str, team_name: str) -> pd.DataFrame:
    """
    Original idea for this came from
    [annatakegawa](https://github.com/annatakegawa),
    and
[from her fork](
https://github.com/annatakegawa/NPB-data-analysis/blob/main/data_collection/get_salary_data.py).

    Gets a list of NPB players and returns the result as a pandas `DataFrame`.

    """

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='ResultTable02b')

    # get titles
    thead = table.find('thead')
    title_elements = thead.find_all('th')
    titles = [title.text.strip().replace('｜', 'ー') for title in title_elements]
    df = pd.DataFrame(columns=titles)

    # add rows
    tbody = table.find('tbody')
    column_data = tbody.find_all('tr')
    for row in column_data:
        row_data = row.find_all(['th', 'td'])
        individual_row_data = [data.text.strip() for data in row_data]
        # print(individual_row_data)
        length = len(df)
        df.loc[length] = individual_row_data

    # convert numeric columns' data types
    num_cols = df.columns[2:]
    df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')
    df['チーム'] = team_name

    df.rename(
        columns={
            "背番号": "player_jersey_number",
            "名前": "player_name_jap",
            "年俸": "player_salary",
            "チーム": "Team",
            "防御率": "pitching_ERA",
            "試合数": "total_games",
            "勝利": "pitching_W",
            "敗戦": "pitching_L",
            "投球回数": "pitching_IP",
            "勝率": "pitching_W%",
            "完投": "pitching_CG",
            "完封": "pitching_SHO",
            "セーブ": "pitching_SV",
            "ホールド": "pitching_H",
            "奪三振": "pitching_SO",
            "奪三振率": "pitching_SO%",
            "失点": "pitching_R",
            "自責点": "pitching_ER",
            "被安打": "pitching_H",
            "被本塁打": "pitching_HR",
            "与四球": "pitching_BB",
            "与死球": "pitching_HBP",
            "与四球率": "pitching_BB%",
            "打率": "bating_AVG",
            "打席数": "batting_PA",
            "打数": "batting_AB",
            "安打": "batting_H",
            "二塁打": "batting_2B",
            "三塁打": "batting_3B",
            "本塁打": "batting_HR",
            "塁打数": "batting_TB",
            "得点": "batting_R",
            "打点": "batting_RBI",
            "三振": "batting_SO",
            "四球": "batting_BB",
            "死球": "batting_HBP",
            "盗塁": "batting_SB",
            "出塁率": "batting_OBP",
            "長打率": "batting_SLG",
            "OPS": "batting_OPS",
            "三振率": "batting_SO%",
        },
        inplace=True,
    )

    return df


def get_salary(team_dict: dict, year: int, position: str):
    """
    Original idea for this came from
    [annatakegawa](https://github.com/annatakegawa),
    and
[from her fork](
https://github.com/annatakegawa/NPB-data-analysis/blob/main/data_collection/get_salary_data.py).

    From a given list of NPB players,
    get their salaries in a given year,
    and return the result as a pandas `DataFrame`.

    """

    team_dfs = []
    player_mapper_arr = {}

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

    for team_name, team_info in team_dict.items():
        team_url = team_info['url']
        url = f'https://sp.baseball.findfriends.jp{team_url}{year}/{position}/'
        team_data = create_player_data_df(url, team_name)
        team_dfs.append(team_data)
    combined_df = pd.concat(team_dfs, ignore_index=True)

    # Yes, this website chose to do "Salary (in 10K Yen)".
    # Fix that here so it's clearer exactly how much yen someone's
    # getting paid.
    combined_df["player_salary"] = combined_df["player_salary"] * 10000
    combined_df["player_id"] = combined_df[
        "player_name_jap"
    ].map(player_mapper_arr)
    combined_df["player_id"] = combined_df["player_id"].astype("UInt64")

    save_path = os.path.join('salaries/', f'{year}_{position}.csv')
    combined_df.to_csv(save_path, index=False)


if __name__ == '__main__':
    team_dict = create_team_dict()
    now = datetime.now()
    for year in range(now.year, now.year + 1):
        print('--- Getting batter data for', year, ' ---')
        get_salary(team_dict, year, 'batter')
        print('--- Getting pitcher data for', year, ' ---')
        get_salary(team_dict, year, 'pitcher')
