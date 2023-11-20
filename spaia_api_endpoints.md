# SPAIA NPB API endpoints

# Players

## Player info
Base: https://spaia.jp/baseball/npb/api/player_by_team?person_info_id=1400101

## Career Hitting Stats 
Base: https://spaia.jp/baseball/npb/api/hitting_stats_career
- Filter by team = `?teamId=2`
- Filter by player = `playerId=700094`

## Season Hitting Stats
Base: https://spaia.jp/baseball/npb/api/hitting_stats_by_year?player_id=1400101
- Must specify a player ID

## Monthly Hitting Stats
Base: https://spaia.jp/baseball/npb/api/hitting_stats_by_month?player_id=1400101&year=2023

## Player Game Hitting Stats
Base: https://spaia.jp/baseball/npb/api/hitting_stats_by_game?player_id=1400101&year=2022
- Filter by team = `&team_id=1`

## Player Pitching Sabermetric Stats (season)
Base: https://spaia.jp/baseball/npb/api/player_pitching_detail_saber?year=2023&order_by=EarnedRunAverage&is_desc=1&teams=1,2,3,4,5,6,7,8,9,11,12,376

## Player Batting Sabermetric Stats (season)
Base: https://spaia.jp/baseball/npb/api/player_batting_detail_saber?year=2023&order_by=BattingAverage&is_desc=1&teams=1,2,3,4,5,6,7,8,9,11,12,376

## Player Directory
Base: https://spaia.jp/baseball/npb/api/directory

## Similar Players
Base: https://spaia.jp/baseball/npb/api/related_players?player_id=1400101

## Same Draft Year
Base: https://spaia.jp/baseball/npb/api/same_draft_year_players?player_id=1400101

# Schedule (done)

## Upcomming Games
Base: https://spaia.jp/baseball/npb/api/game_schedule

## Games on the Same Date
Base: https://spaia.jp/baseball/npb/api/games_info_by_date?gameDate=20231018

## Weekly Schedule
Base: https://spaia.jp/baseball/npb/api/weekly_schedule?from=20231022&to=20231028

## Monthly Schedule
Base: https://spaia.jp/baseball/npb/api/game_calendar?year=2023&month=05

## Season Schedule
Base: https://spaia.jp/baseball/npb/api/schedules?Year=2023

# Standings

## By Game
Base: https://spaia.jp/baseball/npb/api/official_stats_history?GameAssortment=1&Year=2023
- NOTE: 
    - `GameAssortment=1` = Central League
    - `GameAssortment=2` = Pacific League

# Teams

## Full Team Rosters
Base: https://spaia.jp/baseball/npb/api/directory?TeamID=2&year=2023

## Batters
Base: https://spaia.jp/baseball/npb/api/batter_list?team=2&year=2023

## Pitchers
Base: https://spaia.jp/baseball/npb/api/pitcher_list?team=2&year=2023

## Coaching Staff
Base: https://spaia.jp/baseball/npb/api/staff_list?team=2&year=2023

## Full System: 
Base: https://spaia.jp/baseball/npb/api/players_by_team?team_id=2&year=2023

# NPB Draft

## Draft order
Base: https://spaia.jp/baseball/npb/api/team_rank_by_year?year=2023

## Current Draft Pool
Base: https://spaia.jp/baseball/npb/api/draft_info

## Past NPB Drafts
Base: https://spaia.jp/baseball/npb/api/past_draft_players?year=2022

# Games

## Current Game Info
Base: https://spaia.jp/baseball/npb/api/live_games?GameID=2021014362

## Post-Game Info
Base: https://spaia.jp/baseball/npb/api/game_over_view?gameId=2021014362

## Pre-Game Odds
Base: https://spaia.jp/baseball/npb/api/prediction_game?GameID=2021014362

## Current Score
Base: https://spaia.jp/baseball/npb/api/current_score?game_id=2021014362

## Starting Lineups
Base: https://spaia.jp/baseball/npb/api/starting_members_for_flash?gameId=2021014362

## Pitch-by-picth data
Base: https://spaia.jp/baseball/npb/api/flash_atbat_history?gameId=2021014362

## Play-by-play data
Base: https://spaia.jp/baseball/npb/api/game_text_pbp?GameID=2021014362

## Batting Stats - Player Game
Base: https://spaia.jp/baseball/npb/api/both_batter_stats?gameId=2021014362&matchday=20231018

## Pitching Stats - Player Game
Base: https://spaia.jp/baseball/npb/api/both_pitcher_game_stats?gameId=2021014362&matchday=20231018

