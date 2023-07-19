import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from utils.parse import Parse, Rank, SteamID32

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class DotaProfile:
    def __init__(self, steam_link):
        self.userid = SteamID32.get_steamid32(steam_link)
        self.username = Parse(self.userid).get_username()
        self.avatar_url = Parse(self.userid).get_avatar_url()
        self.win_count = Parse(self.userid).get_won()
        self.lose_count = Parse(self.userid).get_losses()
        self.rank_tier = Parse(self.userid).get_rank_tier()
        self.heroes = Parse(self.userid).get_five_player_heroes_names()
        self.last_match = Parse(self.userid).get_last_match_time()
        self.is_plus = Parse(self.userid).is_dota_plus()
        self.winrate = str(round(int(self.win_count) / (int(self.win_count) + int(self.lose_count)) * 100, 2))
        self.heroes_images = self.__output_images_of_five_favorite_characters()
        self.get_leaderboard_rank = str(Parse(self.userid).get_leaderboard_rank())

        self.capture_this()

    def capture_this(self):
        # Fonts
        nickname_font = self.__setup_font('OpenSans-Bold', 22)
        lastmath_text = self.__setup_font('OpenSans-Regular', 11)
        lastmath_data = self.__setup_font('OpenSans-SemiBold', 11)
        winloserate = self.__setup_font('OpenSans-Regular', 12)
        stats_number = self.__setup_font('OpenSans-Medium', 18)
        leaderboard_rank_font = self.__setup_font('OpenSans-Medium', 16)

        img = Image.open(f'{BASE_DIR}/img/background.png')
        draw = ImageDraw.Draw(img)

        # Resize
        avatar = self.__take_avatar().resize((93, 93), resample=Image.Resampling.LANCZOS)
        img.paste(avatar, (25,21))

        # Heroes images paste
        heroes_images = [x.resize((21, 21), resample=Image.Resampling.LANCZOS) for x in self.heroes_images]
        img.paste(heroes_images[0], (133, 93),  mask=heroes_images[0])
        img.paste(heroes_images[1], (158, 93),  mask=heroes_images[1])
        img.paste(heroes_images[2], (183, 93),  mask=heroes_images[2])
        img.paste(heroes_images[3], (208, 93),  mask=heroes_images[3])
        img.paste(heroes_images[4], (232, 93),  mask=heroes_images[4])

        # Rank
        rank_image = self.__rank_images()[0].resize((100, 100), resample=Image.Resampling.LANCZOS)
        img.paste(rank_image, (328,20),  mask=rank_image)
        if type(self.__rank_images()[1]) != int:
            rank_stars_image = self.__rank_images()[1].resize((100, 100), resample=Image.Resampling.LANCZOS)
            img.paste(rank_stars_image, (328, 20),  mask=rank_stars_image)
        else:
            leaderboard_rank = str(self.__rank_images()[1])
            w, h = draw.textsize(leaderboard_rank)
            draw.text((380-w, 103-h), leaderboard_rank, font=leaderboard_rank_font, fill=(255, 255, 255))

        # Dota plus
        if self.is_plus:
            plus_img = Image.open(f'{BASE_DIR}/img/dota_plus.png').convert('RGBA')
            plus_img = plus_img.resize((27, 31), resample=Image.Resampling.LANCZOS)
            img.paste(plus_img, (103,92),  mask=plus_img)

        # First part
        draw.text((130, 17), self.username,  font=nickname_font, fill=(255, 255, 255))
        draw.text((130, 45), 'Last match:',  font=lastmath_text, fill=(142, 165, 176))
        draw.text((193, 45), self.last_match,  font=lastmath_data, fill=(255, 255, 255))

        draw.text((130, 59), 'WON', font=winloserate, fill=(141, 165, 175))
        draw.text((190, 59), 'LOST', font=winloserate, fill=(141, 165, 175))
        draw.text((252, 59), 'WINRATE', font=winloserate, fill=(141, 165, 175))

        draw.text((130, 68), self.win_count,  font=stats_number, fill=(100, 184, 105))
        draw.text((190, 68), self.lose_count,  font=stats_number, fill=(241, 74, 76))
        draw.text((252, 68), self.winrate + '%',  font=stats_number, fill=(255, 255, 255))

        # Image save
        img.save('{}/export/{}.png'.format(BASE_DIR, self.userid))

    def __take_avatar(self):
        avatar = Image.open(BytesIO(requests.get(self.avatar_url, stream = True).content))
        return avatar

    def __setup_font(self, name, size: int):
        return ImageFont.truetype(f'{BASE_DIR}/fonts/{name}.ttf', size, encoding='unic')

    def __output_images_of_five_favorite_characters(self):
        heroes_images = []
        for hero in self.heroes:
            if hero.count(' ') != 0:
                hero = hero.replace(' ', '_')
            image_png = Image.open(f'{BASE_DIR}/img/heroes/{hero}.png').convert('RGBA')
            heroes_images.append(image_png)
        return heroes_images

    def __rank_images(self):
        rank = str(Rank(self.userid)).split()
        if rank[0] == 'Immortal':
            if int(rank[1]) > 100:
                rank_img = Image.open(f'{BASE_DIR}/img/ranks/Immortal.png').convert('RGBA')
                return [rank_img, int(rank[1])]
            elif 100 >= int(rank[1]) > 10:
                rank_img = Image.open(f'{BASE_DIR}/img/ranks/Immortalb.png').convert('RGBA')
                return [rank_img, int(rank[1])]
            elif 10 >= int(rank[1]) >= 1:
                rank_img = Image.open(f'{BASE_DIR}/img/ranks/Immortalc.png').convert('RGBA')
                return [rank_img, int(rank[1])]
        else:
            rank_img = Image.open(f'{BASE_DIR}/img/ranks/{rank[0]}.png').convert('RGBA')
            rank_stars_img = Image.open(f'{BASE_DIR}/img/ranks/stars/{rank[1]}.png').convert('RGBA')
            return [rank_img, rank_stars_img]





