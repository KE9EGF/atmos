# TODO: Add models: RAP, NBM, AIGFS, HIRESW.

while True:
    # Packages, I probably couldn't live without them.
    try:
        try:
            import sys
            import os
            import tqdm
            import requests as rq
            import xarray as xa
            import datetime as dt
            import numpy as np
            from time import sleep
            from tqdm import tqdm
        except ImportError as e:
            print("Error: Missing required library.")
            print("Please check that all required libraries are correctly installed.")
            print(e)
            sys.exit()
            
        # Dictionaries, Lists, Variables, and Other Crap. This took so long.
        def getStepping(Model, Type, Resolution=None):         
            stepping = modelConfig[model]["typeConfig"][type]["stepping"]
            if Resolution is None:
                return stepping
            else:
                return stepping[Resolution]
        
        def findNearestValidTime(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]
            
        defaultGRIBType = "GRIB2"
        availableModels = ["GFS", "NAM", "HRRR", "RAP", "HiResW", "AIGFS", "NBM"]
        defaultChunkSize = 1028 # kB
        modelConfig = {
            "GFS": {
                "baseUrl": "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/",
                "urlStructure": "gfs.{}/{}/{}", # Date, Run Time, Filename
                "availableTypes": ["ATM", "PGRB2","PGRB2B", "PGRB2FULL", "GOESSIMPGRB2", "SFC", "SFLUXGRB", "WGNE"],
                "runTimes": [0, 6, 12, 18], # UTC
                "archiveLimit": 9, # Days
                "steppingThresholds": [120], # This is to determine at what forecase hour stepping intervals change
                "testFiles": ["gfs.t{run}z.pgrb2.0p25.f000", "gfs.t{run}z.pgrb2.0p25.f384"],
                "typeConfig": {
                    # SFC and ATM files are stored in .NC format.
                    # .NC (NetCDF4) FILES DO NOT HAVE RESOLUTIONS!
                    "ATM": {
                        "resolutions": None,
                        "extension": ".nc",
                        "minHour": 0,
                        "maxHour": 12,
                        "stepping": [1],
                        "analysisSupport": True,
                        "fileName": "gfs.t{run}z.atm{fhr}.nc" # Run Time, Forecast Hour
                    },
                    "GOESSIMPGRB2": {
                        "resolutions": ["0p25"],
                        "extension": ".grib2",
                        "minHour": 0,
                        "maxHour": 180,
                        "stepping": [3],
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}z.goessimpgrb2.{res}.f{fhr}" # Run Time, Resolution, Forecast Hour
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
                        "fileName": "gfs.t{run}z.pgrb2.{res}.f{fhr}" # Run Time, Resolution, Forecast Hour
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
                        "fileName": "gfs.t{run}z.pgrb2b.{res}.f{fhr}" # Run Time, Resolution, Forecast Hour
                    },
                    "PGRB2FULL": {
                        "resolutions": ["0p50"],
                        "extension": ".grib2",
                        "minHour": 0,
                        "maxHour": 384,
                        "stepping": [3],
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}z.pgrb2full.{res}.f{fhr}" # Run Time, Resolution, Forecast Hour
                    },
                    "SFC": {
                        "resolutions": None,
                        "extension": ".nc",
                        "minHour": 1,
                        "maxHour": 12,
                        "stepping": [1],
                        "analysisSupport": True,
                        "fileName": "gfs.t{run}z.sfc.f{fhr}" # Run Time, Forecast Hour
                    },
                    "SFLUXGRB": {
                        "resolutions": None,
                        "extension": ".grib2",
                        "minHour": 0,
                        "maxHour": 384,
                        "stepping": [1, 3],
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}z.sfluxgrb.f{fhr}" # Run Time, Forecast Hour
                    },
                    "WGNE": {
                        "resolutions": None,
                        "extension": ".grib2",
                        "minHour": 3,
                        "maxHour": 180,
                        "stepping": [3],
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}z.wgne.f{fhr}" # Run Time, Forecast Hour
                        }
                    }
                },
            "NAM": {
                "baseUrl": "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nam/prod/"
            },
            "HRRR": {

            },
            "RAP": {

            },
            "HIRESW": {
                
            },
            "NBM": {
                
            },
            "AIGFS": {
                "baseUrl": "https://nomads.ncep.noaa.gov/pub/data/nccf/com/aigfs/prod/",
                "urlStructure": "aigfs.{}.{}.{}", # Date, Run Time, Filename
                "availableTypes": ["PRES", "SFC"],
                "runTimes": [0, 6, 12, 18], # UTC
                "archiveLimit": 9, # Days
                "lateSteppingThreshold": None
            }
        }
        
        # User Input and Conditionals. God this took so long.
        running = True
        while running:
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
                modelChoice = input("--> ").strip()
                if not modelChoice:
                    print("\nPlease enter a number.")
                    sleep(1)
                else:
                    try:
                        modelChoice = int(modelChoice)
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
                                sleep(1)
                        else:
                            print("\nPlease select a valid option.")
                            sleep(1)
                            continue
                    except ValueError:
                        print("\nPlease enter a number.")
                        sleep(1)
    
            # Type Selection        
            while True:
                print(f'\nSelect what type of {model} GRIB you want.\n')
                for index, Type in enumerate(modelConfig[model]["availableTypes"], start=1):
                    print(f'{index} - {Type}')
                typeChoice = input("--> ").strip()
                if not typeChoice:
                    print("\nPlease enter a number.")
                    sleep(1)
                else:
                    try:
                        typeChoice = int(typeChoice)
                        typeChoice -= 1
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
                                sleep(1)
                        else:
                            print("Please enter a valid option.")
                    except ValueError:
                        print("\nPlease enter a number.")


            # Date Selection
            while True:
                rawDateLimit = currentDT - dt.timedelta(modelConfig[model]["archiveLimit"])
                dateLimit = rawDateLimit.strftime("%Y%m%d")
                dateLimit = int(dateLimit)
                print(f'\nSelect a date for your {type} {model} GRIB.')
                try:
                    dateSelection = int(input("(YYYY-MM-DD) --> ").replace("-","").strip())
                except ValueError:
                    print("Please enter a date as YYYYMMDD or YYYY-MM-DD")
                    sleep(1)
                if dateSelection > currentDate:
                    print("\nSorry, we don't support fetching GRIBs from the future... yet.")
                    sleep(1)
                elif dateSelection < dateLimit:
                    print("\nThe entered date is older than the archive limit, or is invalid.")
                    print(f'The earliest accessible {model} GRIBs are from: {rawDateLimit.strftime("%Y-%m-%d")}')
                    sleep(1)
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
                        sleep(1)
                    
            # Run Time Selection.
            # Needed special conditions here to make sure that run
            # times that have not been made here are not displayed
            # and therefore cannot be selected.
            while True:
                index = 0
                print(f'\nPlease select a run time (UTC) for your {type} {model} GRIB.')
                print("REMINDER: THE NWS CAN TAKE SEVERAL HOURS AFTER A RUN TO FULLY UPLOAD FILES!")
                for runTime in modelConfig[model]["runTimes"]:
                    if runTime > currentHour and dateSelection == currentDate:
                        break
                    else:
                        print(f'{index + 1} - {runTime:02d}:00 UTC')
                    index += 1
                try:
                    timeChoice = int(input("--> "))
                except ValueError:
                    print("Please enter a number.")
                    sleep(1)
                    if timeChoice > index or timeChoice < 0:
                        print("\nPlease select a valid time.")
                        sleep(1)
                    else:
                        timeChoice -= 1
                        
                        # File Checking
                        while True:
                            url = modelConfig[model]["baseUrl"]
                            testFiles = modelConfig[model]["testFiles"]
                            check1 = rq.head(url + testFiles[0])
                            check2 = rq.head(url + testFiles[1])
                            if check1.status_code == 404:
                                print("\nNo or little files have been uploaded for this run time.")
                                print("It is highly recommended that you back out.")
                                braveryConfirm = input("Would you still like to proceed? (Y/N) --> ").upper().strip()
                                if braveryConfirm == "N":
                                    break
                                elif braveryConfirm == "Y":

                                    continue
                                else:
                                    print("\nReally? You couldn't type Y or N? Butterfingers...")
                                    sleep(1)
                            elif check2.status_code == 404:
                                print("\nSome or most files have been uploaded for this runtime.")
                                print("""If you wish to have full access to these files, it is
                                      recommended that you choose an earlier run or date.""")
                                braveryConfirm = input("Would you still like to proceed? (Y/N) --> ").upper().strip()
                                # Finish this
                                if braveryConfirm == "N":
                                    pass
                                elif braveryConfirm == "Y":
                                    pass
                                else:
                                    print("\nReally? You couldn't type Y or N? Butterfingers...")
                                    sleep(1)                                    
                        while True: 
                            print(f'\nYou chose {modelConfig[model]["runTimes"][timeChoice]:02d}:00. Is this correct?')
                            timeConfirm = input("(Y/N) --> ").strip().upper()
                            if timeConfirm == "Y":
                                runTime = f'{modelConfig[model]["runTimes"][timeChoice]:02d}'
                                break
                            elif timeConfirm == "N":
                                continue
                            else:
                                print("\nReally? You couldn't type Y or N? Butterfingers...")
                                sleep(1)

                    
            # Resolution Selection.        
            while True:
                if modelConfig[model]["typeConfig"][type]["resolutions"] == None:
                    print(f'\nResolutions are not available for the {type} {model} GRIB. This may be a .NC file. Proceeding.')
                    break
                elif len(modelConfig[model]["typeConfig"][type]["resolutions"]) == 1:
                    print(f'\nOnly one available resolution for the {type} {model} GRIB. Selecting {modelConfig[model]["typeConfig"][type]["resolutions"][0].replace("p", ".")}°.')
                    break
                print("\nSelect a resolution.")
                for index, resolution in enumerate(modelConfig[model]["typeConfig"][type]["resolutions"], start=1):
                    print(f'{index} - {resolution.replace("p", ".")}°')
                try:
                    resChoice = int(input("--> ").strip())
                except ValueError:
                    print("\nPlease enter a number.")
                    sleep(1)
                if resChoice > len(modelConfig[model]["typeConfig"][type]["resolutions"]) or resChoice <= 0:
                    print("\nPlease select a valid resolution.")
                    sleep(1)
                    continue
                else:
                    resChoice -= 1
                    print(f'\nYou chose {modelConfig[model]["typeConfig"][type]["resolutions"][resChoice].replace("p", ".")}°. Is this correct?')
                    resConfirm = input("(Y/N) --> ").strip().upper()
                    if resConfirm == "Y":
                        resolution = modelConfig[model]["typeConfig"][type]["resolutions"][resChoice]
                        break
                    elif resConfirm == "N":
                        continue
                    else:
                        print("\nReally? You couldn't type Y or N? Butterfingers...")
                        sleep(1)

            # Forecast Hour Selection. This was by far the hardest part to figure out.
            # Also yes, I'm using a NumPy array so I can efficiently round entered times
            # to the nearest valid time in the array, cry about it in Visual Basic.
            complete = False
            minHour = modelConfig[model]["typeConfig"][type]["minHour"]
            maxHour = modelConfig[model]["typeConfig"][type]["maxHour"]
            time = minHour
            steppingIndex = 0
            validTimes = np.array([minHour])
            while True:
                if isinstance(modelConfig[model]["typeConfig"][type]["stepping"], dict):
                    for threshold in modelConfig[model]["steppingThresholds"]:
                        if complete:
                            break
                        while True:
                            stepping = getStepping(model, type, resolution)
                            if steppingIndex > len(stepping) - 1:
                                complete = True
                                break
                            time += stepping[steppingIndex]
                            print(time)
                            np.append(validTimes, time)
                            if time >= threshold:
                                steppingIndex += 1
                                break
                else:
                    stepping = getStepping(model, type)
                    time += stepping
                    validTimes = np.append(validTimes, time)
                    if time >= maxHour:
                        complete = True
                        break
            while True:
                if modelConfig[model]["typeConfig"][type]["analysisSupport"] == True:
                    print("\nYour selected type allows you do download an analysis file. Would you like to do that?")
                    analysisConfirm = input("(Y/N) --> ").strip().upper()
                    if analysisConfirm == "Y":
                        anlSelected = True
                        break
                    elif analysisConfirm == "N":
                        anlSelected = False
                        break
                    else:
                        print("\nReally? You couldn't type Y or N? Butterfingers...")
                        sleep(1)    
            while True:
                if anlSelected == True:
                    break
                else:
                    print("\nSelect a forecast hour.")
                    print("If the selected forecast hour is invalid, the closest one will be automatically selected.")
                    print(f'Minimum Hour: {minHour}')
                    print(f'Maximum Hour: {maxHour}')
                    try:
                        forecastHour = int(input("--> ").strip())
                    except ValueError:
                        print("Please enter a number.")
                        sleep(1)
                    if forecastHour not in validTimes:
                        forecastHour = findNearestValidTime(validTimes, forecastHour)
                        print(f'Invalid hour. Selecting forecast hour {forecastHour} instead.')
                    elif forecastHour < 0:
                        print("Are you serious?")
                        sleep(1)
                    print(f'\nYou chose forecast hour {forecastHour}. Is this correct?')
                    fhrConfirm = input("(Y/N) --> ").strip().upper()
                    if fhrConfirm == "Y":
                        print(modelConfig[model]["typeConfig"][type]["fileName"].format(runTime, resolution, forecastHour))
                        break
                    elif fhrConfirm == "N":
                        continue
                    else:
                        print("\nReally? You couldn't type Y or N? Butterfingers...")
                        sleep(1)
                    # FINISH THE FILE SELECTION
    except KeyboardInterrupt:
        print("\n")
        sys.exit()



