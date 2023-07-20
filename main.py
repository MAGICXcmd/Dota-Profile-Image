from flask import Flask, render_template, request, send_file, redirect
from flask_assets import Environment
from werkzeug.security import safe_join

from utils.assets import bundles

from module.utils.dotaprofile import DotaProfile

app = Flask(__name__)
assets = Environment(app)
assets.register(bundles)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        SteamID = request.form['steam_link']
        img_dir = DotaProfile(SteamID).export()
        return redirect(f'/card/{img_dir}')

    return render_template('index.html')


@app.route('/img/<path:filename>.png')
def serve_image(filename):
    img_path = safe_join('cards', f'{filename}.png')
    return send_file(img_path)


@app.route('/card/<path:filename>')
def card(filename):
    return render_template('image.html', img=filename)


@app.errorhandler(404)
def error404(error):
    return render_template('404.html')


@app.errorhandler(500)
def error500(error):
    return render_template('500.html')