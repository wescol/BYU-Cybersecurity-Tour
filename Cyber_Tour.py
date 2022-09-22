from ast import For
from curses.ascii import isascii
import subprocess
from xml.sax.xmlreader import InputSource
import climage
from colorama import Fore, Style
from termcolor import cprint
import time
import getpass
import os
import sys
#from ffpyplayer.player import MediaPlayer
#import cv2
from omxplayer.player import OMXPlayer
from glitch_this import ImageGlitcher
from PIL import Image, ImageDraw
import numpy as np
from random import uniform
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #Set GPIO mode to BCM
GPIO.setup(11, GPIO.IN) #Set trigger pin

def play_EcEn(x):
    OMXPlayer('Digital_Embed.mp4', args='--no-osd -o alsa -b')

GPIO.add_event_detect(11, GPIO.FALLING, callback = play_EcEn, bouncetime=100) #This establishes an event listener that will execute if a laser is shot at the target

def idle(): #Matrix 'screensaver'
    subprocess.call(['cmatrix -bs'],shell=True) # this is a resource intensive command, an RPi 3 or newer should handle it without issue

def alert(): #Prints large yellow '-ALERT-'
    cprint(Style.RESET_ALL)
    cprint(Fore.YELLOW + '       ▄████████  ▄█          ▄████████    ▄████████     ███         '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.YELLOW + '      ███    ███ ███         ███    ███   ███    ███ ▀█████████▄     '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.YELLOW + '      ███    ███ ███         ███    █▀    ███    ███    ▀███▀▀██     '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.YELLOW + '      ███    ███ ███        ▄███▄▄▄      ▄███▄▄▄▄██▀     ███   ▀     '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.YELLOW + '██  ▀███████████ ███       ▀▀███▀▀▀     ▀▀███▀▀▀▀▀       ███       ██'.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.YELLOW + '      ███    ███ ███         ███    █▄  ▀███████████     ███         '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.YELLOW + '      ███    ███ ███▌    ▄   ███    ███   ███    ███     ███         '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.YELLOW + '      ███    █▀  █████▄▄██   ██████████   ███    ███    ▄████▀       '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.YELLOW + '                 ▀                        ███    ███                 '.center(os.get_terminal_size().columns), attrs=['blink'])
    print('\n\n\n\n\n')

def inp_detect(): #Prints large light yellow 'INPUT DETECTED'
    cprint(Style.RESET_ALL)
    print('')
    print('')
    print(Fore.LIGHTYELLOW_EX + '     ▄█  ███▄▄▄▄      ▄███████▄ ███    █▄      ███          ████████▄     ▄████████     ███        ▄████████  ▄████████     ███        ▄████████ ████████▄     '.center(os.get_terminal_size().columns))
    print(Fore.LIGHTYELLOW_EX + '    ███  ███▀▀▀██▄   ███    ███ ███    ███ ▀█████████▄      ███   ▀███   ███    ███ ▀█████████▄   ███    ███ ███    ███ ▀█████████▄   ███    ███ ███   ▀███    '.center(os.get_terminal_size().columns))
    print(Fore.LIGHTYELLOW_EX + '    ███▌ ███   ███   ███    ███ ███    ███    ▀███▀▀██      ███    ███   ███    █▀     ▀███▀▀██   ███    █▀  ███    █▀     ▀███▀▀██   ███    █▀  ███    ███    '.center(os.get_terminal_size().columns))
    print(Fore.LIGHTYELLOW_EX + '▄▄  ███▌ ███   ███   ███    ███ ███    ███     ███   ▀      ███    ███  ▄███▄▄▄         ███   ▀  ▄███▄▄▄     ███            ███   ▀  ▄███▄▄▄     ███    ███  ▄▄'.center(os.get_terminal_size().columns))
    print(Fore.LIGHTYELLOW_EX + '▀▀  ███▌ ███   ███ ▀█████████▀  ███    ███     ███          ███    ███ ▀▀███▀▀▀         ███     ▀▀███▀▀▀     ███            ███     ▀▀███▀▀▀     ███    ███  ▀▀'.center(os.get_terminal_size().columns))
    print(Fore.LIGHTYELLOW_EX + '    ███  ███   ███   ███        ███    ███     ███          ███    ███   ███    █▄      ███       ███    █▄  ███    █▄      ███       ███    █▄  ███    ███    '.center(os.get_terminal_size().columns))
    print(Fore.LIGHTYELLOW_EX + '    ███  ███   ███   ███        ███    ███     ███          ███   ▄███   ███    ███     ███       ███    ███ ███    ███     ███       ███    ███ ███   ▄███    '.center(os.get_terminal_size().columns))
    print(Fore.LIGHTYELLOW_EX + '    █▀    ▀█   █▀   ▄████▀      ████████▀     ▄████▀        ████████▀    ██████████    ▄████▀     ██████████ ████████▀     ▄████▀     ██████████ ████████▀     '.center(os.get_terminal_size().columns))
    print(Fore.YELLOW + '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

def hack() -> int: #Aesthetic for "hacking" the system
    code = getpass.getpass('ACCESS TOKEN:')
    print(Style.RESET_ALL)
    if code == 'hax':
        time.sleep(1)
        subprocess.call(['espeak-ng \"Access token received.\" -v mb-us1'],shell=True)
        cprint('\rprocessing...')
        subprocess.call(['espeak-ng \"Processing!\" -v mb-us1'],shell=True)
        for i in range(3):
            subprocess.call(['espeak-ng \"Resolving!\" -v mb-us1'],shell=True)
            time.sleep(1)
        return 1
    else:
        return 0

def access_denied(): #Plays alarm and prints large red blinking 'ACCEDD DENIED'
    for i in range(3):
        for j in range(3):
            os.system('play -nq -t alsa synth 0.6 square 150 synth 0.6 sine fmod 700-100')
        subprocess.call(['espeak-ng \"Intrusion detected.\" -v mb-us1'],shell=True)
    time.sleep(1)
    cprint(Style.RESET_ALL)
    print('')
    print('')
    cprint('   ▄████████  ▄████████  ▄████████    ▄████████    ▄████████    ▄████████      ████████▄     ▄████████ ███▄▄▄▄    ▄█     ▄████████ ████████▄  '.center(os.get_terminal_size().columns), 'red', attrs=['blink'])
    cprint('  ███    ███ ███    ███ ███    ███   ███    ███   ███    ███   ███    ███      ███   ▀███   ███    ███ ███▀▀▀██▄ ███    ███    ███ ███   ▀███ '.center(os.get_terminal_size().columns), 'red', attrs=['blink'])
    cprint('  ███    ███ ███    █▀  ███    █▀    ███    █▀    ███    █▀    ███    █▀       ███    ███   ███    █▀  ███   ███ ███▌   ███    █▀  ███    ███ '.center(os.get_terminal_size().columns), 'red', attrs=['blink'])
    cprint('  ███    ███ ███        ███         ▄███▄▄▄       ███          ███             ███    ███  ▄███▄▄▄     ███   ███ ███▌  ▄███▄▄▄     ███    ███ '.center(os.get_terminal_size().columns), 'red', attrs=['blink'])
    cprint('▀███████████ ███        ███        ▀▀███▀▀▀     ▀███████████ ▀███████████      ███    ███ ▀▀███▀▀▀     ███   ███ ███▌ ▀▀███▀▀▀     ███    ███ '.center(os.get_terminal_size().columns), 'red', attrs=['blink'])
    cprint('  ███    ███ ███    █▄  ███    █▄    ███    █▄           ███          ███      ███    ███   ███    █▄  ███   ███ ███    ███    █▄  ███    ███ '.center(os.get_terminal_size().columns), 'red', attrs=['blink'])
    cprint('  ███    ███ ███    ███ ███    ███   ███    ███    ▄█    ███    ▄█    ███      ███   ▄███   ███    ███ ███   ███ ███    ███    ███ ███   ▄███ '.center(os.get_terminal_size().columns), 'red', attrs=['blink'])
    cprint('  ███    █▀  ████████▀  ████████▀    ██████████  ▄████████▀   ▄████████▀       ████████▀    ██████████  ▀█   █▀  █▀     ██████████ ████████▀  '.center(os.get_terminal_size().columns), 'red', attrs=['blink'])
    cprint(Style.RESET_ALL)
    for i in range(3):
        subprocess.call(['espeak-ng \"Denied!\" -v mb-us1'],shell=True)
        time.sleep(1)

def access_granted(): #Prints large greeen blinking 'ACCESS GRANTED'
    cprint(Style.RESET_ALL)
    print('')
    print('')
    cprint(Fore.LIGHTGREEN_EX + '   ▄████████  ▄████████  ▄████████    ▄████████    ▄████████    ▄████████         ▄██████▄     ▄████████    ▄████████ ███▄▄▄▄       ███        ▄████████ ████████▄  '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.LIGHTGREEN_EX + '  ███    ███ ███    ███ ███    ███   ███    ███   ███    ███   ███    ███        ███    ███   ███    ███   ███    ███ ███▀▀▀██▄ ▀█████████▄   ███    ███ ███   ▀███ '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.LIGHTGREEN_EX + '  ███    ███ ███    █▀  ███    █▀    ███    █▀    ███    █▀    ███    █▀         ███    █▀    ███    ███   ███    ███ ███   ███    ▀███▀▀██   ███    █▀  ███    ███ '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.LIGHTGREEN_EX + '  ███    ███ ███        ███         ▄███▄▄▄       ███          ███              ▄███         ▄███▄▄▄▄██▀   ███    ███ ███   ███     ███   ▀  ▄███▄▄▄     ███    ███ '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.LIGHTGREEN_EX + '▀███████████ ███        ███        ▀▀███▀▀▀     ▀███████████ ▀███████████      ▀▀███ ████▄  ▀▀███▀▀▀▀▀   ▀███████████ ███   ███     ███     ▀▀███▀▀▀     ███    ███ '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.LIGHTGREEN_EX + '  ███    ███ ███    █▄  ███    █▄    ███    █▄           ███          ███        ███    ███ ▀███████████   ███    ███ ███   ███     ███       ███    █▄  ███    ███ '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.LIGHTGREEN_EX + '  ███    ███ ███    ███ ███    ███   ███    ███    ▄█    ███    ▄█    ███        ███    ███   ███    ███   ███    ███ ███   ███     ███       ███    ███ ███   ▄███ '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.LIGHTGREEN_EX + '  ███    █▀  ████████▀  ████████▀    ██████████  ▄████████▀   ▄████████▀         ████████▀    ███    ███   ███    █▀   ▀█   █▀     ▄████▀     ██████████ ████████▀  '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Fore.LIGHTGREEN_EX + '                                                                                              ███    ███                                                            '.center(os.get_terminal_size().columns), attrs=['blink'])
    cprint(Style.RESET_ALL)
    subprocess.call(['espeak-ng \"Credentials accepted!\" -v mb-us1'],shell=True)
    time.sleep(5)

def interp_as_ascii(inp_string): #Assumes inp_string is a binary number and returns the ASCII interpretation thereof
    check = 1
    bin_num = ""
    ascii_str = ""
    for x in inp_string:
        bin_num += x
        if check % 8 == 0 and not check == 0:
            ascii_str += chr(int(bin_num,2))
            bin_num = ""
        check += 1
    return(ascii_str)

def bit_flip(inp_string): #Assumes inp_string is a binary number and returns the number with all bits flipped
    check = 1
    bin_num = ""
    flip_str = ""
    for x in inp_string:
        bin_num += x
        if check % 8 == 0 and not check == 0:
            flip_str += str('{0:08b}'.format(~int(bin_num, 2) & 255))
            bin_num = ""
        check += 1
    return(flip_str)    

def bit_shift(inp_string: str, shift: int, lor): #Assumes inp_string is a a binary number, takes shift steps, determines left or right shift, then returns the number shifted
    if lor == 'l':
        return shift_left(inp_string, shift)
    elif lor == 'r':
        return int(inp_string, 2) >> shift
    else:
        cprint(Fore.RED + "Bit Shifting Error: shift direction undefined. Original number returned.")
        return(inp_string) 

def shift_left(inp: str) -> str: #FIX ME
    shift = input(Fore.LIGHTGREEN_EX + 'Number of bits to shift LEFT: ' + Fore.WHITE)
    bad_shift = True
    while bad_shift:
        if shift > len(inp): 
            cprint(Fore.LIGHTRED_EX + 'Input number exceeds object length, please enter a smaller number.')
            shift = input(Fore.LIGHTGREEN_EX + 'Number of bits to shift LEFT: ' + Fore.WHITE)
        else:
            break
    return inp[shift:] + ('0' * shift)

def shift_right(inp: str) -> str: #FIX ME
    shift = input(Fore.LIGHTGREEN_EX + 'Number of bits to shift RIGHT: ' + Fore.WHITE)
    bad_shift = True
    while bad_shift:
        if shift > len(inp): 
            cprint(Fore.LIGHTRED_EX + 'Input number exceeds object length, please enter a smaller number.')
            shift = input(Fore.LIGHTGREEN_EX + 'Number of bits to shift RIGHT: ' + Fore.WHITE)
        else:
            break
    return inp[:len(inp) - shift] + ('0' * shift)

def bit_operations(inp_string): #Lists bitwise operation options
    temp_bin = int(inp_string, 2)
    cprint(Fore.LIGHTGREEN_EX + 'Bitwise Operations:')
    options = ['Flip Bits', 'Shift Bits Left', 'Shift Bits Right', 'Return to Decryption Options']
    for tool in options:
        cprint(str(options.index(tool) + 1) + " - " + Fore.YELLOW + tool, end='\t')
        cprint('')
    select = input(Fore.LIGHTGREEN_EX + 'Select an operation: ' + Fore.WHITE)
    if select == '1':
        return bit_flip(inp_string)
    elif select == '2':
        return shift_left(inp_string)
    elif select == '3':
        return shift_right(inp_string)
    else:
        return inp_string

def alpha_shift_up(inp_string: str) -> str: #Converts string to ASCII values then adds shift value from each character and returns string
    shift_num = input(Fore.LIGHTGREEN_EX + 'Shift how many steps?' + Fore.WHITE)
    shift_str = ''
    temp_num = -1
    for ch in inp_string:
        temp_num = ord(ch)
        temp_num += shift_num
        shift_str + chr(temp_num)
    return shift_str

def alpha_shift_down(inp_string: str) -> str: #Converts string to ASCII values then subtracts shift value from each character and returns string
    shift_num = input(Fore.LIGHTGREEN_EX + 'Shift how many steps?' + Fore.WHITE)
    shift_str = ''
    temp_num = -1
    for ch in inp_string:
        temp_num = ord(ch)
        temp_num -= shift_num
        shift_str + chr(temp_num)
    return shift_str

def deobfuscate(inp_string: str) -> str: #Options for manipulating alphanumeric values of input string
    cprint(Fore.LIGHTGREEN_EX + 'Deobfuscator Operations:')
    options = ['Shift Alpha Up', 'Shift Alpha Down', 'Return to Decryption Options']
    for tool in options:
        cprint(str(options.index(tool) + 1) + " - " + Fore.YELLOW + tool, end='\t')
        cprint('')
    select = input(Fore.LIGHTGREEN_EX + 'Select an operation: ' + Fore.WHITE)
    if select == '1':
        return alpha_shift_up(inp_string)
    elif select == '2':
        return alpha_shift_down(inp_string)
    else:
        return inp_string
    
def decrypter(inp_file): #Presents options for decrypting an input file
    try:
        file = open(inp_file, 'r')
        contents = file.read()
        cprint('')
        for char in contents:
            cprint(Fore.WHITE + char, end='')
            sys.stdout.flush()
            time.sleep(uniform(0,0.01))
        cprint('')
        cprint('')
        options = ['ASCII Interpreter', 'Alphabet Deobfuscator', 'Bit Operations', 'Return to files']
        
        temp_str = contents #This variable should only be manipulated by 'options' that perform operations, not interpretations
        while file.closed == False:
            try:
                cprint(Fore.LIGHTGREEN_EX + 'Decryption options:')
                for tool in options:
                    cprint(str(options.index(tool) + 1) + " - " + Fore.YELLOW + tool, end='\t')
                cprint('')
                select = input(Fore.LIGHTGREEN_EX + 'Select a decryption option: ' + Fore.WHITE)
                if select == '1':
                    cprint('')
                    cprint(interp_as_ascii(temp_str))
                    cprint('')
                elif select == '2':
                    cprint('')
                    cprint(deobfuscate(temp_str))
                    cprint('')
                elif select == '3':
                    cprint('')
                    temp_str = bit_operations(temp_str)
                    cprint(Fore.LIGHTGREEN_EX + "File contents following bitwise operation:")
                    cprint('')
                    for char in temp_str:
                        cprint(Fore.WHITE + char, end='')
                        sys.stdout.flush()
                        time.sleep(uniform(0,0.01))
                    cprint('')
                    cprint('')
                elif select == '4':
                    try:
                        file.close() #Close file and return to file selection
                    except IOError:
                        cprint('')
                        cprint(Fore.RED + 'File is already closed or failed to close.')  
                        cprint('')  
                else:
                    cprint('')
                    print('Invalid Operation')
                    cprint('')
            except:
                cprint('')
                cprint('Operation failed. Was the tool incorrect for the file type?')
                cprint('')
    except:
        cprint('')
        cprint('Invalid selection')
        cprint('')
    cprint('')

def play_video_v2(inp_vid): #Plays input video
    subprocess.call(['ffplay -vcodec h264 -fs -noborder -autoexit ' + inp_vid], shell=True)

def play_video_v3(inp_vid): #Plays input video (optimised for raspberry pi)
    OMXPlayer(inp_vid, args='--no-osd -o alsa -b')

def browse_files(): #Ciphers that are solvable with separate physical "cheat-sheet" (see READ.ME)
    print(chr(27) + "[2J")
    subprocess.call(['espeak-ng \"These, are protected files.\" -v mb-us1'],shell=True)
    cprint(Fore.RED + ' - All files are encrypted - '.center(os.get_terminal_size().columns))
    cprint(Fore.RED + ' - Files must be decrypted before they can be read - '.center(os.get_terminal_size().columns))
    view_files = True
    docs = os.listdir('files') #scans files in '/files' and returns a list of available files
    cprint('')
    while view_files:
        cprint(Fore.LIGHTGREEN_EX + 'Files in LOCAL:')
        cprint('')
        for file in docs:
            cprint(Fore.WHITE + str(docs.index(file) + 1) + " - " + Fore.YELLOW + file)
        cprint(Fore.WHITE + "0 - " + Fore.YELLOW + "Quit")
        cprint('')
        select = input(Fore.LIGHTGREEN_EX + 'Select an option: ' + Fore.WHITE)
        if select == '0':
            break
        else:
            try:
                decrypter('files/' + docs[int(select) - 1])
            except:
                cprint('')
                cprint('Invalid Selection')
                cprint('')
        
def hello_world(): #War Games easteregg
        print(chr(27) + "[2J")
        for x in 'GREETINGS PROFESSOR FALKEN.':
            cprint(Fore.LIGHTBLUE_EX + x, end='')
            sys.stdout.flush()
            time.sleep(0.03)
        subprocess.call(['espeak-ng \"GREETINGS, PROFESSOR, FALLKEN.\" -v mb-us1 -p 0'],shell=True)
        cprint('')
        cprint('')
        inp = input(Fore.LIGHTBLUE_EX + '')
        if inp == '07734' or inp == '01134':
            cprint('')
            for x in 'A STRANGE GAME.':
                cprint(Fore.LIGHTBLUE_EX + x, end='')
                sys.stdout.flush()
                time.sleep(0.03)
            subprocess.call(['espeak-ng \"STRANGE GAME.\" -v mb-us1 -p 0'],shell=True)
            time.sleep(0.5)
            cprint('')
            for x in 'THE ONLY WINNING MOVE IS':
                cprint(Fore.LIGHTBLUE_EX + x, end='')
                sys.stdout.flush()
                time.sleep(0.03)
            cprint('')
            for x in 'NOT TO PLAY.':
                cprint(Fore.LIGHTBLUE_EX + x, end='')
                sys.stdout.flush()
                time.sleep(0.03)
            subprocess.call(['espeak-ng \"THE, ONLY WINNING MOVE IS, NOT TO PLAY.\" -v mb-us1 -p 0'],shell=True)
            time.sleep(1.5)
            cprint('')
            for x in 'HOW ABOUT A NICE GAME OF CHESS?':
                cprint(Fore.LIGHTBLUE_EX + x, end='')
                sys.stdout.flush()
                time.sleep(0.03)
            subprocess.call(['espeak-ng \"HOW, ABOUT A NICE, GAME OF, CHESS?\" -v mb-us1 -p 0'],shell=True)
            time.sleep(2)
        else:
            for x in 'WOULDN\'T YOU PERFER A NICE GAME OF CHESS?':
                cprint(Fore.LIGHTBLUE_EX + x, end='')
                sys.stdout.flush()
                time.sleep(0.03)
            subprocess.call(['espeak-ng \"WOULDN\'T YOU PERFER A NICE GAME OF CHESS?\" -v mb-us1 -p 0'],shell=True)
            time.sleep(2)

def custom_cmd(): #konami code entrypoint up, up, down, down, left, right, left, right, B, A
    print(chr(27) + "[2J")
    cmd = input(Fore.LIGHTGREEN_EX + 'Enter command: ' + Fore.WHITE)
    cprint(Fore.LIGHTGREEN_EX + 'Interpretting input...')
    for char in cmd:
        if char == '8':
            cprint(Fore.WHITE + '🡹', end=' ')
        elif char == '2':
            cprint(Fore.WHITE + '🡻', end=' ')
        elif char == '4':
            cprint(Fore.WHITE + '🡸', end=' ')
        elif char == '6':
            cprint(Fore.WHITE + '🡺', end=' ')
        elif char == '9':
            cprint(Fore.WHITE + '🅐', end=' ')
        elif char == '7':
            cprint(Fore.WHITE + '🅑', end=' ')
        else:
            cprint(Fore.WHITE + '?', end=' ')
        sys.stdout.flush()
        time.sleep(uniform(0.07,.3))
    cprint('')
    time.sleep(2)
    if cmd == '8822464679': #Konami code
        #subprocess.Popen(['mpg123', '-q', 'frog.mp3']).wait()
        subprocess.call(['espeak-ng \"Custom command accepted!\" -v mb-us1'],shell=True)
        time.sleep(1)
        subprocess.call([f'python pyfrogger.py'],shell=True) #Frogger easteregg
    else:
        cprint(Fore.LIGHTRED_EX + 'Invalid command.')
        time.sleep(2)

def run_tour_v2(): #Runs tour for both Cybersecurity and EcEn - Cybersecurity should use numpad inputs while EcEn can use the laser to run the tour.
    idling = True
    while idling: #while loop meant to loop infinitely for tours
        idle()
        print(chr(27) + "[2J")
        hacker_img = climage.convert('kosmo.jpg', is_unicode=True) #code for printing image to terminal
        cprint(hacker_img)
        subprocess.call(['espeak-ng -v mb-us1 \"Well come. We have been expecting you.\"'],shell=True)
        time.sleep(0.2)
        cprint(Fore.LIGHTGREEN_EX + '    - MENU -')
        cprint(Fore.LIGHTGREEN_EX + '1 - cyber_introduction')
        cprint(Fore.LIGHTGREEN_EX + '2 - ecen_introduction')
        cprint(Fore.LIGHTGREEN_EX + '3 - local_files')
        cprint(Fore.LIGHTGREEN_EX + '4 - hello_world')
        #cprint(Fore.LIGHTGREEN_EX + '5 - custom_entry')
        cprint(Fore.LIGHTGREEN_EX + '0 - exit')
        cprint('')
        select = getpass.getpass("Select program, then press ENTER: ")
        if select == '1': #Plays the tour video. File name must match that of video. Assumed file type is MP4
            play_video_v3('Cybersecurity_Final.mp4') #THIS IS WHERE YOU CHANGE THE VIDEO FILE NAME IF NECESSARY
        elif select == '2':
            cprint(Fore.RED + 'Shoot the target!!', attrs=['blink'])
        elif select == '3':
            browse_files()
        elif select == '4':
            hello_world()
        elif select == 'unimplemented': #War Games easteregg
            entry = hack()
            if entry:
                access_granted()
                if entry == 1:
                    kosmos_prog()
                if entry == 2:
                    cprint('Surprise!')
            else:
                access_denied()
                continue
        elif select == 'work_in_progress': #Allows for 'custom' inputs that resemble a gamepad (for Konami code input)
            custom_cmd()
        elif select == '159': #Verifone easteregg
            print(chr(27) + "[2J")
            cprint(Fore.YELLOW + 'WARNING:', end=' ')
            time.sleep(1)
            cprint(Fore.LIGHTGREEN_EX + 'Program mismatch.')
            time.sleep(1)
            for char in "This isn\'t a Verifone system!":
                cprint(Fore.WHITE + char, end='')
                sys.stdout.flush()
                time.sleep(uniform(0,0.07))
            time.sleep(2)
        elif select == '404':
            print(chr(27) + "[2J")
            cprint(Fore.RED + "ERROR:", end=" ")
            time.sleep(1)
            cprint(Fore.WHITE + "Not found!")
            time.sleep(3)
        elif select == '1337': #'L33t' easteregg
            print(chr(27) + "[2J")
            alert()
            for char in "Looks like we\'ve got a":
                cprint(Fore.WHITE + char, end='')
                sys.stdout.flush()
                time.sleep(uniform(0,0.07))
            cprint(Fore.RED + ' REAL ', attrs=['blink'], end="")
            for char in "hacker over here":
                cprint(Fore.WHITE + char, end='')
                sys.stdout.flush()
                time.sleep(uniform(0,0.07))
            cprint(' ')
            subprocess.call(['espeak-ng \"Looks like we\'ve got a REAL, hacker over here." -v mb-us1'],shell=True)
            time.sleep(1)
            for char in "L00k 4t y()u 4nd y0u23 f4ncy l33t 5p34k":
                cprint(Fore.WHITE + char, end='')
                sys.stdout.flush()
                time.sleep(uniform(0,0.07))
            subprocess.call(['espeak-ng \"Look at you and your fancy leet speak." -v mb-us1'],shell=True)
            time.sleep(1)
            cprint('')
            for char in "W311 6u355 wh47?":
                cprint(Fore.WHITE + char, end='')
                sys.stdout.flush()
                time.sleep(uniform(0,0.07))
            subprocess.call(['espeak-ng \"Well guess what." -v mb-us1'],shell=True)
            time.sleep(1)
            cprint('')
            for char in "411 y0u'23 b453 423 b3l()n6 t0 u5":
                cprint(Fore.WHITE + char, end='')
                sys.stdout.flush()
                time.sleep(uniform(0,0.07))
            subprocess.call(['espeak-ng \"All your base are belawng to us." -v mb-us1'],shell=True)
            time.sleep(3)
        elif select == '0':
            cprint(Fore.LIGHTGREEN_EX + 'Re-enterring stasis', end='')
            time.sleep(0.5)
            continue
        else:
            cprint(Fore.LIGHTGREEN_EX + 'Program not recognized.')
            time.sleep(0.5)
            cprint(Fore.LIGHTGREEN_EX + 'Re-enterring stasis', end='')
            time.sleep(0.5)
            for char in "...":
                cprint(Fore.WHITE + char, end='')
                sys.stdout.flush()
                time.sleep(1)            
        print(chr(27) + "[2J")
            
run_tour_v2()

# book with hints or eastereggs?
# catch Kosmo doing something sp00ky?
# Kosmo interracts end of video to say something?
# female voice instead of male voice?
# storyline? 2 different stations?
# history of cybersecurity?
# escape rooms puzzles? Cryptography puzzles? Eastereggs!
