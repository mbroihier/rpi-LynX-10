# rpi-LynX-10

This code is installed on a Raspberry Pi 3 running Rasbian (4.1.18-v7).

It assumes that the user account installing the application has sudo privileges.

Edit the Makefile DEST variable to point to the location where the application is to be installed. Then do:

~~~~
make install
~~~~

This command will build the server, create an application run directory, copy the files needed to the run directory, install entries into the crontab, and start the x10_server and x10lights daemons.

# What this application does

The application, as configured, turns on a set of lights at my house at sunset and turns them off at 11:00 PM.  It does this by talking to a LynX-10 x10 controller I have at the house that talks to various x10 modules plugged into my house's outlets and switches.  The Raspberry Pi uses a serial connection to the LynX-10 that is RS-232 running at 1200 BAUD.  Coming off of my Raspberry Pi 3, I have a USB to RS-232 converter.  The x10_server configures the RS-232 via /dev/ttyUSB0 (note that this may have to change before running make install if the serial device is not at the same location) and sends commands received from x10Clients that send LynX-10 commands stored in control files (eg the files on and off in this project directory).  A Perl daemon, x10lights, sends "on" commands via the x10Client when sunset is detected (sunset is specified in the file sunset.txt). Cron runs x10Client instances at 11 PM each day to turn off the lights.

I have apps on my i and Android devices that can send on and off commands to x10_server running on the Pi so that I can turn the lights on and off manually.

This is a very old system.  I built it back in 1998 and it was orignally controlled by a 486 machine that I had that was running Red Hat Linux.  This was eventually replaced by a Pentium, Pentium II, and then a fitPC.  Although old, it still works and as I mentioned above, I now have apps I've built for Apple and Android devices sending commands to this server over my private home network.

I've included a tool, sunRiseSet.py, that will creat a replacement sunset.txt file that is tailored to a location.  This tool isn't perfect.  It's based on a circular earth orbit and a spherical earth.  To generate a sunset.txt file do this:

~~~~
./sunRiseSet.py <lat> <long> >sunset.txt
~~~~

where the parameters are latitude (+ North) and longitude (+ East) in degrees.  For me, the following is close enough (North Dallas area):

~~~~
./sunRiseSet.py 33 -97 >sunset.txt
~~~~

When the tool finishes, copy sunset.txt over the the installed version and kill x10lights.  The process will be restarted by the cron entires installed via make.