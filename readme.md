# Real life traffic into Euroscope using the Opensky Network
![Showcase](https://github.com/aap007freak/OpenSkyToEuroscope/blob/master/images/showcase.PNG)
## Installation and usage
(It is assumed you already have Euroscope and the correct sector files installed for the area you want to display IRL traffic)
1. Clone or download this repo.
2. In the base folder, you'll find a `config.cfg` file. Here you can edit the bounding box of the area that will be displayed. The format is *min latitude, max latitude, min longitude, max longitude*; all on a separate line. You can find the coordinates you need [here](https://www.openstreetmap.org/export) . By default, the bounding box is centered on EBBU FIR.
3. Run  `OpenSkyToEuroscope.exe`. It should open a console that says *Waiting for Euroscope.*
4. Open Euroscope. In the connection settings:
    *   connection mode = Direct to VATSIM
    *   Server = 127.0.0.1 (It is not in the dropdown menu, but you can just type in the box)
    *   Uncheck the "connect to VATSIM"-checkbox
    *   Since you're not actually connecting to VATSIM, the other fields (e.g. certificate and password)  don't matter
    ![Connection settings](https://github.com/aap007freak/OpenSkyToEuroscope/blob/master/images/connectionsettings.PNG)

5. Click connect. It might take up to 30 seconds for aircraft to load in.
6. Please note that aircraft positions are only updated every 10 seconds.

## How it works
The [Opensky Network](https://opensky-network.org/) is a non-profit community-based receiver network which has been continuously collecting air traffic surveillance data since 2013. It has a free-to-use API from which users can extract flight data.
To gather the data was easy, to put that data into Euroscope was *a lot* harder. At first, the only possible way seemed to use [SBS2FSDproxy](https://adsbradar.ru/sbstofsdproxy-adsb), an outdated and sketchy proxy server that converted SBS data into the FSD format, which is the format VATSIM and IVAO use. After looking at the source code, I figured that it was way easier to just build a FSD server myself.
Using [unofficial documentation](https://studentweb.uvic.ca/~norrisng/fsd-doc/intro/overview/) for the FSD protocol and scenario files (which are essentially already in FSD format) and after testing I figured that to display aircraft in Euroscope, you only need 1 line of FSD.
To add flightplans, you need other lines, but since the Opensky API doesn't have route information, this can't be implemented anyway. In the future it might be possible to link the script with other API's (like flightradar24 or Eurocontrol), to get accurate route information.

## Building from source
The program is written in `Python 3.8.5`.
If you want to edit/extend the source code, you'll have to add the Opensky API via pip. Execute the command `pip install -e lib/opensky-api/python`. (More info [here](https://github.com/openskynetwork/opensky-api)).

## Credits
 * The Opensky team and contributors.
 * Gergely Csernak and contributors for Euroscope.
 * Callum Rid (the source code is partially inspired by [his work](https://github.com/CallumRidd/SBS2FSDproxy/blob/master/SBS2FSDproxy/SBS2FSD.py)).
 * Norris Ng for the [FSD documentation](https://github.com/norrisng/fsd-doc).

 * The guys over at ADSBradar.ru. They still host the SBS2FSDProxy code, which made decompiling a lot easier.
