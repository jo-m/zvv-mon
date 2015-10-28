#!.venv/bin/python3

from datetime import datetime
from flask import (
   Flask,
   render_template,
   request,
   send_from_directory,
)
import html
import json
import requests

DEFAULT_STATION = 'Zürich,+Haldenegg'

app = Flask(__name__)

def gets_suggestion(text):
    """
    Get a station (id) by (incomplete) name, uses the fuzzy search API.
    """
    url = 'http://online.fahrplan.zvv.ch/bin/ajax-getstop.exe/dn'
    data = {
        'encoding': 'utf-8',
        'start': 1,
        'getstop': 1,
        'suggestMethod': None,
        'S': text,
        'REQ0JourneyStopsS0A': 1,
        'REQ0JourneyStopsB': 10,
    }
    r = requests.get(url, params=data)
    # have to strip away Javascript returned
    return json.loads(r.text[8:-22])['suggestions']

def get_zvv_data(station_name, station_id, maxJourneys=8):
    """
    Fetch the timetable for a given station name and id
    """
    data = {
        'maxJourneys': maxJourneys,
        # 'input': 'Zürich,+Hardplatz',
        # 'time': '10:00',
        # 'data': '07.07.15',
        'REQStationS0ID': station_id,
        'input': station_name,
        'boardType': 'dep',
        'start': 1,
        'tpl': 'stbResult2json',
    }
    r = requests.post('http://online.fahrplan.zvv.ch/bin/stboard.exe/dny', data=data)
    return r.json()

@app.route('/slack_api/')
def slack_api():
    """
    API for slack
    """
    stations = gets_suggestion(request.args.get('refresh', DEFAULT_STATION))
    if len(stations) == 0:
        return 'Station not found'

    name, sid = stations[0]['value'], stations[0]['id']
    data = get_zvv_data(name, sid, 4)

    return render_template('slack.txt',
        station=data['station'],
        conns=data['connections'])

@app.route('/<station_name>')
def root(station_name=DEFAULT_STATION):
    """
    Standard endpoint
    """
    stations = gets_suggestion(station_name)
    if len(stations) == 0:
        return render_template('notfound.html'), 404

    name, sid = stations[0]['value'], stations[0]['id']
    data = get_zvv_data(name, sid)

    return render_template('index.html',
        station=data['station'],
        conns=data['connections'],
        refresh=request.args.get('refresh', None))

@app.route('/')
def root_noarg():
    """
    Standard endpoint with no args
    """
    return root()

@app.route('/static/<path:path>')
def send_js(path):
    """
    Serves static files (CSS, Fonts)
    """
    return send_from_directory('static', path)

@app.template_filter('unescape')
def unescape(arg):
    return html.unescape(arg)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
