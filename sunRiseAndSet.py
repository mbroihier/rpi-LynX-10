#!/usr/bin/python
import homogeneoustransforms as ht
import earthInfo
import time
import datetime
import calendar
import math
import sys

currentTime = calendar.timegm(datetime.datetime.strptime("6/20/2016:22:34","%m/%d/%Y:%H:%M").timetuple())

thisDay = currentTime

timeSinceReference = currentTime - calendar.timegm(datetime.datetime.strptime("6/20/2016:22:34","%m/%d/%Y:%H:%M").timetuple())
angleOfEarthRelativeToSun = (timeSinceReference % earthInfo.oneYear)*2*math.pi / earthInfo.oneYear

pointOnEarth = ht.vector(0,0,0)

angleOffsetToTrueNoon =  (calendar.timegm(datetime.datetime.strptime("6/20/2016:12:00","%m/%d/%Y:%H:%M").timetuple()) - calendar.timegm(datetime.datetime.strptime("6/20/2016:22:34","%m/%d/%Y:%H:%M").timetuple()))*2*math.pi/earthInfo.oneDay + math.pi

longitude = float(sys.argv[2]) * 2 * math.pi / 360.0 - angleOffsetToTrueNoon

#print 'longitude relative to time reference 1 = ', longitude / math.pi * 180, ' degrees'
latitude = float(sys.argv[1]) * 2 * math.pi / 360.0

pointOnEarth.x = math.cos(longitude) * earthInfo.radius * math.cos(latitude)
pointOnEarth.y = math.sin(longitude) * earthInfo.radius * math.cos(latitude)
pointOnEarth.z = math.sin(latitude) * earthInfo.radius

#print pointOnEarth, pointOnEarth.mag()


solarPlaneTransform = ht.rotateZ(angleOfEarthRelativeToSun) * ht.translateX(earthInfo.distanceToSun) 

v = earthInfo.solarDisk()[0]
earthVector = ht.vector(v[0],v[1],v[2])
sunVector = solarPlaneTransform * earthVector

diskMag = sunVector.mag()


sunIsNowDown = 1
lastTimeSunWasDown = sunIsNowDown

firstTime = 1
sunUp = 0
delta = 30
correction = earthInfo.oneDay % delta

timeTable = [['//// ////' for i in range (0,31)] for j in range (0,12)]

for day in range(0,367):

    timeSinceReference = thisDay - calendar.timegm(datetime.datetime.strptime("6/20/2016:22:34","%m/%d/%Y:%H:%M").timetuple())
    angleOfEarthRelativeToSun = (timeSinceReference % earthInfo.oneYear)*2*math.pi / earthInfo.oneYear
    earthToSunTransformPart1 = ht.translateX(math.cos(angleOfEarthRelativeToSun)*earthInfo.distanceToSun) * ht.translateY(math.sin(angleOfEarthRelativeToSun)*earthInfo.distanceToSun) * ht.rotateY(-earthInfo.tiltRelativeToTheSunEarthPlane)

    for secondOfDay in range(0,earthInfo.oneDay,delta):
        UTCtimeOfDay = currentTime
#        earthToSunTransform = earthToSunTransformPart1*ht.rotateZ(math.pi*2*UTCtimeOfDay / earthInfo.oneDay)
        earthToSunTransform = earthToSunTransformPart1*ht.rotateZ(math.pi*2*secondOfDay / earthInfo.oneDay)

        pointOnEarthRelativeToSun = earthToSunTransform * pointOnEarth
        mag = pointOnEarthRelativeToSun.mag()
#        print 'point on earth relative to sun: ', pointOnEarthRelativeToSun, 'mag: ', mag
        sunIsNowDown = mag > diskMag
        if sunIsNowDown != lastTimeSunWasDown and not firstTime:
            if not sunIsNowDown:
                sunUp = currentTime
            else:
                sunRise = ('0' if len(str(time.gmtime(sunUp).tm_hour)) == 1 else '')+str(time.gmtime(sunUp).tm_hour)+('0'if len(str(time.gmtime(sunUp).tm_min)) ==1 else '')+str(time.gmtime(sunUp).tm_min)
                sunSet = ('0' if len(str(time.gmtime(UTCtimeOfDay).tm_hour)) == 1 else '')+str(time.gmtime(UTCtimeOfDay).tm_hour)+('0'if len(str(time.gmtime(UTCtimeOfDay).tm_min)) ==1 else '')+str(time.gmtime(UTCtimeOfDay).tm_min)
#                print ("****%2d %2d %s %s" % (time.gmtime(sunUp).tm_mon,time.gmtime(sunUp).tm_mday,sunRise,sunSet))
                timeTable [time.gmtime(sunUp).tm_mon - 1][time.gmtime(sunUp).tm_mday - 1] = sunRise + ' ' + sunSet

        currentTime += delta
        lastTimeSunWasDown = sunIsNowDown
        firstTime = 0

    thisDay += earthInfo.oneDay
    currentTime += correction - delta
    if currentTime != thisDay:
        print 'time not synchronized', thisDay, currentTime, correction

timeTable[1][28] = timeTable[1][27]
for i in range (0,31):
    line = ("%2.2d " % (i+1))
    for j in range (0,12):
        line += ' ' + timeTable[j][i]
    print line




