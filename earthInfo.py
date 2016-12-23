
import datetime
import calendar
import math
import homogeneoustransforms as ht

radius = 6371.0 #km 
distanceToSun = 149597890.0 # km
tiltRelativeToTheSunEarthPlane = 24.5 * math.pi / 180 # radians
oneDay = 23 * 3600 + 56 * 60 + 4 # seconds relative to an "inertial" (fixed start) frame
oneYear = calendar.timegm(datetime.datetime.strptime("6/21/2017:04:24","%m/%d/%Y:%H:%M").timetuple()) - calendar.timegm(datetime.datetime.strptime("6/20/2016:22:34","%m/%d/%Y:%H:%M").timetuple());

solarPlane = ht.vector(distanceToSun,0,0)

def equator ():
    points = [ [0,0,0] for i in range(0,3600*24)]
    delta = 2 * math.pi / (3600*24)
    angle = 0
    for i in range(0,3600*24):
        points[i] = [math.cos(angle)*radius, math.sin(angle)*radius, 0]
        angle += delta
    return(points)
            

def primeMeridian ():
    points = [ [0,0,0] for i in range(0,3600*24)]
    delta = 2 * math.pi / (3600*24)
    angle= 0
    for i in range(0,3600*24):
            points[i] = [math.cos(angle)*radius, 0, math.sin(angle)*radius]
            angle += delta
    return(points)
            
def latitude (lat):
    points = [ [0,0,0] for i in range(0,3600*24)]
    delta = 2 * math.pi / (3600*24)
    angle = 0
    z = radius * math.sin(lat)
    minorRadius = radius * math.cos(lat)
    for i in range(0,3600*24):
        points[i] = [math.cos(angle)*minorRadius, math.sin(angle)*minorRadius, z]
        angle += delta
    return(points)
            
def solarDisk ():
    points = [ [0,0,0] for i in range(0,3600*24)]
    delta = 2 * math.pi / (3600*24)
    angle= 0
    for i in range(0,3600*24):
            points[i] = [0,math.cos(angle)*radius, math.sin(angle)*radius]
            angle += delta
    return(points)
            
    
