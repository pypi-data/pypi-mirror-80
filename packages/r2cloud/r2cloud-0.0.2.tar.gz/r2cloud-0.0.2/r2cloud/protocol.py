#!/bin/env python
## Protocol file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

import httpx

class protocol:
    ## init function
    # @param object   self     - instance of class
    # @param string   addr     - address of r2cloud server
    # @param string   version  - version of r2cloud api (default: v1)
    # @param mixed    verify   - verify ssl cert of server (default: False) more read from httpx.get parameter verify
    def __init__(self, addr, version = 'v1', verify = False):
        self.addr    = addr
        self.version = version
        self.verify  = verify

    ## generate api url
    # @param object self
    # @param string suffix - added to end of url
    # @return string
    def getApiUrl(self, suffix = ''):
        return self.addr + '/api/' + self.version + '/' + suffix

    ## HTTP get on api addres
    # @param object      self
    # @param string      action - api action address
    # @param dict        params - GET parameters (Default: None)
    # @param auth object auth   - auth object (Default: None)
    # @return httpx request object
    def apiGet(self, action, params = None, auth = None):
        return httpx.get(
            self.getApiUrl(action),
            verify=self.verify,
            params=params,
            headers=auth.headers() if auth != None else None
        )

    ## HTTP post on api addres
    # @param object      self
    # @param string      action - api action address
    # @param dict        params - POST parameters (Default: None)
    # @param auth object auth   - auth object (Default: None)
    # @return httpx request object
    def apiPost(self, action, params, auth = None):
        return httpx.post(
            self.getApiUrl(action),
            verify=self.verify,
            json=params,
            headers=auth.headers() if auth != None else None
        )

    ## HTTP post on addres on server
    # @param object      self
    # @param string      suburl - address on server (Ex: /api/v1)
    # @param dict        params - POST parameters (Default: None)
    # @param auth object auth   - auth object (Default: None)
    # @return httpx request object
    def post(self, suburl, params, auth = None):
        return httpx.post(
            self.addr + suburl,
            verify=self.verify,
            json=params,
            headers=auth.headers() if auth != None else None
        )

    ## HTTP get on addres on server
    # @param object      self
    # @param string      suburl - address on server (Ex: /api/v1)
    # @param dict        params - GET parameters (Default: None)
    # @param auth object auth   - auth object (Default: None)
    # @return httpx request object
    def get(self, suburl, params = None, auth = None):
        return httpx.get(
            self.addr + suburl,
            verify=self.verify,
            params=params,
            headers=auth.headers() if auth != None else None
        )