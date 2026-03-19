while True:
    # Packages, I probably couldn't live without them.
    try:
        try:
            import sys
            import os
            import time
            import tqdm
            import requests as rq
            import xarray as xa
            import datetime as dt
            import numpy as np
            from tqdm import tqdm
        except ImportError as e:
            print("Error: Missing required library.")
            print("Please check that all required libraries are correctly installed.")
            print(e)
            sys.exit()
            
        # Dictionaries, Lists, Variables, and Other Crap. This took so long.
        # MAY REWRITE THIS LATER ON FOR GRIB FILTER SUPPORT!!
        def getStepping(Model, Type, resolution=None):         
            stepping = modelConfig[model]["typeConfig"][type]["stepping"]
            if resolution is None:
                return stepping
            else:
                return stepping[resolution]

        def findNearestValidTime():
            return True
            # Make this.

        
        defaultGRIBType = "GRIB2"
        availableModels = ["GFS", "NAM", "HRRR", "CMC", "ARW"]
        defaultChunkSize = 1028 # kB
        modelConfig = {
            "GFS": {
                "baseUrl": "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/",
                "urlStructure": "gfs.{}/{}/{}", # Date, Run Time, Filename
                "availableTypes": ["ATM", "PGRB2","PGRB2B", "PGRB2FULL", "GOESSIMPGRB2", "SFC", "SFLUXGRB", "WGNE"],
                "runTimes": [0, 6, 12, 18], # UTC
                "archiveLimit": 9, # Days
                "lateSteppingThreshold": 120, # Hours
                "testFiles": ["gfs.t{}z.pgrb2.0p25.f000", "gfs.t{}z.pgrb2.0p25.f384"],
                "typeConfig": {
                    # SFC and ATM files are stored in .NC format.
                    # .NC (NetCDF4) FILES DO NOT HAVE RESOLUTIONS!
                    # Stepping is... complicated. They can vary with resolution.
                    # 1-value: [STEPPING (hours)]
                    # 2-value: [EARLY STEPPING (f<120), LATE STEPPING (f>120)]
                    "ATM": {
                        "resolutions": None,
                        "extension": ".nc",
                        "minHour": 0,
                        "maxHour": 12,
                        "stepping": 1,
                        "analysisSupport": True,
                        "fileName": "gfs.t{}z.atm{}.nc" # Run Time, Forecast Hour
                    },
                    "GOESSIMPGRB2": {
                        "resolutions": ["0p25"],
                        "extension": ".grib2",
                        "minHour": 0,
                        "maxHour": 180,
                        "stepping": 3,
                        "analysisSupport": False,
                        "fileName": "gfs.t{}z.goessimpgrb2.{}.{}" # Run Time, Resolution, Forecast Hour
                    },
                    "PGRB2": {
                        "resolutions": ["0p25", "0p50", "1p00"],
                        "extension": ".grib2",
                        "minHour": 0,
                        "maxHour": 384,
                        "stepping": {
                            "0p25": [1, 3],
                            "0p50": [3, 3],
                            "1p00": [3, 3]
                        },
                        "analysisSupport": True,
                        "fileName": "gfs.t{}z.pgrb2.{}.{}" # Run Time, Resolution, Forecast Hour
                    },
                    "PGRB2B": {
                        "resolutions": ["0p25", "0p50", "1p00"],
                        "extension": ".grib2",
                        "minHour": 0,
                        "maxHour": 384,
                        "stepping": {
                            "0p25": [1, 3],
                            "0p50": [3, 3],
                            "1p00": [3, 3]
                        },
                        "analysisSupport": True,
                        "fileName": "gfs.t{}z.pgrb2b.{}.{}" # Run Time, Resolution, Forecast Hour
                    },
                    "PGRB2FULL": {
                        "resolutions": ["0p50"],
                        "extension": ".grib2",
                        "minHour": 0,
                        "maxHour": 384,
                        "stepping": 3,
                        "analysisSupport": False,
                        "fileName": "gfs.t{}z.pgrb2full.{}.{}" # Run Time, Resolution, Forecast Hour
                    },
                    "SFC": {
                        "resolutions": None,
                        "extension": ".nc",
                        "minHour": 1,
                        "maxHour": 12,
                        "stepping": 1,
                        "analysisSupport": True,
                        "fileName": "gfs.t{}z.sfc.{}" # Run Time, Forecast Hour
                    },
                    "SFLUXGRB": {
                        "resolutions": None,
                        "extension": ".grib2",
                        "minHour": 000,
                        "maxHour": 384,
                        "stepping": [1, 3],
                        "analysisSupport": False,
                        "fileName": "gfs.t{}z.sfluxgrb.{}" # Run Time, Forecast Hour
                    },
                    "WGNE": {
                        "resolutions": None,
                        "extension": ".grib2",
                        "minHour": 3,
                        "maxHour": 180,
                        "stepping": 3,
                        "analysisSupport": False,
                        "fileName": "gfs.t{}z.wgne.{}" # Run Time, Forecast Hour
                        }
                    }
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
                print("\nSelect what model of GRIB you would like.")
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
                    if modelConfirm == "Y":
                        model = availableModels[modelChoice].upper()
                        break
                    elif modelConfirm == "N":
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
                print(f'\nSelect what type of {model} GRIB you want.\n')
                for index, type in enumerate(modelConfig[model]["availableTypes"], start=1):
                    print(f'{index} - {type}')
                try:
                    typeChoice = int(input("--> ").strip()) - 1
                except ValueError:
                    print("\nPlease enter a number.")
                if typeChoice >= 0 and typeChoice < len(modelConfig[model]["availableTypes"]):
                    print(f'\nYou chose {modelConfig[model]["availableTypes"][typeChoice]}. Is this correct?')
                    typeConfirm = input("(Y/N) --> ").strip().upper()
                    if typeConfirm == "Y":
                        type = modelConfig[model]["availableTypes"][typeChoice]
                        break
                    elif typeConfirm == "N":
                        continue
                    else:
                        print("\nReally? You couldn't type Y or N? Butterfingers...")
                        time.sleep(1)
                else:
                    print("Please enter a valid option.")

            # Date Selection
            while True:
                rawDateLimit = currentDT - dt.timedelta(modelConfig[model]["archiveLimit"])
                dateLimit = rawDateLimit.strftime("%Y%m%d")
                dateLimit = int(dateLimit)
                print(f'\nSelect a date for your {type} {model} GRIB.')
                dateSelection = int(input("(YYYY-MM-DD) --> ").replace("-","").strip())
                if dateSelection > currentDate:
                    print("\nSorry, we don't support fetching GRIBs from the future... yet.")
                    time.sleep(1)
                elif dateSelection < dateLimit:
                    print("\nThe entered date is older than the archive limit, or is invalid.")
                    print(f'The earliest accessible {model} GRIBs are from: {rawDateLimit.strftime("%Y-%m-%d")}')
                    time.sleep(1)
                else:
                    print(f'\nYou chose {dateSelection}. Is this correct?')
                    dateConfirm = input("(Y/N) --> ").strip().upper()
                    if dateConfirm == "Y":
                        date = dateSelection
                        break
                    elif dateConfirm == "N":
                        continue
                    else:
                        print("\nReally? You couldn't type Y or N? Butterfingers...")
                        time.sleep(1)
                    
            # Run Time Selection.
            while True:
                index = 0
                print(f'\nPlease select a run time (UTC) for your {type} {model} GRIB.')
                print("REMINDER: THE NWS CAN TAKE UPWARDS OF MULTIPLE HOURS AFTER THE RUN TIME TO FULLY UPLOAD FILES!")
                for runTime in modelConfig[model]["runTimes"]:
                    if runTime > currentHour and dateSelection == currentDate:
                        break
                    else:
                        print(f'{index + 1} - {runTime:02d}:00 UTC')
                    index += 1
                try:
                    timeChoice = int(input("--> "))
                    if timeChoice > index or timeChoice < 0:
                        print("\nPlease select a valid time.")
                        time.sleep(1)
                        continue
                    else:
                        timeChoice -= 1
                        print(f'\nYou chose {modelConfig[model]["runTimes"][timeChoice]:02d}:00. Is this correct?')
                        timeConfirm = input("(Y/N) --> ").strip().upper()
                        if timeConfirm == "Y":
                            time = modelConfig[model]["runTimes"][timeChoice]
                            print(timeChoice)
                            break
                        elif timeConfirm == "N":
                            continue
                        else:
                            print("\nReally? You couldn't type Y or N? Butterfingers...")
                            time.sleep(1)
                except ValueError:
                    print("Please enter a number.")
                    time.sleep(1)
                    
            # Resolution Selection.        
            while True:
                if len(modelConfig[model]["typeConfig"][type]["resolutions"]) == 1:
                    print(f'\nOnly one available resolution for the {type} {model} GRIB. Selecting {modelConfig[model]["typeConfig"][type]["resolutions"][0].replace("p", ".")}°.')
                    break
                elif modelConfig[model]["typeConfig"][type]["resolutions"] == None:
                    print(f'\nResolutions are not available for the {type} {model} GRIB. This may be a .NC file. Proceeding.')
                    break
                print("\nPlease select a resolution.")
                for index, resolution in enumerate(modelConfig[model]["typeConfig"][type]["resolutions"], start=1):
                    print(f'{index} - {resolution.replace("p", ".")}°')
                resChoice = int(input("--> ").strip())
                if resChoice > len(modelConfig[model]["typeConfig"][type]["resolutions"]) or resChoice <= 0:
                    print("Please select a valid resolution.")
                    time.sleep(1)
                    continue
                else:
                    resChoice -= 1
                    print(f'\nYou chose {modelConfig[model]["typeConfig"][type]["resolutions"][resChoice].replace("p", ".")}°. Is this correct?')
                    resConfirm = input("(Y/N) --> ").strip().upper()
                    if resConfirm == "Y":
                        resolution = modelConfig[model]["typeConfig"][type]["resolutions"][resChoice]
                        print(resolution)
                        break
                    elif resConfirm == "N":
                        continue
                    else:
                        print("\nReally? You couldn't type Y or N? Butterfingers...")
                        time.sleep(1)

            # Forecast Hour Selection. This was by far the hardest part to figure out.
            # Yes, I'm using a NumPy array so I can efficiently round entered times
            # to the nearest valid time in the array, cry about it.
            complete = False
            minHour = modelConfig[model]["typeConfig"][type]["minHour"]
            maxHour = modelConfig[model]["typeConfig"][type]["maxHour"]
            time = minHour
            lateSteppingThreshold = modelConfig[model]["lateSteppingThreshold"]
            validTimes = np.array([time])
            while True:
                if complete:
                    print(validTimes)
                    break
                if isinstance(modelConfig[model]["typeConfig"][type]["stepping"], dict):
                    stepping = getStepping(model, type, resolution)
                    np.append(validTimes, time)
                    while True:
                        time += stepping[0]
                        validTimes = np.append(validTimes, time)
                        if time >= lateSteppingThreshold:
                            break
                    while True:
                        time += stepping[1]
                        validTimes = np.append(validTimes, time)
                        if time >= maxHour:
                            complete = True
                            break
                else:
                    stepping = getStepping(model, type)
                    time += stepping
                    validTimes = np.append(validTimes, time)
                    if time >= maxHour:
                        complete = True
                        break
                    # Finish this
                        
    except KeyboardInterrupt:
        print("\n")
        sys.exit()