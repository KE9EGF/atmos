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
        # MAY REWRITE THIS LATER ON FOR GRIB FILTER SUPPORT!!
        defaultGRIBType = "GRIB2"
        availableModels = ["GFS", "ECMWF", "NAM", "HRRR", "CMC", "ARW"]
        defaultChunkSize = 1028 # kB
        modelConfig = {
        "GFS": {
            "baseUrl": "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/",
            "availableTypes": ["atm", "pgrb2","pgrb2b", "pgrb2full", "goessimpgrb2", "sfc", "sfluxgrib", "wgne"],
            "availableExtensions": [".grib2", ".nc"], # SFC and ATM files are stored in .nc format.
            "availableResolutions": ["0p25", "0p50", "1p00"], # Degrees
            "runTimes": [0, 6, 12, 18], # UTC 
            "forecastTimings": { # Corresponds to each type in availableTypes
                # 2-value: [STEPPING (minutes), MAX HOUR] 
                # 3-value: [EARLY STEPPING (<f120), LATE STEPPING (>f120), MAX HOUR]
                "atm": [60, 12],
                "goessimpgrb2": [180, 180],
                "pgrb2": [60, 180, 384],
                "pgrb2b": [60, 180, 384],
                "pgrb2full": [180, 384],
                "sfc": [60, 12],
                "sfluxgrb": [60, 180, 384], 
                "wgne": [180, 180]
            },
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
            time.sleep(0.5)
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
                print("\nPlease enter a number.")
                break
            
            # Model Conditionals, the complicated stuff. This took longer, but was straightforward.
            while True:
                if modelChoice >= 0 and modelChoice < 6:
                    print(f'\nYou chose {availableModels[modelChoice]}. Is this correct?')
                    modelConfirm = input("(Y/N) --> ").strip().upper()
                    if modelConfirm == "Y" and modelConfirm.isalpha() and len(modelConfirm) == 1:
                        break
                    elif modelConfirm == "N" and modelConfirm.isalpha() and len(modelConfirm) == 1:
                        break
                    else:
                        print("\nReally? You couldn't type Y or N? Butterfingers...")
                        time.sleep(1)
                else:
                    print("\nPlease select a valid option.")
                    time.sleep(0.5)
                    break

            
    except KeyboardInterrupt:
        sys.exit()