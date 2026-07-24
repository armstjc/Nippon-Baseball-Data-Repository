from datetime import datetime
import logging
from os.path import exists
from random import shuffle
import pandas as pd
from tqdm import tqdm

from utls import get_json_from_url


def get_npb_draft_results(season: int) -> pd.DataFrame:
    """ """
    now = datetime.now()
    if exists(f"npb_draft/{season}_npb_draft.csv"):
        data_df = pd.read_csv(f"npb_draft/{season}_npb_draft.csv")
        return data_df

    url = f"https://spaia.jp/baseball/npb/api/past_draft_players?year={season}"
    draft_json = get_json_from_url(url=url)
    if len(draft_json) == 0:
        # if we're in this state, its because the data doesn't exist,
        # or there's something weird with your setup.
        # Let's try a diffrient season if that's the case,
        # and then fail hard.
        logging.warning(
            f"Cannot find draft data for {season}. " +
            "We'll try to see if we can get another draft year instead."
        )
        seasons_arr = [x for x in range(2004, now.year)]
        shuffle(seasons_arr)
        season = seasons_arr[-1]
        logging.warning(
            f"Let's see if we can get the {season} NPB draft instead."
        )
        url = f"https://spaia.jp/baseball/npb/api/past_draft_players?year={season}"
        draft_json = get_json_from_url(url=url)

    data_df = pd.json_normalize(data=draft_json)

    data_df.rename(
        columns={
            "ID": "draft_entry_id",
            "Year": "season",
            "TeamID": "team_id",
            "TeamNameS": "team_name",
            "MtgAssortmentID": "mtg_assortment_id",
            "MtgAssortment": "mtg_assortment",
            "NominateID": "nominate_id",
            "ConvertedNominateID": "converted_nominate_id",
            "NominateCount": "nomination_count",
            "NominateSituationID": "nomination_situation_id",
            "PlayerID": "player_id",
            "DraftPlayerID": "draft_player_id",
            "PlayerName": "player_name_jap",
            "Profile": "previous_school",
            "ProfileDivision": "school_division",
            "ConvertedProfileDivision": "converted_school_division",
            "PositionID": "position_id",
            "PersonInfoID": "person_info_id",
            "CurrentTeamID": "current_team_id",
            "CurrentTeamNameS": "current_team_name_jap"
        },
        inplace=True
    )
    data_df = data_df.astype(
        {
            "draft_entry_id": "UInt64",
            "season": "UInt16",
            "team_id": "UInt64",
            "team_name": "str",
            "mtg_assortment_id": "UInt32",
            "mtg_assortment": "str",
            "nominate_id": "UInt32",
            "converted_nominate_id": "UInt32",
            "nomination_count": "UInt8",
            "nomination_situation_id": "UInt8",
            "player_id": "UInt64",
            "draft_player_id": "UInt64",
            "player_name_jap": "str",
            "previous_school": "str",
            "school_division": "UInt8",
            "converted_school_division": "UInt8",
            "position_id": "UInt8",
            "has_player_page_link": "bool[pyarrow]",
            "person_info_id": "UInt64",
            "has_draft_page_link": "bool[pyarrow]",
            "player_kind": "UInt8",
            "playing_division": "UInt8",
            "current_team_id": "UInt64",
            "current_team_name_jap": "str",
            "kyodo_id": "str"
        }
    )
    data_df["updated_at"] = now.isoformat()
    data_df.to_csv(f"npb_draft/{season}_npb_draft.csv", index=False)
    data_df.to_parquet(f"npb_draft/{season}_npb_draft.parquet", index=False)
    return data_df


def main():
    """ """
    now = datetime.now()

    # for season in tqdm(range(2004, now.year)):
    #     # print(get_npb_draft_results(2020))
    #     get_npb_draft_results(season)

    # get_npb_draft_results(2012)

    get_npb_draft_results(now.year - 1)
    get_npb_draft_results(now.year)


if __name__ == "__main__":
    main()
