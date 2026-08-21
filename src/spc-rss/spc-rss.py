# Packages my beloved
try:
    import os, sys
    import rich
    import threading
    import httpx as hx
    import feedparser as fp
    import readchar as rc
    from time import sleep
    from tqdm import tqdm
    from rich import print
    from rich.panel import Panel
except ImportError as e:
    print("Imports failed. Please ensure all libraries are installed.")
    print(e)
    sleep(2)
    sys.exit()

# RSS Links
WW_RSS = "http://www.spc.noaa.gov/products/spcwwrss.xml"
PDS_RSS = "http://www.spc.noaa.gov/products/spcpdswwrss.xml"
MD_RSS = "http://www.spc.noaa.gov/products/spcmdrss.xml"
AC_RSS = "http://www.spc.noaa.gov/products/spcacrss.xml"
MB_RSS = "http://www.spc.noaa.gov/products/spcmbrss.xml"
FW_RSS = "http://www.spc.noaa.gov/products/spcfwrss.xml"

# Setting Screens
mainScreen = rich.panel.Panel("""""", title="Press the corresponding key to view an RSS feed.", title_align='center', subtitle="Press Q to quit, or E to return to this menu.", subtitle_align='center')

# Functions
def cprint(chars):
    print(f'\r{chars}', end="")

def keyListener():
    while True:
        key = rc.readkey()
        if key == "q":
            sys.exit()
        elif key == "e":
            cprint(mainScreen)

# Making a thread for background key detection
keyThread = threading.Thread(target=keyListener)

# Main Sequence
running = True
while running:
    try:
        keyThread.start()
        while True:
            print(f'\r{mainScreen}', end="")
            break
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()

