#!/bin/bash

sudo apt-get update
sudo apt-get --assume-yes install libpng12-dev
sudo apt-get --assume-yes install python-gpiozero
sudo apt-get --assume-yes install python-pkg-resources
sudo apt-get --assume-yes install python-smbus
git clone https://github.com/vascofazza/gbzattinymonitor.git /home/pi/gbzattinymonitor
chmod 755 /home/pi/gbzattinymonitor/Pngview/pngview
# Insert battery script into rc.local before final 'exit 0'
if ! grep -Fxq "python /home/pi/gbzattinymonitor/monitor.py &" /etc/rc.local
then
sed -i "s/^exit 0/python \/home\/pi\/gbzattinymonitor\/monitor.py \&\\nexit 0/g" /etc/rc.local >/dev/null
fi
