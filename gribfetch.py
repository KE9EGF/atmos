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
            "runTimes": [0, 6, 12, 18], # UTC
            "archiveLimit": 9, # Days
            "typeConfig": {
                # SFC and ATM files are stored in .NC format.
                # .NC (NetCDF4) FILES DO NOT HAVE RESOLUTIONS!
                # Stepping is... complicated. They vary with resolution.
                # 2-value: [STEPPING (hours), MAX HOUR]
                # 3-value: [EARLY STEPPING (f<120), LATE STEPPING (f>120), MAX HOUR]
                "atm": {
                    "extension": ".nc",
                    "stepping": [1, 12]
                },
                "goessimpgrb2": {
                    "resolutions": ["0.25°"],
                    "extension": ".grib2",
                    "stepping": [3, 180]
                },
                "pgrb2": {
                    "resolutions": ["0.25°", "0.50°", "1.00°"]
                    "extension": ".grib2"
                },
                "pgrb2b": {
                    
                },
                "pgrb2full": {
                    
                },
                "sfc": {
                    
                },
                "sfluxgrb": {
                    
                },
                "wgne": {
                    
                }
            }
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
            currentDate = currentDT.strftime("%Y%m%d")
            currentDate = int(currentDate)
            
            # Model Selection
            while True:
                time.sleep(0.5)
                print("\nPlease select what model of GRIB you would like.")
                for index, model in enumerate(availableModels):
                    print(f'{index} - {model}')
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

            # Date, Time, and Final Selection for the main file. 
            # TODO: Optimize with pure logic selection and utilise Xarray for regional file selection using 2 pairs of   latitude and longitude to make a quadrant.
            while True:
                rawDateLimit = currentDT - dt.timedelta(modelConfig[availableModels[modelChoice]]["archiveLimit"])
                dateLimit = rawDateLimit.strftime("%Y%m%d")
                dateLimit = int(dateLimit)
                
                print(f'\nPlease select a date for your {modelConfig[availableModels[modelChoice]]["availableTypes"][typeChoice].upper()} {availableModels[modelChoice]} GRIB.')
                dateSelection = input("(YYYY-MM-DD) --> ").replace("-", "")
                dateSelection = int(dateSelection)
                if dateSelection > currentDate:
                    print("\nSorry, we don't support fetching GRIBs from the future.")
                    time.sleep(1)
                if dateSelection < dateLimit:
                    print("\nThe entered date is older than the archive limit")
                    print(f'The earliest accessible {availableModels[modelChoice]} GRIBs are from: {rawDateLimit.strftime("%Y-%m-%d")}')
                    time.sleep(1)
    except KeyboardInterrupt:
        print("\n")
        sys.exit()