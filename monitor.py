from smbus import SMBus
from time import sleep
import os
from subprocess import check_output

bus = SMBus(1)
addr = 0x13

# Config
warning = 0
status = 0
PNGVIEWPATH = "/home/pi/gbzattinymonitor/Pngview/"
ICONPATH = "/home/pi/gbzattinymonitor/icons"
CLIPS = 1
REFRESH_RATE = 60
VCC = 4.2
VOLTFULL = 230
VOLT100 = 225
VOLT75 = 212
VOLT50 = 206
VOLT25 = 200
VOLT0 = 190

width = int(check_output("/bin/fbset").split("\n")[1].split("x")[0][6:]) -75
if width < 600:
	width = 649
def read():
	return bus.read_byte(addr)
	#sleep(0.3)
	#b = bus.read_byte(0x13)
	#return b>>8+a

def convertVoltage(val):
    global VCC
    voltage = float(val) * (VCC / 255.0)
    return voltage

def changeicon(percent):
    i = 0
    killid = 0
    os.system(PNGVIEWPATH + "/pngview -b 0 -l 30001" + " -x " + str(width) + " -y 5 " + ICONPATH + "/battery" + percent + ".png &")
    out = check_output("ps aux | grep pngview | awk '{ print $2 }'", shell=True)
    nums = out.split('\n')
    for num in nums:
        i += 1
        if i == 1:
            killid = num
            os.system("sudo kill " + killid)

os.system(PNGVIEWPATH + "/pngview -b 0 -l 299999 -x 650 -y 5 " + ICONPATH + "/blank.png &")

while True:
	val1 = read()
	sleep(2)
	val2 = read()
	sleep(2)
	val3 = read()
	ret = (float(val1+val2+val3)/3.0)
	print ret
	if ret < VOLT0:
		if status != 0:
			print 
			changeicon("0")
			if CLIPS == 1:
				os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattshutdown.mp4 --alpha 160;")
				voltcheck = (read())
				if voltcheck <= VOLT0:
					os.system("sudo shutdown -h now")
				else:
					warning = 0
		status = 0
	elif ret < VOLT25:
		if status != 25:
			changeicon("25")
			if warning != 1:
				if CLIPS == 1:
					os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattalert.mp4 --alpha 160")
				warning = 1
			status = 25
	elif ret < VOLT50:
		if status != 50:
			changeicon("50")
		status = 50
	elif ret < VOLT75:
		if status != 75:
			changeicon("75")
		status = 75
	elif ret < VOLT100:
		if status != 100:
			changeicon("100")
		status = 100
	else:
		if status != -1:
			changeicon("FULL")
		status = -1
	sleep(REFRESH_RATE)
