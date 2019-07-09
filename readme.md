# Client/Server app for storing information about cars
## Installation:
```
git clone https://github.com/SirNicolas/car_info.git
pip install -r requirements.txt 
```
## Run Client:
* host - path to server that stores information about sold cars
* serial-number - serial_number of sold car
* serial_number - path to json file that stores information about sold car

Read information about sold car
```
python bin/client.py read --host host:port --serial-number serial_number 
```
or

Write to server information about sold car
```
python bin/client.py write --host host:port --c json-path 
```


## Run Server:
* fill host/port and database name in $HOME/settings.json
* install requirements
* run server by `python bin/server.py`

## Run tests:

```
pytest tests
```