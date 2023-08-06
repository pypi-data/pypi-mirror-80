#!/bin/env python
## schedule file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

class schedule:
    ## init function
    # @param object   self                  - instance of class
    # @param string   schedule_dict         - dict of schedule
    def __init__(self, schedule_dict, api):
        self.id            = schedule_dict['id']
        self.satelliteId   = schedule_dict['id']
        self.name          = schedule_dict['name']
        self.enabled       = schedule_dict['enabled']
        self.frequency     = schedule_dict['frequency']

        self.api           = api

    ## Enable schedule
    # @param object       self    - instance of class
    # @return return code
    def enable(self):
        postParams = {
            'id':      self.id,
            'enabled': True
        }
        
        req = self.api.protocol.apiPost("admin/schedule/save", postParams, auth=self.api.auth)

        if req.status_code == 200:
            self.enabled = True

        return req.status_code

    ## Disable schedule
    # @param object       self    - instance of class
    # @return return code
    def disable(self):
        postParams = {
            'id':      self.id,
            'enabled': False
        }
        
        req = self.api.protocol.apiPost("admin/schedule/save", postParams, auth=self.api.auth)

        if req.status_code == 200:
            self.enabled = False

        return req.status_code

    ## Cancel current observation if any and start new one
    # @param object       self    - instance of class
    # @return return code
    def immediatelyStart(self):
        postParams = {
            'id':      self.id
        }
        
        req = self.api.protocol.apiPost("admin/schedule/immediately/start", postParams, auth=self.api.auth)

        return req.status_code

    ## Complete currently running observation. This will trigger normal demodulation/decoding process
    # @param object       self    - instance of class
    # @return return code
    def immediatelyComplete(self):
        postParams = {
            'id':      self.id
        }
        
        req = self.api.protocol.apiPost("admin/schedule/immediately/complete", postParams, auth=self.api.auth)

        return req.status_code