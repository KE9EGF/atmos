print("Hello! Welcome to GRIBFETCH!")
while True:
    # Packages, I probably couldn't live without them.
    try:
        try:
            import sys
            import os
            import requests as rq
            import time
            import tqdm
            import datetime as dt
            import xarray as xa
            from tqdm import tqdm
        except ImportError as e:
            print("Error: Missing required library.")
            print("Please check that all required libraries are correctly installed.")
            print(e)
            sys.exit()
            
        # Dictionaries, Lists, Variables, and Other Crap. This took so long.
        defaultGRIBType = "GRIB2"
        availableModels = ["GFS", "ECMWF", "NAM", "HRRR", "CMC", "ARW"]
        defaultChunkSize = 4096
        modelConfig = {
        "GFS": {
            "baseUrl": "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/",
            "availableTypes": ["pgrb2", "pgrb2full", "goessimpgrb2", "sfluxgribf", "wgne", ""],
            "availableExtensions": [".grib2", ".nc"],
            "availableResolutions": [0.25, 0.5, 1],
            "maxForecastHour": 180,
            "forecastStepping": 180,
            "runTimes": [0, 6, 12, 18]
        },
        "ECMWF": {
        
        },
        "NAM": {
            "baseUrl": "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nam/prod/"
        },
        "HRRR": {
            
        },
        "CMC": {
            
        },
        "ARW": {
            
        }
        }
        
        # User Input, just how I like it.
        running = True
        while running:
            time.sleep(1)
            print("\nPlease select what model GRIB you would like.")
            print("""
            0 - GFS
            1 - ECMWF
            2 - NAM
            3 - HRRR
            4 - CMC
            5 - ARW
            \n""")
            try:
                modelChoice = int(input("--> ").strip())
            except ValueError:
                print("Please enter a number.")
                break
            
            # Model Conditionals, the complicated stuff. This took longer.
            if modelChoice >= 0 and modelChoice < 6:
                print(f'You chose {availableModels[modelChoice]}. Is this correct?')
                userModelConfirm = input("(Y/N) --> ").strip().upper()
                if userModelConfirm == "Y":
                    pass
                elif userModelConfirm == "N":
                    continue
                else:
                    print("Really? You couldn't type Y or N? Butterfingers...")
                    time.sleep(1)
            else:
                print("Please select a valid option.")
                break
    except KeyboardInterrupt:
        sys.exit()