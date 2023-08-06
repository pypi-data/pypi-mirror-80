#!/bin/env python
## tleArray file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

from .tle import tle
from datetime import datetime

class tleArray:
    ## init function
    # @param object   self                  - instance of class
    # @param string   tlearray_dict         - dict of tleArray
    def __init__(self, tlearray_dict):
        self.lastUpdated = datetime.fromtimestamp(tlearray_dict['lastUpdated'] / 1000)
        self.tle         = []

        for tle_dict in tlearray_dict['tle']:
            self.tle.append(
                tle(tle_dict['data'])
            )