#!/bin/sh
#installs dependencies for Cyber_Tour.py
#apt update
#apt -y upgrade
#apt install -y python2.7 python3 espeak-ng ffmpeg mpg123 #Python dependencies (both 2.7 & 3 are needed), espeak-ng is a TTS engine, ffmpeg plays video, mpg123 is a codec
#cd /home/pi/Cyber-Tour
#git clone https://github.com/numediart/MBROLA.git #MBROLA is a speech synthesis library that allows espeak-ng to sound nice
#cd MBROLA
#make
#cp bin/mbrola /usr/bin/mbrola #allows for mbrola execution
#mkdir /usr/share/mbrola
#sudo git init
#sudo git remote add numlsediart https://github.com/numediart/MBROLA-voices.git
#sudo git fetch numediart
#sudo git checkout numediart/master -- data/us1 #clone mb-us1 voice
#cd data
#cp us1 /usr/share/mbrola/ #move voice to mbrola library
#cd ..
#pip install --upgrade pip
#pip2 install pygame #allows frogger easteregg to run (via python2.7)
#pip3 install numpy termcolor colorama climage glitch-this wheel moviepy play-mp3 #Other libraries/dependencies to support image display and video/audio playback

cd /home/pi/Cyber-Tour
python3 -u Cyber_Tour.py