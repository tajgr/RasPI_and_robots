SICKinit
The skript is a specilal debian (?) init skript.
This skript runs the main program SICK2014_main.py

It have to be plased in /etc/init.d/
Usage:
for testing:
    sudo /etc/init.d/SICKinit {start|stop}
Register script to be run at start-up:
    sudo update-rc.d SICKinit defaults
    
For remove the script from start-up:
    sudo update-rc.d -f SICKinit  remove
    
More info: http://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html
           https://wiki.debian.org/LSBInitScripts