import homogeneoustransforms as ht
import earthInfo
import time
import datetime
import calendar
import math

currentTime = time.time()

timeSinceReference = currentTime - calendar.timegm(datetime.datetime.strptime("6/20/2016:22:34","%m/%d/%Y:%H:%M").timetuple())
angleOfEarthRelativeToSun = (timeSinceReference % earthInfo.oneYear)*2*math.pi / earthInfo.oneYear

earthToSunTransform = ht.translateX(math.cos(angleOfEarthRelativeToSun)*earthInfo.distanceToSun) * ht.translateY(math.sin(angleOfEarthRelativeToSun)*earthInfo.distanceToSun) * ht.rotateY(-earthInfo.tiltRelativeToTheSunEarthPlane)

solarPlaneTransform = ht.rotateZ(angleOfEarthRelativeToSun) * ht.translateX(earthInfo.distanceToSun) 

v = earthInfo.solarDisk()[0]
earthVector = ht.vector(v[0],v[1],v[2])
sunVector = solarPlaneTransform * earthVector

diskMag = sunVector.dot(sunVector)

sunIsDown = 1
index = 0

pointsAtLatitude = [ht.vector(0,0,0) for i in range(0,24*3600)]

for v in earthInfo.latitude(0*math.pi/180):
    earthVector = ht.vector(v[0],v[1],v[2])
    sunVector = earthToSunTransform * earthVector
    pointsAtLatitude[index] = sunVector
#    print sunVector
    mag = sunVector.dot(sunVector)
    if index == 0:
        min = max = mag
    if mag < min:
        min = mag
        minIndex = index
    if mag > max:
        max = mag
        maxIndex = index
    if diskMag > mag and sunIsDown:
        print "sun is up at:"
        print index
        sunIsDown = 0
    else:
        if diskMag < mag and not sunIsDown:
            print "sun is down at:"
            print index
            sunIsDown = 1;
            lastDownIndex = index
            
    index = index + 1
#    print sunVector

for day in range(0,365):

    currentTime += earthInfo.oneDay

    timeSinceReference = currentTime - calendar.timegm(datetime.datetime.strptime("6/20/2016:22:34","%m/%d/%Y:%H:%M").timetuple())
    angleOfEarthRelativeToSun = (timeSinceReference % earthInfo.oneYear)*2*math.pi / earthInfo.oneYear

    earthToSunTransform = ht.translateX(math.cos(angleOfEarthRelativeToSun)*earthInfo.distanceToSun) * ht.translateY(math.sin(angleOfEarthRelativeToSun)*earthInfo.distanceToSun) * ht.rotateY(-earthInfo.tiltRelativeToTheSunEarthPlane)

    solarPlaneTransform = ht.rotateZ(angleOfEarthRelativeToSun) * ht.translateX(earthInfo.distanceToSun) 

    v = earthInfo.solarDisk()[0]
    earthVector = ht.vector(v[0],v[1],v[2])
    sunVector = solarPlaneTransform * earthVector

    diskMag = sunVector.dot(sunVector)

    index = 0

    for v in earthInfo.latitude(33.1*math.pi/180):
        earthVector = ht.vector(v[0],v[1],v[2])
        sunVector = earthToSunTransform * earthVector
#    print sunVector
        mag = sunVector.dot(sunVector)
        if index == 0:
            min = max = mag
        if mag < min:
            min = mag
            minIndex = index
        if mag > max:
            max = mag
            maxIndex = index
        if diskMag > mag and sunIsDown:
#            print "sun is up at:"
#            print index
            sunIsDown = 0
        else:
            if diskMag < mag and not sunIsDown:
#                print "sun is down at:"
                print index, ' diff = ', index - lastDownIndex, ' day: ', day
                lastDownIndex = index
                sunIsDown = 1;
            
        index = index + 1
#    print sunVector

#deltaTime = time.time() - currentTime

#print deltaTime
