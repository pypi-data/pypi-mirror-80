#!/bin/env python
## api file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

from .protocol           import protocol
from .auth               import auth
from .observationSummary import observationSummary
from .observation        import observation
from .tleArray           import tleArray
from .schedule           import schedule

class api:
    ## init function
    # @param object   self     - instance of class
    # @param string   addr     - address of r2cloud server
    # @param string   version  - version of r2cloud api (default: v1)
    # @param mixed    verify   - verify ssl cert of server (default: False) more read from httpx.get parameter verify
    def __init__(self, addr, version = 'v1', verify = False):
        self.protocol = protocol(addr, version, verify)

    ## set self values and login to r2cloud server
    # @param object   self      - instance of class
    # @param string   username  - username to login (Ex: test@test.com)
    # @param string   password  - password for username
    # @post  in self.auth is set auth object
    # @return auth object when ok else int return code
    def login(self, username, password):
        
        self.username = username
        self.password = password

        return self.selfLogin()

    ## reLogin when auth token is expired else do nothing
    # @param object   self      - instance of class
    # @return None if token is fresh else auth object when login ok else return code
    def freshAuth(self):
        if not(self.auth.isValid()):
            return self.selfLogin()
            
    ## login to r2cloud server using self values
    # @param object   self      - instance of class
    # @post  in self.auth is set auth object
    # @return auth object when ok else int return code
    def selfLogin(self):
        loginParams = {
            'username': self.username,
            'password': self.password
        }
        
        req = self.protocol.apiPost("accessToken", loginParams)

        if req.status_code != 200:
            return req.status_code
        
        self.auth = auth(req.json())

        return self.auth

    ## get Observation list from server
    # @param object   self      - instance of class
    # @return list of observationSummary obj when ok else return code
    def observationList(self):

        req = self.protocol.apiGet("admin/observation/list", auth=self.auth)

        if req.status_code != 200:
            return req.status_code
        
        res = []
        for observation in req.json():
            res.append(
                observationSummary(observation, self)
            )

        return res

    ## get Observation from server
    # @param object   self          - instance of class
    # @param int      observationId - id of observation
    # @param int      satelliteId   - id of observated satellite
    # @return observation obj when ok else return code
    def observation(self, observationId, satelliteId):
        getParams = {
            'id':          observationId,
            'satelliteId': satelliteId
        }

        req = self.protocol.apiGet("admin/observation/load", params=getParams, auth=self.auth)
        
        if req.status_code != 200:
            return req.status_code
            
        return observation(req.json(), self)

    ## get TLE from server
    # @param object   self          - instance of class
    # @return tleArray obj when ok else return code
    def tle(self):
        req = self.protocol.apiGet("admin/tle", auth=self.auth)
        
        if req.status_code != 200:
            return req.status_code
            
        return tleArray(req.json())

    ## get schedule List from server
    # @param object   self      - instance of class
    # @return list of schedule obj when ok else return code
    def scheduleList(self):

        req = self.protocol.apiGet("admin/schedule/list", auth=self.auth)

        if req.status_code != 200:
            return req.status_code
        
        res = []
        for schedule_dict in req.json():
            res.append(
                schedule(schedule_dict, self)
            )

        return res
        print(req.json())

