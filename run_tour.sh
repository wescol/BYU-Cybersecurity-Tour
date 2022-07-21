#!/bin/sh
apt update
apt -y upgrade
apt install -y python2.7 python3 espeak-ng mbrola-us1 ffmpeg mpg123
pip install --upgrade pip
pip2 install pygame
pip3 install numpy termcolor colorama climage glitch-this wheel moviepy play-mp3
python3 Cyber_Tour.py