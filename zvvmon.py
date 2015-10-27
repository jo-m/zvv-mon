#!.venv/bin/python3

from flask import (
    Flask,
    render_template,
    send_from_directory,
)
import requests
from datetime import datetime

app = Flask(__name__)

def get_zvv_data(station_name):
    now = datetime.now()
    data = {
        'maxJourneys': 8,
        # 'input': 'Zürich,+Hardplatz',
        # 'time': '10:00',
        # 'data': '07.07.15',
        # 'time': now.strftime('%H:%M'),
        # 'date': now.strftime('%d.%m.%y'),
        'input': station_name,
        'boardType': 'dep',
        'start': 1,
        'tpl': 'stbResult2json'
    }
    r = requests.post('http://online.fahrplan.zvv.ch/bin/stboard.exe/dny', data=data)
    return r.json()

@app.route('/<station_name>')
def root(station_name='Zürich,+Haldenegg'):
    data = get_zvv_data(station_name)
    return render_template('index.html',
        station=data['station'],
        conns=data['connections'])

@app.route('/')
def root_noarg():
    return root()


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
