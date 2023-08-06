#!/bin/env python
## Observation file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

from datetime       import datetime
from .tle            import tle
from .groundStation  import groundStation

class observation:
    ## init function
    # @param object     self             - instance of class
    # @param dict       dict_observation - dict of obeservation
    # @param api object api              - instance of api for server with observation
    def __init__(self, dict_observation, api):
        self.id                      = int(dict_observation["id"])
        self.satellite               = int(dict_observation["satellite"])
        self.start                   = datetime.fromtimestamp(dict_observation["start"] / 1000)
        self.end                     = datetime.fromtimestamp(dict_observation["end"]   / 1000)
        self.sampleRate              = dict_observation["sampleRate"]
        self.inputSampleRate         = dict_observation["inputSampleRate"])
        self.frequency               = dict_observation["frequency"]
        self.actualFrequency         = dict_observation["actualFrequency"]
        self.decoder                 = dict_observation["decoder"]
        self.bandwidth               = dict_observation["bandwidth"]
        self.tle                     = tle(dict_observation["tle"])
        self.numberOfDecodedPackets  = dict_observation["numberOfDecodedPackets"]
        self.groundStation           = groundStation(dict_observation["groundStation"])
        self.gain                    = dict_observation["gain"]
        self.biast                   = dict_observation["biast"]
        self.rawURL                  = dict_observation["rawURL"]

        
        if "channelA" in dict_observation:
            self.channelA                = dict_observation["channelA"]
            self.channelB                = dict_observation["channelB"]
        
        if "dataEntity" in dict_observation:
            self.dataEntity              = dict_observation["dataEntity"]
        
        if "aURL" in dict_observation:
            self.aURL                    = dict_observation["aURL"]
        
        if "data" in dict_observation:
            self.dataURL                 = dict_observation["data"]   

        if "spectogramURL" in dict_observation:
            self.spectrogramURL           = dict_observation["spectogramURL"]             
        

        self.api                     = api

    ## get data of decoded image (A Layer)
    # @param object     self             - instance of class
    # @return binnary data of JPG image
    def a(self):
        req = self.api.protocol.get(self.aURL, auth=self.api.auth)
        
        if req.status_code != 200:
            return req.status_code
            
        return req.content

    ## get data of RAW record
    # @param object     self             - instance of class
    # @return binnary data of WAV (NOAA) OR RAW.GZ (OTHER)
    def raw(self):
        req = self.api.protocol.get(self.rawURL, auth=self.api.auth)
        
        if req.status_code != 200:
            return req.status_code
            
        return req.content

    ## get binary decoded data
    # @param object     self             - instance of class
    # @return binnary data
    def data(self):
        req = self.api.protocol.get(self.dataURL, auth=self.api.auth)
        
        if req.status_code != 200:
            return req.status_code
            
        return req.content
    
    ## Create req for create Spectrogram
    # @param object     self             - instance of class
    # @return None
    def makeSpectrogram(self):
        pass

    ## get data of spectrogram
    # @param object     self             - instance of class
    # @return binnary data of PNG
    def spectrogram(self):
        req = self.api.protocol.get(self.spectrogramURL, auth=self.api.auth)
        
        if req.status_code != 200:
            return req.status_code
            
        return req.content
