import time
import math
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
        for i in range(len(state_list.states)):
            position_update_string = convert_to_fsd(state_list.states[i])
            connection.sendall(str.encode(position_update_string))

            time_to_sleep = 1 / len(state_list.states) * 5
            time.sleep(time_to_sleep)

#this function isn't used for now because it creates weird problems with headings that I can't figure out.
#it interpolates aircraft left or right of track, seemingly without cause.
#It might have to do with true track vs magnetic track / heading?
def interpolate_euroscope(state_list):
    if state_list:
        for state in state_list.states:
            #convert lat and long to radians
            rlat = state.latitude * math.pi / 180
            rlong = state.longitude * math.pi / 180
            #convert speed to knots
            speed_in_knots = state.velocity * 1.94384449

            #calculation begin here
            #We assume the earth is a 2D object to make calculations easier (#FlatEarthGang)
            #for small enough areas, it shouldn't really matter

            #first we calculate the distance travelled in degrees of latitude
            #one knot is one minute of latitude per hour
            #thus (divide 3 times by 60 to get degree of latitude per second)
            #then convert to radians and times the time (5 seconds)
            dist = speed_in_knots / 60 / 60 / 60 / 180 * math.pi * 5;
            #the trigonometrics are easier if you draw it out int paint
            correction = 0;
            new_rlat = rlat + dist * math.cos((state.heading - correction) / 180 * math.pi)
            new_rlong = rlong + dist * math.sin((state.heading - correction) / 180 * math.pi)
            #calculation done

            #convert back into degrees
            state.latitude = new_rlat * 180 / math.pi
            state.longitude = new_rlong * 180 / math.pi

            #finally, send data to euroscope
            position_update_string = convert_to_fsd(state)
            connection.sendall(str.encode(position_update_string))

            time_to_sleep = 1 / len(state_list.states) * 5
            time.sleep(time_to_sleep)



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
                #the update_euroscope function sleeps 5 seconds already
                interpolate_euroscope(state_list)
            except Timeout:
                print("Read timeout occured, waiting 10 seconds")
                interpolate_euroscope(state_list)
                interpolate_euroscope(state_list)
    except ConnectionAbortedError:
        print("The connection closed. Restart to continue.")
    finally:
        connection.close()
