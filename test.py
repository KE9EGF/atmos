lateThreshold = 120
earlyStepping = 1
lateStepping = 7
maxHour = 384
validTimes = []
minHour = 3
fhr = 0
while True:
    if fhr >= lateThreshold:
        while True:
            fhr += lateStepping
            validTimes.append(fhr)
            if fhr >= maxHour:
                break
    if fhr >= maxHour:
        if validTimes[-1] > maxHour:
            validTimes.pop()
        break
    fhr += earlyStepping
    validTimes.append(fhr)
    
print(validTimes)