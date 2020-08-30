
import time
import requests
import socket as s

from opensky_api import OpenSkyApi
from requests.exceptions import Timeout  # this handles ReadTimeout or ConnectTimeout


def convert_to_fsd(state):
    #according to euroscope scenario file docs + unofficial fsd protocol docs
    base_string = "@{transponder}:{callsign}:{squawk}:1:{lat}:{long}:{alt}:0:{heading}:0\n"

    #alter some variables
    altitude_in_feet = 0
    if(state.baro_altitude != None):
        altitude_in_feet = state.baro_altitude * 3.2808399

    transponder_mode = "N"
    if(state.on_ground):
        transponder_mode = "S"

    #compose the final string
    return base_string.format(
        transponder=transponder_mode,
        callsign=state.callsign, squawk=state.squawk,
        lat=state.latitude, long=state.longitude,
        alt=round(altitude_in_feet), heading=state.heading)

def update_euroscope(state_list):
    if state_list:
        for state in state_list.states:
            position_update_string = convert_to_fsd(state)
            connection.sendall(str.encode(position_update_string))

#load config file
with open("config.cfg", "r") as cfg:
    bounds = list([ float(line) for line in cfg])


#initialize api
api = OpenSkyApi()

#setup socket
socket = s.socket(s.AF_INET, s.SOCK_STREAM)
adress = ('127.0.0.1', 6809)
socket.bind(adress)
socket.listen(1) # the socket only accepts 1 client (Euroscope)

while 1:
    print('Waiting for Euroscope.')
    connection, client_address = socket.accept()
    print('Connected to Euroscope', connection, client_address)
    state_list = []
    try:
        while(1):
            try:
                state_list = api.get_states(bbox=bounds)
                update_euroscope(state_list)
                time.sleep(10)
            except Timeout:
                print("Read timeout occured, waiting 10 seconds")
                #to prevent weird speed issues when the update times out, we
                update_euroscope(state_list)
                time.sleep(10)
    except ConnectionAbortedError:
        print("The connection closed. Restart to continue.")
    finally:
        connection.close()
