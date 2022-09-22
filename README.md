<strong>This is an ongoing project for the BYU Cybersecurity major.
Its purpose is to provide an engaging experience for potential  and
current students through video tours, games, and puzzles both apparent
and hidden via eastereggs.</strong>

<h2>Installation insrtuctions:</h2>

'run_tour.sh' needs to be made executable via 'chmod +x run_tour.sh'
 
After 'run_tour.sh' is made executable, create a cron job so that
'run_tour.sh' executes each time the system starts for plug-and-play
ease of use

If file names need to be updated or are changed, they need to be
updated in Cyber_Tour.py under the 'run_tour_v2()' function. Some
adjustments to the codec may need to be made in order for proper
playback. (Search 'ffmpeg codec' online for more info)

Creating the cron job can be done via the following commands:

crontab -e

@reboot sh /home/'<user>'/Cyber-Tour/run_tour.sh


The cheat sheet is attached as a PDF and should be near the tour station.
It gives hints to how ciphers function, and how to solve the included ciphers.

<h2>Other notes and references:</h2>

The 'Frogger' files (data directory and .py files that aren't Cyber_Tour.py)
were downloaded from https://sourceforge.net/projects/pyfrogger/ and are open source.
Further information concerning this project can be found in 'read-me.rtf'
