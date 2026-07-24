# Nippon-Baseball-Data-Repository

Holds public data for the Nippon Professional Baseball (NPB) League, a professional baseball league based in Japan.

## Data

This repository will consistently refresh
Data is housed in individual releases due to ease of use, and can be accessed below.
Most of the data for this repository is largely sourced from [SPAIA](https://spaia.jp/), a Japanese sports website that just happens to have a treasure trove of NPB stats and information.

## Data Endpoints

| Data point | Release | Job Status |
| ---- | ---- | ---- |
| Player Game Stats  | [Player Game Stats](https://github.com/armstjc/Nippon-Baseball-Data-Repository/releases/tag/player_game_stats) | [![Update NPB Game Stats](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_game_stats.yml/badge.svg)](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_game_stats.yml)            |
| Play-by-play (PBP) | [PBP](https://github.com/armstjc/Nippon-Baseball-Data-Repository/releases/tag/pbp)                             | [![Update NPB PBP](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_pbp.yml/badge.svg)](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_pbp.yml)                                 |
| Rosters            | [NPB Rosters](https://github.com/armstjc/Nippon-Baseball-Data-Repository/releases/tag/rosters)                 | [![Update NPB Rosters](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_rosters.yml/badge.svg)](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_rosters.yml)                     |
| Schedules          | [Schedule](https://github.com/armstjc/Nippon-Baseball-Data-Repository/releases/tag/schedule)                   | [![Update NPB Schedules and Standings](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_schedules.yml/badge.svg)](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_schedules.yml) |
| Schedules          | [Game_Standings](https://github.com/armstjc/Nippon-Baseball-Data-Repository/releases/tag/game_standings)       | [![Update NPB Schedules and Standings](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_schedules.yml/badge.svg)](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_schedules.yml) |
| NPB Draft          | [NPB Draft](https://github.com/armstjc/Nippon-Baseball-Data-Repository/releases/tag/draft)                     | [![Update NPB Schedules and Standings](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_schedules.yml/badge.svg)](https://github.com/armstjc/Nippon-Baseball-Data-Repository/actions/workflows/get_npb_schedules.yml) |

## Why releases over just comminting to the repository?

GitHub (and by extension most Git implementations) struggles to properly handle changes to binary files, and changes to large (25+ MB) files if you're constantly making changes to files.

If you want a more in-depth explanation, [@tanho63](https://github.com/tanho63)'s _Project Immortality: Using GitHub To Make Your Work Live Forever_ talk during Posit (2022) goes a bit more into detail about some of the technical reasons why this is the case.

<iframe width="560" height="315" src="https://www.youtube.com/embed/wzcz4xNGeTI?si=FhkQbiNGhFuEqvRg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## How to contribute
If you would like for a feature to be added, or for a bug to be fixed [you can open an issue](https://github.com/armstjc/Nippon-Baseball-Data-Repository/issues) so that it can be put under consideration.
If you would like to contribute data or code to this project, [please create a pull request](https://github.com/armstjc/Nippon-Baseball-Data-Repository/pulls). If everything with the request is good, I'll make the best effort possible to include that pull into this repo.


## Liscensing

The code within this repository is governed by the MIT liscense, [Wikipedia](https://en.wikipedia.org/wiki/MIT_License) has a very good writeup on the basics of the MIT liscense if you want to learn more.

If you wish to use the data of this repository,
the only thing we would like to ask is for you to please include the following text in a way where any user can see it:

```
This uses data sourced from the Nippon Baseball Data Repository, which can be accessed here:

https://github.com/armstjc/Nippon-Baseball-Data-Repository
```

And if you need to cite this repo for academic work, here is how to cite the repo for APA:

```
Armstrong, Joseph (2026). Nippon Baseball Data Repository (Main Branch) [Computer software].
https://github.com/armstjc/Nippon-Baseball-Data-Repository/tree/main
```