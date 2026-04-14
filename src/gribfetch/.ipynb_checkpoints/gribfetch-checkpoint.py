# TODO: Add models: NAM, HRRR, RAP, NBM, AIGFS, HIRESW.
# TODO: Optimize pretty much everything after downloading and file-fetching works.
running = True
while running:
    # Packages, I probably couldn't live without them.
    try:
        try:
            import sys, os
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
        
        # Source - https://stackoverflow.com/a/68994644
        # Posted by user8017857
        # Retrieved 2026-04-10, License - CC BY-SA 4.0
        def findNearest(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        availableModels = ["GFS", "NAM", "HRRR", "RAP", "HiResW", "AIGFS", "NBM"]
        chunkSize = 1028 # kB
        modelConfig = {
            "GFS": {
                "baseUrl": "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{date}/{run}/atmos/",
                "availableTypes": ["ATM", "PGRB2","PGRB2B", "PGRB2FULL", "GOESSIMPGRB2", "SFC", "SFLUXGRB", "WGNE"],
                "runTimes": [0, 6, 12, 18],     # UTC
                "archiveLimit": 9,              # Days
                "steppingThresholds": [120],    # This is to determine at what forecast hour the stepping intervals change
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
                        "fileName": "gfs.t{run}z.atm{fhr}.nc"
                    },
                    "GOESSIMPGRB2": {
                        "resolutions": ["0p25"],
                        "extension": ".grib2",
                        "minHour": 0,
                        "maxHour": 180,
                        "stepping": [3],
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}z.goessimpgrb2.{res}.{fhr}"
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
                        "fileName": "gfs.t{run}z.pgrb2.{res}.{fhr}"
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
                        "fileName": "gfs.t{run}z.pgrb2b.{res}.{fhr}"
                    },
                    "PGRB2FULL": {
                        "resolutions": ["0p50"],
                        "extension": ".grib2",
                        "minHour": 0,
                        "maxHour": 384,
                        "stepping": [3],
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}z.pgrb2full.{res}.{fhr}"
                    },
                    "SFC": {
                        "resolutions": None,
                        "extension": ".nc",
                        "minHour": 1,
                        "maxHour": 12,
                        "stepping": [1],
                        "analysisSupport": True,
                        "fileName": "gfs.t{run}z.sfc.{fhr}.nc"
                    },
                    "SFLUXGRB": {
                        "resolutions": None,
                        "extension": ".grib2",
                        "minHour": 0,
                        "maxHour": 384,
                        "stepping": [1, 3],
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}z.sfluxgrb.{fhr}.grib2"
                    },
                    "WGNE": {
                        "resolutions": None,
                        "extension": ".grib2",
                        "minHour": 3,
                        "maxHour": 180,
                        "stepping": [3],
                        "analysisSupport": False,
                        "fileName": "gfs.t{run}z.wgne.{fhr}"
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
                print(f'\nSelect what type of {model} GRIB you want.')
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
                dateLimit = int(rawDateLimit.strftime("%Y%m%d"))
                print(f'\nSelect a date for your {type} {model} GRIB.')
                try:
                    dateSelection = int(input("(YYYY-MM-DD) --> ").replace("-","").strip())
                    if dateSelection > currentDate:
                        print("\nSorry, we don't support fetching GRIBs from the future... yet.")
                        sleep(1)
                    elif dateSelection < dateLimit:
                        print("\nThe entered date is older than the archive limit, or is invalid.")
                        print(f'The earliest accessible {model} GRIBs are from: {rawDateLimit.strftime("%Y-%m-%d")}')
                        sleep(1)
                    else:
                        year = str(dateSelection)[:4]
                        month = str(dateSelection)[4:6]
                        day = str(dateSelection)[6:8]
                        print(f'\nYou chose {year}-{month}-{day}. Is this correct?')
                        dateConfirm = input("(Y/N) --> ").strip().upper()
                        if dateConfirm == "Y":
                            date = dateSelection
                            break
                        elif dateConfirm == "N":
                            continue
                        else:
                            print("\nReally? You couldn't type Y or N? Butterfingers...")
                            sleep(1)
                except ValueError:
                    print("Please enter a date as YYYYMMDD or YYYY-MM-DD.")
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
                    if timeChoice > index or timeChoice < 0:
                        print("\nPlease select a valid time.")
                        sleep(1)
                    else:
                        timeChoice -= 1                                 
                        print(f'\nYou chose {modelConfig[model]["runTimes"][timeChoice]:02d}:00. Is this correct?')
                        timeConfirm = input("(Y/N) --> ").strip().upper()
                        if timeConfirm == "Y":
                            runTime = f'{modelConfig[model]["runTimes"][timeChoice]:02d}'
                            url = modelConfig[model]["baseUrl"].format(date=date, run=runTime)
                            testFiles = modelConfig[model]["testFiles"]
                            try:
                                check1 = rq.head(url + testFiles[0].format(run=runTime))
                                check2 = rq.head(url + testFiles[1].format(run=runTime))
                            except requests.exceptions.RequestException as e:
                                print("\nAn unexpected error occurred, please try again later.")
                                print(e)
                                sleep(3)
                                sys.exit()
                            if check1.status_code in (404, 403):
                                print("\nNo files have been uploaded for this run time.")
                                print("You will be returned to the run selection.")
                                sleep(2)
                                continue
                            elif check2.status_code in (404, 403):
                                print("\nSome or most files have been uploaded for this runtime.")
                                print("""If you wish to have full access to these files, it is
recommended that you choose an earlier run or date.""")
                                print("\nWould you still like to proceed?")
                                braveryConfirm = input("(Y/N) --> ").upper().strip()
                                if braveryConfirm == "N":
                                    continue
                                elif braveryConfirm == "Y":
                                    break
                                else:
                                    print("\nReally? You couldn't type Y or N? Butterfingers...")
                                    sleep(1)
                            elif check1.status_code == 200 and check2.status_code == 200:
                                break
                        elif timeConfirm == "N":
                            continue
                        else:
                            print("\nReally? You couldn't type Y or N? Butterfingers...")
                            sleep(1)
                except ValueError:
                    print("Please enter a number.")
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
                        res = modelConfig[model]["typeConfig"][type]["resolutions"][resChoice]
                        break
                    elif resConfirm == "N":
                        continue
                    else:
                        print("\nReally? You couldn't type Y or N? Butterfingers...")
                        sleep(1)

            # Forecast Hour Selection. This was by far the hardest part to figure out.
            # Also yes, I'm using a NumPy array so I can efficiently round entered times
            # to the nearest valid time in the array, cry about it in Visual Basic.
            thresholds = modelConfig[model]["steppingThresholds"]
            minHour = modelConfig[model]["typeConfig"][type]["minHour"]
            maxHour = modelConfig[model]["typeConfig"][type]["maxHour"]
            time = minHour
            validTimes = np.array([time])
            if isinstance(modelConfig[model]["typeConfig"][type]["stepping"], dict):
                stepping = getStepping(model, type, resolution)
            else:
                stepping = getStepping(model, type)
            for threshold in thresholds:
                for step in stepping:
                    while time < maxHour:
                        time += step
                        validTimes = np.append(validTimes, time)
                        if time == threshold:
                            break
            while True:
                if modelConfig[model]["typeConfig"][type]["analysisSupport"] == True:
                    print("\nYour selected type allows you do download an analysis file. Would you like to do that?")
                    anlConfirm = input("(Y/N) --> ").strip().upper()
                    if anlConfirm == "Y":
                        fhr = "anl"
                        anlSelected = True
                        break
                    elif anlConfirm == "N":
                        anlSelected = False
                        break
                    else:
                        print("\nReally? You couldn't type Y or N? Butterfingers...")
                        sleep(1)  
            while True:
                if anlSelected:
                    break
                print("\nEnter a forecast hour.")
                print("If the entered forecast hour is invalid, the closest one will be selected.")
                print(f'Minimum Hour: {minHour}')
                print(f'Maximum Hour: {maxHour}')
                fhr = input("--> ").strip()
                if not fhr:
                    continue
                try:
                    fhr = int(fhr)
                    if fhr not in validTimes:
                        fhr = findNearest(validTimes, fhr)
                        print(f'\nInvalid hour. Selecting forecast hour #{fhr} instead.')
                        sleep(1)
                    elif fhr < 0:
                        print("Are you serious?")
                        sleep(1)
                        continue
                    print(f'\nYou chose forecast hour #{fhr}. Is this correct?')
                    fhrConfirm = input("(Y/N) --> ").strip().upper()
                    if fhrConfirm == "Y":
                        fhr = f'f{fhr}'
                        break
                    elif fhrConfirm == "N":
                        continue
                    else:
                        print("\nReally? You couldn't type Y or N? Butterfingers...")
                        sleep(1)
                except ValueError:
                    print("Please enter a number.")
                    sleep(1)
                    
            # Final Selection and Downloading
            while True:
                print("\nPlease review the listed selections below.")
                print(f"""
Model: {model}
Type:  {type}
Date:  {year}-{month}-{day}
Run:   {int(runTime):02d}:00Z
Res:   {res.replace("p", ".")}°
Anl?:  {anlSelected}
FHR:   {fhr.replace("f", "")}""")
                print("\nAre these all correct?")
                allConfirm = input("(Y/N) --> ").upper().strip()
                if allConfirm == "Y":
                    break
                elif allConfirm == "N":
                    print("Please re-run this program to select your wanted attributes.")
                    sleep(2)
                    sys.exit()
                else:
                    print("\nReally? You couldn't type Y or N? Butterfingers...")
                    sleep(1)

            url = modelConfig[model]["baseUrl"].format(date=date, run=runTime)
            extension = modelConfig[model]["typeConfig"][type]["extension"]
            # This filename will act as the file path, being the download 
            # destination in the directory this program is run in.
            fileName = modelConfig[model]["typeConfig"][type]["fileName"].format(run=runTime, res=res, fhr=fhr)
            check = rq.head(url + fileName)
            if check.status_code in (404, 403):
                print("The file with your selected attributes is unavailable")
                print("Please re-run the program and select an earlier file.")
                sleep(2)
                sys.exit()
            
            # Source - https://stackoverflow.com/a/37573701
            # Posted by leovp, modified by community. See post 'Timeline' for change history
            # Retrieved 2026-04-14, License - CC BY-SA 4.0
            response = rq.get(url, stream=True)
            totalSize = int(response.headers.get("content-length", 0))                
            with tqdm(total=totalSize, unit="B", unit_scale=True) as progressBar:
                with open(fileName, "wb") as file:
                    for data in response.iter_content(chunkSize):
                        progressBar.update(len(data))
                        file.write(data)

            if totalSize != 0 and progressBar.n != totalSize:
                raise RuntimeError("An unexpected error occurred, and the file could not be properly downloaded.")
                sleep(2)
                sys.exit()

            # For some reason, some GRIBs on NOMADS do not have their
            # extension attached to them (e.g. .nc, .grib2), this small
            # conditional solves that, as it is rather annoying to
            # manually rename it.
            # FINISH THIS!
            if extension not in fileName:
                os.rename(fileName, fileName + extension)
            print("\n")
    except KeyboardInterrupt:
        print("\n")
        sys.exit()



