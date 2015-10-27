# ZVV Abfahrtszeiten

Zeigt die Abfahrtszeiten von Haltestellen des Züricher Verkehrsverbunds an.
Die Daten sind in Echt-Zeit und berücksichtigen auch Verspätungen etc.

## Local setup
    pip install virtualenv
    virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    # run app
    ./zvvmon.py

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

After a reboot, the script should be reachable at <http://host:5000/>.
