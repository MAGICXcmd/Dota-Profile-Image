import json

import requests
from datetime import datetime

from pathlib import Path
from steam.steamid import SteamID

BASE_DIR = Path(__file__).resolve().parent.parent


class SteamID32:
    @classmethod
    def get_steamid32(cls, link: str):
        steamid32 = SteamID.from_url(link).as_32
        return steamid32


class Parse:
    def __init__(self, userid):
        self.userid = userid
        self.userinfo = self.__get_profile_info(userid)

    def __get_profile_info(self, userid):
        url = f'https://api.opendota.com/api/players/{userid}'
        return requests.get(url).json()

    def __get_player_heroes(self):
        url = f'https://api.opendota.com/api/players/{self.userid}/heroes'
        return requests.get(url).json()

    def __get_wl(self, game_mode: int = None):
        if game_mode is None:
            url = f'https://api.opendota.com/api/players/{self.userid}/wl'
        else:
            url = f'https://api.opendota.com/api/players/{self.userid}/wl?game_mode={str(game_mode)}'
        return requests.get(url).json()

    def __get_player_recent_matches(self):
        url = f'https://api.opendota.com/api/players/{self.userid}/recentMatches'
        return requests.get(url).json()

    def __get_heroes(self):
        with open(f'{BASE_DIR}/utils/heroes_id.json', 'r') as f:
            dict = json.load(f)
        return dict

    def get_username(self):
        return self.userinfo['profile']['personaname']

    def get_avatar_url(self):
        return self.userinfo['profile']['avatarfull']

    def get_loccountrycode(self):
        return self.userinfo['profile']['loccountrycode']

    def get_profile_url(self):
        return self.userinfo['profile']['profileurl']

    def get_steamid(self):
        return self.userinfo['profile']['steamid']

    def get_rank_tier(self):
        return self.userinfo['rank_tier']

    def get_leaderboard_rank(self):
        return self.userinfo['leaderboard_rank']

    def get_mmr_estimate(self):
        return str(self.userinfo['mmr_estimate'])

    def get_won(self, game_mode: int = None):
        return str(self.__get_wl(game_mode)['win'])

    def get_losses(self, game_mode: int = None):
        return str(self.__get_wl(game_mode)['lose'])

    def is_dota_plus(self):
        return self.userinfo['profile']['plus']

    def get_five_player_heroes_json(self):
        return self.__get_player_heroes()[0:5]

    def get_five_player_heroes_names(self):
        names = []
        for hero in self.get_five_player_heroes_json():
            name = self.search_hero_name(str(hero['hero_id']))
            names.append(name)
        return names

    def search_hero_name(self, id):
        return self.__get_heroes()[id]

    def get_last_match_time(self):
        start_time = self.__get_player_recent_matches()[0]['start_time']
        data = datetime.fromtimestamp(start_time)
        return data.strftime("%d %B %Y %H:%M:%S")


class Rank:
    def __init__(self, userid):
        rank = Parse(userid).get_rank_tier()
        self.leaderboard_rank = Parse(userid).get_leaderboard_rank()

        if rank == 'null':
            self.rank = None
            return

        if type(rank) is int or type(rank) is float:
            rank = str(rank)

        if not all([rank.isdigit(), len(rank) == 2]):
            print("Something went wrong!\nRank input: %s\n" % rank)
            self.rank = None
            return

        self.rank = rank

    def __str__(self):
        return str(self.name)

    @property
    def name(self):
        if self.rank is None:
            return None

        if self.rank[0] == "8":
            return f"Immortal {self.leaderboard_rank}"

        ranks = {"1": "Herald",
                 "2": "Guardian",
                 "3": "Crusader",
                 "4": "Archon",
                 "5": "Legend",
                 "6": "Ancient",
                 "7": "Divine"}

        return f"{ranks[self.rank[0]]} {self.rank[1]}"
