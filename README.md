# ZVV Abfahrtszeiten, mit Slack Integration

Zeigt die Abfahrtszeiten von Haltestellen des Züricher Verkehrsverbunds an.
Die Daten sind in Echt-Zeit und berücksichtigen auch Verspätungen etc.

## Local setup
    pip install virtualenv
    virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    # run app
    ./zvvmon.py

Die App ist nun hier erreichbar: <http://localhost:5000>. Um andere
Haltestellen abzufragen, einfach als Pfad den Namen anhängen:

* <http://localhost:5000/Zürich,+Central>
* <http://localhost:5000/Zürich,+Klusplatz>

Um die Seite automatisch neu zu laden, den `refresh=<sekunden>` Parameter
hinzufügen:

<http://localhost:5000/Zürich,+Central?refresh=20>

## Setup on server

    sudo apt-get install python3-pip
    sudo adduser zvv
    sudo passwd -l zvv
    sudo su zvv
    cd
    pip3 install --user virtualenv
    git clone https://github.com/jo-m/zvv-mon.git
    cd zvv-mon
    ~/.local/bin/virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    crontab -e

    # add this line:
    @reboot cd /home/zvv/zvv-mon/; ./zvvmon.py

    # optionally, for keeping a log:
    @reboot cd /home/zvv/zvv-mon/; ./zvvmon.py &>> /home/zvv/zvv-log.txt

After a reboot, the app should be reachable at <http://example.com:5000/>.

## Slack setup
Add a new slack command here: <https://<domain>.slack.com/services/new/slash-commands>.

* URL: http://<example.com:5000/slack_api/>
* Method: `GET`

Thats it! You can now use `/zvv Station Name` from Slack.
