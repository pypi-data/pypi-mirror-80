#!/bin/env python
## tle file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

from pyorbital.orbital import Orbital

class tle:
    ## init function
    # @param object   self                  - instance of class
    # @param string   tle_dict              - dict of tle
    def __init__(self, tle_dict):
        if isinstance(tle_dict, list):
            self.line1 = tle_dict[0]
            self.line2 = tle_dict[1]
            self.line3 = tle_dict[2]
        else:
            self.line1 = tle_dict['line1']
            self.line2 = tle_dict['line2']
            self.line3 = tle_dict['line3']

        self.pyOrbital = Orbital(self.line1, line1=self.line2, line2=self.line3)