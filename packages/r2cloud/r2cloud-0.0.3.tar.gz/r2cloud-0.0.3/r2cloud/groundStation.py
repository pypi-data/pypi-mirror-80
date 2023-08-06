#!/bin/env python
## groundStation file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

from datetime import datetime

class groundStation:
    ## init function
    # @param object   self                  - instance of class
    # @param string   groundStation_dict    - dict of groundStation
    def __init__(self, groundStation_dict):
        self.lon = groundStation_dict['lon']
        self.lat = groundStation_dict['lat']

        if "alt" in groundStation_dict:
            self.alt = groundStation_dict['alt']
        else:
            self.alt = 0

        if "elevationMin" in groundStation_dict:
            self.elevationMin = groundStation_dict['elevationMin']
        else:
            self.elevationMin = 0

    ## Find future pass by TLE
    # @param object       self    - instance of class
    # @param tle object   tle     - tle of object to observe
    # @param int          length  - Number of hours to find passes (Default: 10)
    # @param datetime obj utctime - current UTC time (Default: datetime.utcnow())
    def futurePass(self, tle, length = 10, utctime = None):
        if utctime == None:
            utctime = datetime.utcnow()

        return tle.pyOrbital.get_next_passes(
            utctime,
            length,
            self.lon,
            self.lat, 
            self.alt, 
            tol=0.001, 
            horizon=self.elevationMin
        )