#!/usr/bin/python3
# File name   : setup.py
# Author      : Adeept
# Date        : 2020/3/14
# Modified on 21-12-2020 by Giovanni Bernardo (@Cyb3rn0id)

import os
import time

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)

def replace_num(file,initial,new_num):  
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)

for x in range(1,4):
    if os.system("sudo apt-get update") == 0:
        break

# edited on 31-12-2020 by CyB3rn0id
# commented those 4 lines because takes a lot of time 
# and I've enough space on the microSD card
# os.system("sudo apt-get purge -y wolfram-engine")
# os.system("sudo apt-get purge -y libreoffice*")
# os.system("sudo apt-get -y clean")
# os.system("sudo apt-get -y autoremove")

# for x in range(1,4):
#    if os.system("sudo apt-get -y upgrade") == 0:
#        break

for x in range(1,4):
    if os.system("sudo pip3 install -U pip") == 0:
        break

for x in range(1,4):
    if os.system("sudo apt-get install -y python-dev python-pip libfreetype6-dev libjpeg-dev build-essential") == 0:
        break

for x in range(1,4):
    if os.system("sudo -H pip3 install --upgrade luma.oled") == 0:
        break

for x in range(1,4):
    if os.system("sudo apt-get install -y i2c-tools") == 0:
        break

for x in range(1,4):
    if os.system("sudo pip3 install adafruit-pca9685") == 0:
        break

for x in range(1,4):
    if os.system("sudo pip3 install rpi_ws281x") == 0:
        break

for x in range(1,4):
    if os.system("sudo apt-get install -y python3-smbus") == 0:
        break

for x in range(1,4):
    if os.system("sudo pip3 install mpu6050-raspberrypi") == 0:
        break

for x in range(1,4):
    if os.system("sudo pip3 install flask") == 0:
        break

for x in range(1,4):
    if os.system("sudo pip3 install flask") == 0:
        break

for x in range(1,4):
    if os.system("sudo pip3 install flask_cors") == 0:
        break

for x in range(1,4):
    if os.system("sudo pip3 install websockets") == 0:
        break

try:
    replace_num("/boot/config.txt",'#dtparam=i2c_arm=on','dtparam=i2c_arm=on\nstart_x=1\n')
except:
    print('Riprova')

for x in range(1,4):
    if os.system("sudo pip3 install numpy") == 0:
        break

for x in range(1,4):
    if os.system("sudo pip3 install opencv-contrib-python==3.4.3.18") == 0:
        break

for x in range(1,4):
    if os.system("sudo apt-get -y install libqtgui4 libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqt4-test") == 0:
        break

for x in range(1,4):
    if os.system("sudo pip3 install imutils zmq pybase64 psutil") == 0:   ####
        break

for x in range(1,4):
    if os.system("sudo git clone https://github.com/oblique/create_ap") == 0:
        break

try:
    os.system("cd " + thisPath + "/create_ap && sudo make install")
except:
    pass

try:
    os.system("cd //home/pi/create_ap && sudo make install")
except:
    pass

for x in range(1,4):
    if os.system("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq") == 0:
        break

try:
    os.system('sudo touch //home/pi/startup.sh')
    with open("//home/pi/startup.sh",'w') as file_to_write:
    #you can choose how to control the robot
        file_to_write.write("#!/bin/sh\nsudo python3 " + thisPath + "/server/webServer.py")
#        file_to_write.write("#!/bin/sh\nsudo python3 " + thisPath + "/server/server.py")
except:
    pass

os.system('sudo chmod 777 //home/pi/startup.sh')

replace_num('/etc/rc.local','fi','fi\n//home/pi/startup.sh start')

# edited on 31-12-2020 by CyB3rn0id
# commented those 6 lines because I've not found any conflict at 31-12-2020
# I don't know about what conflict we're talking about, maybe is a thing
# that was solved at the end of 2020 with the latest Raspbian Os release
# try: #fix conflict with onboard Raspberry Pi audio
#    os.system('sudo touch /etc/modprobe.d/snd-blacklist.conf')
#    with open("/etc/modprobe.d/snd-blacklist.conf",'w') as file_to_write:
#        file_to_write.write("blacklist snd_bcm2835")
# except:
#    pass

os.system("sudo cp -f //home/pi/adeept_rasptank/server/config.txt //etc/config.txt")

print('\n\n\n')
print('I programmi sono stati installati.')
print('Puoi spegnere il Raspberry Pi, innestare l\'HAT, collegare i servocomandi in punti qualsiasi dedicati ai servocomandi ed accendere il Raspberry attendendo che i servocomandi si muovano e si portino in posizione centrale.')
print('Dopo aver fatto questo puoi spegnere, scollegare i servocomandi avendo cura di non spostarli e procedere all\'assemblaggio')