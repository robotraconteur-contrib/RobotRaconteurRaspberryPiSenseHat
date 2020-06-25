# Set up instructions for Raspberry Pi Robot Raconteur Sense Hat 

## Set up raspi-config
wget https://archive.raspberrypi.org/debian/pool/main/r/raspi-config/raspi-config_20200601_all.deb -P /tmp

apt-get install libnewt0.52 whiptail parted triggerhappy lua5.1 alsa-utils -y

apt-get install -fy

dpkg -i /tmp/raspi-config_20200601_all.deb
or
dpkg -i raspi-config_20200601_all.deb

Then Run:

sudo raspi-config

select option 5: Interfacing Options

Then Enable I2C and exit

## Install Necessary Libraries
### Clone RTIMULib:

git clone https://github.com/RPi-Distro/RTIMULib/ RTIMU

cd RTIMU/Linux/python

### Follow instruction in RTIMULib/Linux/python:

sudo apt install python3-dev

python setup.py build

python setup.py install

### Install libopenjp2-7:

sudo apt install libopenjp2-7

### Install sense-hat:

sudo apt install sense-hat

## Install Raspberry Pi Sense Hat Emulator

sudo add-apt-repository ppa://waveform/ppa
sudo apt-get update
sudo apt-get install python-sense-emu python3-sense-emu sense-emu-tools
