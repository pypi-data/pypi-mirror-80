#!/bin/env python
## common tools file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

from ..tleArray import tleArray

## filter observation list by satellite
# @param list of observationSummary obj               observationList   - list of observations to filter
# @param mixed (int or str in list or independently)  satellite         - name of sat or norad id in list or independently (Ex: "NOAA 19" or 33591 or ["NOAA 19", "NOAA 18"] or [33591, 33592])                
# @return list of observationSummary obj
def filterSat(observationList, satellites):
    if not(isinstance(satellites, list)):
      satellites = [satellites] 

    res = []
    for observation in observationList:
      if observation.name in satellites or observation.satelliteId in satellites:
        res.append(observation)

    return res

## filter tle array by satellite
# @param tleArray obj                                 tleArrayIN    - tle array to filter
# @param mixed (int or str in list or independently)  sattellite    - name of sat or norad id in list or independently (Ex: "NOAA 19" or 33591 or ["NOAA 19", "NOAA 18"] or [33591, 33592])                
# @return list of observationSummary obj
def tleFilterSat(tleArrayIN, satellites):
    if not(isinstance(satellites, list)):
      satellites = [satellites] 

    res = tleArray({
      'lastUpdated': float(tleArrayIN.lastUpdated.strftime('%s')) * 1000,
      'tle': []
    })

    for tle in tleArrayIN.tle:
      if tle.line1 in satellites:
        res.tle.append(tle)

    return res


## filter observation list, have only with data
# @param list of observationSummary obj   observationList - list of observations to filter    
# @return list of observationSummary obj
def filterHasData(observationList):
    res = []
    for observation in observationList:
      if observation.hasData:
        res.append(observation)

    return res

## filter schedule list, have only enabled
# @param list of schedule obj   scheduleList - list of schedules to filter              
# @return list of schedule obj
def filterEnabled(scheduleList):
    res = []
    for schedule in scheduleList:
      if schedule.enabled:
        res.append(schedule)

    return res

## save binary data to file
# @param self
# @param mixed  bin  - binary data to save
# @param string file - file name 
# @return None
def bin2file(bin, file):
    file = open(file, "wb")
    file.write(bin)
    file.close()

