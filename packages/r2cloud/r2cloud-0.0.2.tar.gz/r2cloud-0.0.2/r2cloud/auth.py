#!/bin/env python
## tle file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

import time

class auth:
    ## init function
    # @param object     self             - instance of class
    # @param dict       auth_dict        - dict of auth
    def __init__(self, auth_dict):
        self.token_type   = auth_dict['token_type']
        self.access_token = auth_dict['access_token']
        self.expires_in   = time.time() + auth_dict['expires_in'] - 10

    ## generate header with auth token
    # @param self
    # @return dict
    def headers(self):
        return {
            'Authorization': self.token_type + ' ' + self.access_token
        }

    ## is auth valid
    # @param self
    # @return bool (is valid - not expirated)
    def isValid(self):
        return time.time() < self.expires_in