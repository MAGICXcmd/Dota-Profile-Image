from utils.dotaprofile import DotaProfile

DEGUB = False

if DEGUB:
    SteamID = 'https://steamcommunity.com/profiles/76561198850706100/'
else:
    SteamID = (input('Введите ссылку на профиль Steam: '))


if __name__ == "__main__":
    DotaProfile(SteamID)
