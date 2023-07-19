from flask import Flask, render_template
from flask_assets import Environment

from utils.assets import bundles

# from module.utils.dotaprofile import DotaProfile

DEGUB = True

# if DEGUB:
#     SteamID = 'https://steamcommunity.com/profiles/76561198850706100/'
# else:
#     SteamID = (input('Введите ссылку на профиль Steam: '))

app = Flask(__name__)
assets = Environment(app)
assets.register(bundles)

@app.route('/')
def index():
    return render_template('index.html')
