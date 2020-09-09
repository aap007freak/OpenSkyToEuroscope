import math

#Bounds of the area
lat_min = 50
lat_max = 52
long_min = 0
long_max = 2
lat_center = 51
long_center = 1

lat1 = 50.5
long1 = 0.5
heading1 = 45
speed1 = 100 #knots

lat2 = 51.5
long2 = 1.5
heading2 = 180 # knots
speed2 = 200

#long = sinus, lat = cosinus

def interpolate(lat, long, speed, heading, seconds):
    #convert lat and long into radians
    rlat = lat * math.pi / 180
    rlong = long * math.pi / 180
    #knots is minutes of latitude per hour, to get degrees of latitude, we need to  it per second, we need to divide by 60 twice
    dist = speed / 60 / 60 / 60 / 60 * seconds;
    print(dist)
    new_rlat = rlat + dist * math.cos(heading / 180 * math.pi)
    new_rlong = rlong + dist * math.sin(heading / 180 * math.pi)
    #convert back into degrees
    new_lat = new_rlat * 180 / math.pi
    new_long = new_rlong * 180 / math.pi
    print("The coordinates were interpolated from:", lat, long, "to", round(new_lat, 3), round(new_long, 5))

interpolate(lat1, long1, speed1, heading1, 5)
interpolate(lat2, long2, speed2, heading2, 5)
