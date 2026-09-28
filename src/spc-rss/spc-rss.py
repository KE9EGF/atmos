# Packages my beloved
try:
    import os
    import sys
    import threading
    from time import sleep

    import feedparser
    import readchar
    from rich import print as rprint
    from rich.align import Align
    from rich.console import Console
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

# Other Variables
key = ""
running = True
onMainScreen = True
console = Console(width=75)
menuKeys = ["t", "y", "u", "g", "h", "j"]
mainSubtitle = "Press Q to quit, or E to return to the main menu."

# Setting Screens
mainScreenText = """
T - Watches and Status Reports   Y - PDS Watches Only      U - Mesoscale Disc.

G - Convective Outlooks          H - Multimedia Briefings  J - Fire WX Outlooks
"""
mainScreen = Panel(
    Align.center(mainScreenText),
    title="SPC-RSS",
    title_align="center",
    subtitle=mainSubtitle,
    subtitle_align="center",
)


# Functions
def keyListener():
    global key, running, onMainScreen
    while running:
        key = readchar.readkey().lower()
        if key == "q":
            running = False
            console.clear()
            os._exit(0)
        elif key == "e":
            console.clear()
            rprint(mainScreen)
            onMainScreen = True
        sleep(0.1)


# Making a thread for background key detection
keyThread = threading.Thread(target=keyListener, daemon=True)
keyThread.start()

# TESTING SECTION
d = feedparser.parse(AC_RSS)
print(d.entries[0].title)
print(d.entries[0].description)

sys.exit()
    
# Main Sequence
while running:
    console.clear()
    rprint(mainScreen)
    try:
        while True:
            if key == "g":
                onMainScreen = False
                currentFeed = "AC"
    except KeyboardInterrupt:
        console.clear()
        sys.exit()



