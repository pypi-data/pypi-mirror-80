#!/bin/env python
## observationSummary file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

from .observation import observation
from datetime    import datetime

class observationSummary:
    ## init function
    # @param object     self             - instance of class
    # @param dict       dict_observation - dict of obeservationSummary
    # @param api object api              - instance of api for server with observation
    def __init__(self, dict_observation, api):
        self.id           = int(dict_observation["id"])
        self.satelliteId  = int(dict_observation["satelliteId"])
        self.name         = dict_observation["name"]
        self.start        = datetime.fromtimestamp(dict_observation["start"] / 1000)
        self.hasData      = dict_observation["hasData"]
        self.api          = api

        self.detailsCache = None

    ## get Observation object of observationSummary
    # it download observation only firstly, secondly use cache
    # @param object     self             - instance of class
    # @param bool       redownload       - force download from server, do not use cache
    # @return observation object
    def details(self, redownload = False):
        if (self.detailsCache == None) or redownload:
            self.detailsCache = self.api.observation(self.id, self.satelliteId)

        return self.detailsCache

