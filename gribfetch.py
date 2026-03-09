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
            import xarray as xa
            import datetime as dt
            import re
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
            "archiveLimit": 9, # Days
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
        
        # User Input and Conditionals. God this took so long
        running = True
        while running:
            # This is in here to constantly update.
            currentDT = dt.datetime.now()
            year, month, day, hour = currentDT.year, currentDT.month, currentDT.day, currentDT.hour
            
            # Model Selection
            while True:
                time.sleep(0.5)
                print("\nPlease select what model of GRIB you would like.")
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
                    
                if modelChoice >= 0 and modelChoice < 6:
                    print(f'\nYou chose {availableModels[modelChoice]}. Is this correct?')
                    modelConfirm = input("(Y/N) --> ").strip().upper()
                    if modelConfirm == "Y" and modelConfirm.isalpha() and len(modelConfirm) == 1:
                        break
                    elif modelConfirm == "N" and modelConfirm.isalpha() and len(modelConfirm) == 1:
                        continue
                    else:
                        print("\nReally? You couldn't type Y or N? Butterfingers...")
                        time.sleep(1)
                else:
                    print("\nPlease select a valid option.")
                    time.sleep(0.5)
                    continue

            # Type Selection        
            while True:
                print(f'Please select what type of {availableModels[modelChoice]} GRIB you want.\n')
                for index, type in enumerate(modelConfig[availableModels[modelChoice]]["availableTypes"]):
                    print(f'{index} - {type}')
                try:
                    typeChoice = int(input("--> ").strip())
                except ValueError:
                    print("\nPlease enter a number.")
                if typeChoice >= 0 and typeChoice < len(modelConfig[availableModels[modelChoice]]["availableTypes"]) - 1:
                    print(f'\nYou chose {modelConfig[availableModels[modelChoice]]["availableTypes"][typeChoice]}. Is this correct?')
                typeConfirm = input("(Y/N) --> ").strip().upper()
                if typeConfirm == "Y" and typeConfirm.isalpha() and len(typeConfirm) == 1:
                    break
                elif typeConfirm == "N" and typeConfirm.isalpha() and len(typeConfirm) == 1:
                    continue
                else:
                    print("\nReally? You couldn't type Y or N? Butterfingers...")
                    time.sleep(1)

            # Date, Time, and Final Selection for the main file. TODO: Optimize with pure logic selection.
            while True:
                dateLimit = currentDT - dt.timedelta(modelConfig[availableModels[modelChoice]]["archiveLimit"])
                
                print(f'Please select a date for your {modelConfig[availableModels[modelChoice]]["availableTypes"][typeChoice].upper()} {availableModels[modelChoice].upper()} GRIB.')
                dateSelection = input("(YYYY-MM-DD) --> ").split("-")
            
                print(dateSelection)   
                
                print(dateLimit)
                
    except KeyboardInterrupt:
        print("\n")
        sys.exit()