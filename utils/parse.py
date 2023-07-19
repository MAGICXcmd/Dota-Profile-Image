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
        self.steam32id = userid
        self.userinfo = self.__get_profile_info()

    def __get_profile_info(self):
        url = f'https://api.opendota.com/api/players/{self.steam32id}'
        return requests.get(url).json()

    def __get_player_heroes(self):
        url = f'https://api.opendota.com/api/players/{self.steam32id}/heroes'
        return requests.get(url).json()

    def __get_wl(self, game_mode: int = None):
        if game_mode is None:
            url = f'https://api.opendota.com/api/players/{self.steam32id}/wl'
        else:
            url = f'https://api.opendota.com/api/players/{self.steam32id}/wl?game_mode={str(game_mode)}'
        return requests.get(url).json()

    def __get_player_recent_matches(self):
        url = f'https://api.opendota.com/api/players/{self.steam32id}/recentMatches'
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

    def get_five_player_heroes(self):
        return self.__get_player_heroes()[0:5]

    def get_five_player_heroes_names(self):
        names = []
        for hero in self.get_five_player_heroes():
            name = self.search_hero_name(hero['hero_id'])
            names.append(name)
        return names

    def search_hero_name(self, id):
        return self.__get_heroes()[str(id)]

    def get_last_match_time(self):
        start_time = self.__get_player_recent_matches()[0]['start_time']
        data = datetime.fromtimestamp(start_time)
        return data.strftime("%d %B %Y %H:%M:%S")

    @classmethod
    def get_user_info(cls, userid):
        user = Parse(userid)
        user_info = {}
        user_info['account_id'] = user.steam32id
        user_info['steamid'] = user.get_steamid()
        user_info['personaname'] = user.get_username()
        user_info['avatar'] = user.get_avatar_url()
        user_info['profile_url'] = user.get_profile_url()
        user_info['win_count'] = user.get_won()
        user_info['lose_count'] = user.get_losses()
        user_info['rank_tier'] = user.get_rank_tier()
        user_info['heroes'] = user.get_five_player_heroes_names()
        user_info['last_match'] = user.get_last_match_time()
        user_info['plus'] = user.is_dota_plus()
        user_info['winrate'] = str(round(int(user_info['win_count']) / (int(user_info['win_count']) + int(user_info['lose_count'])) * 100, 2))
        user_info['get_leaderboard_rank'] = str(user.get_leaderboard_rank())
        return user_info


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
