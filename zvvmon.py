#!.venv/bin/python3

from flask import (
    Flask,
    render_template,
    send_from_directory,
)
import requests
from datetime import datetime

app = Flask(__name__)

def get_zvv_data():
    now = datetime.now()
    data = {
        'maxJourneys': 8,
        # 'input': 'Zürich,+Haldenegg',
        'input': 'Zürich,+Hardplatz',
        # 'time': now.strftime('%H:%M'),
        'time': '10:00',
        # 'date': now.strftime('%d.%m.%y'),
        'data': '07.07.15',
        'boardType': 'dep',
        'start': 1,
        'tpl': 'stbResult2json'
    }
    r = requests.post('http://online.fahrplan.zvv.ch/bin/stboard.exe/dny', data=data)
    return r.json()

@app.route('/')
def root():
    data = get_zvv_data()
    return render_template('index.html',
        station=data['station'],
        conns=data['connections'])


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.debug = True
    app.run()
