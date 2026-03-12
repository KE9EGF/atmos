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
        def getStepping(model, type, resolution=None):         
            stepping = modelConfig[model][typeConfig][type][stepping]
            if resolution is None:
                return stepping
            else:
                return stepping[resolution]
        defaultGRIBType = "GRIB2"
        availableModels = ["GFS", "ECMWF", "NAM", "HRRR", "CMC", "ARW"]
        defaultChunkSize = 1028 # kB
        modelConfig = {
            "GFS": {
                "baseUrl": "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/",
                "availableTypes": ["atm", "pgrb2","pgrb2b", "pgrb2full", "goessimpgrb2", "sfc", "sfluxgrb", "wgne"],
                "runTimes": [0, 6, 12, 18], # UTC
                "archiveLimit": 9, # Days
                "lateSteppingThreshold": 120, # Hours
                "typeConfig": {
                    # SFC and ATM files are stored in .NC format.
                    # .NC (NetCDF4) FILES DO NOT HAVE RESOLUTIONS!
                    # Stepping is... complicated. They vary with resolution.
                    # 1-value: [STEPPING (hours)]
                    # 2-value: [EARLY STEPPING (f<120), LATE STEPPING (f>120)]
                    "atm": {
                        "resolutions": None,
                        "extension": ".nc",
                        "minHour": 0,
                        "maxHour": 12,
                        "stepping": 1,
                        "analysisSupport": True,
                        "fileName": "gfs.t{run}z.atm{fhr}.nc"
                    },
                    "goessimpgrb2": {
                        "resolutions": ["0p25"],
                        "extension": ".grib2",
                        "minHour": 000,
                        "maxHour": 180,
                        "stepping": 3,
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}.goessimpgrb2.{res}.{fhr}"
                    },
                    "pgrb2": {
                        "resolutions": ["0p25", "0p50", "1p00"],
                        "extension": ".grib2",
                        "minHour": 000,
                        "maxHour": 384,
                        "stepping": {
                            "0p25": [1, 3],
                            "0p50": 3,
                            "1p00": 3
                        },
                        "analysisSupport": True,
                        "fileName": "gfs.t{run}z.pgrb2.{res}.{fhr}"
                    },
                    "pgrb2b": {
                        "resolutions": ["0p25", "0p50", "1p00"],
                        "extension": ".grib2",
                        "minHour": 000,
                        "maxHour": 384,
                        "stepping": {
                            "0p25": [1, 3],
                            "0p50": 3,
                            "1p00": 3
                        },
                        "analysisSupport": True,
                        "fileName": "gfs.t{run}z.pgrb2b.{res}.{fhr}"
                    },
                    "pgrb2full": {
                        "resolutions": ["0p50"],
                        "extension": ".grib2",
                        "minHour": 000,
                        "maxHour": 384,
                        "stepping": 3,
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}z.pgrb2full.{res}.{fhr}"
                    },
                    "sfc": {
                        "resolutions": None,
                        "extension": ".nc",
                        "minHour": 1,
                        "maxHour": 12,
                        "stepping": 1,
                        "analysisSupport": True,
                        "fileName": "gfs.t{run}z.sfc{fhr}"
                    },
                    "sfluxgrb": {
                        "resolutions": None,
                        "extension": ".grib2",
                        "minHour": 000,
                        "maxHour": 384,
                        "stepping": [1, 3],
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}z.sfluxgrb{fhr}"
                    },
                    "wgne": {
                        "resolutions": None,
                        "extension": ".grib2",
                        "minHour": 3,
                        "maxHour": 180,
                        "stepping": 3,
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}s.wgne.{fhr}"
                        }
                    }
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
        
        # User Input and Conditionals. God this took so long.
        running = True
        while running:
            # This is in here to constantly update.
            # THESE ARE ALL IN UTC TIME!
            currentDT = dt.datetime.now(dt.timezone.utc)
            currentDate = currentDT.strftime("%Y%m%d")
            currentDate = int(currentDate)
            currentTime = currentDT.strftime("%H%M")
            currentTime = int(currentTime)
            currentHour, currentMinute = currentDT.strftime("%H"), currentDT.strftime("%M")
            currentHour, currentMinute = int(currentHour), int(currentMinute)
            
            
            
            # Model Selection
            while True:
                time.sleep(1)
                print("\nPlease select what model of GRIB you would like.")
                for index, model in enumerate(availableModels, start=1):
                    print(f'{index} - {model}')
                try:
                    modelChoice = int(input("--> ").strip())
                except ValueError:
                    print("\nPlease enter a number.")
                modelChoice -= 1
                if modelChoice >= 0 and modelChoice <= len(availableModels):
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
                    time.sleep(1)
                    continue

            # Type Selection        
            while True:
                print(f'\nPlease select what type of {availableModels[modelChoice]} GRIB you want.\n')
                for index, type in enumerate(modelConfig[availableModels[modelChoice]]["availableTypes"], start=1):
                    print(f'{index} - {type}')
                try:
                    typeChoice = int(input("--> ").strip())
                except ValueError:
                    print("\nPlease enter a number.")
                typeChoice -= 1
                if typeChoice >= 0 and typeChoice < len(modelConfig[availableModels[modelChoice]]["availableTypes"]):
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
            # TODO (in the future): Optimize with pure logic selection and utilize Xarray for regional file downloading using GRIB filter.
            while True:
                rawDateLimit = currentUnlaggedDT - dt.timedelta(modelConfig[availableModels[modelChoice]]["archiveLimit"])
                dateLimit = rawDateLimit.strftime("%Y%m%d")
                dateLimit = int(dateLimit)
                
                print(f'\nPlease select a date for your {modelConfig[availableModels[modelChoice]]["availableTypes"][typeChoice].upper()} {availableModels[modelChoice]} GRIB.')
                print("REMEMBER: THE NWS TAKES ABOUT 3.5 HOURS TO UPLOAD AND PROCESS GRIB FILES!")
                dateSelection = input("(YYYY-MM-DD) --> ").replace("-", "")
                dateSelection = int(dateSelection)
                if dateSelection > currentDate:
                    print("\nSorry, we don't support fetching GRIBs from the future... yet.")
                    time.sleep(1)
                elif dateSelection < dateLimit:
                    print("\nThe entered date is older than the archive limit")
                    print(f'The earliest accessible {availableModels[modelChoice]} GRIBs are from: {rawDateLimit.strftime("%Y-%m-%d")}')
                    time.sleep(1)
                else:
                    break

            while True:
                index = 0
                print(f'\nPlease select a run time (UTC) for your {modelConfig[availableModels[modelChoice]]["availableTypes"][typeChoice].upper()} {availableModels[modelChoice]} GRIB.')
                for runTime in modelConfig[availableModels[modelChoice]]["runTimes"]:
                    index += 1
                    if runTime > currentDT.hour and dateSelection == currentDate:
                        break
                    print(f'{index} - {runTime:02d}:00 UTC')
                try:
                    timeChoice = int(input("--> "))
                except ValueError:
                    print("Please enter a number.")
                    time.sleep(1)

            while True:
                print("Please select a resolution.")
                for index, resolution in enumerate(modelConfig[availableModels[modelChoice]]["typeConfig"]["availableTypes"[typeChoice]]["resolutions"], start=1):
                    print(f'{index} - {resolution}')
    except KeyboardInterrupt:
        print("\n")
        sys.exit()