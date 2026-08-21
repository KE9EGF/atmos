running = True
while running:
    try:
        try:
            # Packages my beloved
            import sys
            import rich
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
        
        while True:
            mainScreen = rich.panel.Panel("""
            """, title="Press the corresponding key to view an RSS feed.", title_align='center', subtitle="Press Q to quit, or E to return to this menu.", subtitle_align='center')

            print(mainScreen)
            break
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()