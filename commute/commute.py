import googlemaps
from dataclasses import dataclass
import json

class LocationParser(object):
    def __init__(self):
        pass

    @classmethod
    def parse(cls, json_object):
        leg = json_object['legs'][0]
        steps = leg['steps']

        print ("Total Duration is %.3f min" %(leg['duration']['value']/60.0))
        print ("Total Distance is %.3f km" %(leg['distance']['value']/1000.0))
        for step in steps:
            print (step['html_instructions'])
            print ("\tDuration is %.3f min" %(step['duration']['value']/60.0))
            print ("\tDistance is %.3f km" %(step['distance']['value']/1000.0))


class LocationParser(object):
    def __init__(self):
        pass

    @classmethod
    def parse(cls, json_object):
        leg = json_object['legs'][0]
        steps = leg['steps']

        print ("Total Duration is %.3f min" %(leg['duration']['value']/60.0))
        print ("Total Distance is %.3f km" %(leg['distance']['value']/1000.0))
        for step in steps:
            print (step['html_instructions'])
            print ("\tDuration is %.3f min" %(step['duration']['value']/60.0))
            print ("\tDistance is %.3f km" %(step['distance']['value']/1000.0))

class CommuteModes:
    MODE_DRIVE = "driving"
    MODE_WALK = "walking"
    MODE_BIKE = "bicycling"
    MODE_TRANSIT = "transit"
    MODES = [MODE_DRIVE, MODE_TRANSIT, MODE_BIKE, MODE_WALK]
    N_MODES = 4

@dataclass
class CommuteReport:
    dist_in_km: float
    time_in_minutes: float
    mode: str = ""
    # path: dict = {}

class CommuteTracker(object):
    def __init__(self, api_key):
        self._api_key = api_key
        self._gmaps = googlemaps.Client(key=self._api_key)

    def get_commute(self, src, dest, mode, departure_time):
        result = self._gmaps.directions(
            src,
            dest,
            mode=mode,
            departure_time=departure_time
        )

        report = self._commute_report_from_result(result[0])
        report.mode = mode

        return report

    def _commute_report_from_result(self, result):
        # print(result)
        leg = result['legs'][0]
        # steps = leg['steps']

        time_in_minutes = leg['duration']['value']/60.0
        dist_in_km = leg['distance']['value']/1000.0

        return CommuteReport(time_in_minutes=time_in_minutes, dist_in_km=dist_in_km)

def main():
    from datetime import datetime

    tracker = CommuteTracker()
    src = "1075 Jervis St, Vancouver, BC"
    dest = "725 Granville St, Vancouver, BC"
    departure_time = datetime(year=2019, day=30, month=9, hour=13)

    for mode in CommuteModes.MODES:
        res = tracker.get_commute(src, dest, mode, departure_time)
        print (res)

if __name__ == '__main__':
    main()