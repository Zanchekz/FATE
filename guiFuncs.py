# Clear limb times. The rest gets cleared on its own for some reason
def clearLimbTimes():
    terryLimb1Display.configure(text = "00")
    terryLimb2Display.configure(text = "")
    terryLimb3Display.configure(text = "")
    
    garryLimb1Display.configure(text = "00")
    garryLimb2Display.configure(text = "")
    garryLimb3Display.configure(text = "")
    garryLimb4Display.configure(text = "")
    garryLimb5Display.configure(text = "")
    
    harryLimb1Display.configure(text = "00")
    harryLimb2Display.configure(text = "")
    harryLimb3Display.configure(text = "")
    harryLimb4Display.configure(text = "")
    harryLimb5Display.configure(text = "")

def clearCurrentSet():
    clearLimbTimes()

    terryFirstLimbBreakTimeDisplay.configure(text = "??")
    terryLastLimbBreakTimeDisplay.configure(text = "??")
    terryCapshotDisplay.configure(text = "??")
    terryCapshotTimeDisplay.configure(text = "??")
    terryLimbMedianDisplay.configure(text = "??")
    finalizeTimeDisplay.configure(text = "??")
    nighttimeTimeDisplay.configure(text = "??")
    
    garryWaterLimbBreakTimeDisplay.configure(text = "??")
    garryLastLimbBreakTimeDisplay.configure(text = "??")
    garryCapshotDisplay.configure(text = "??")
    garryLimbMedianDisplay.configure(text = "??")
    garryShrineTimeDisplay.configure(text = "??")
    garryShardInsertsDisplay.configure(text = "??")

    harryWaterLimbBreakTimeDisplay.configure(text = "??")
    harryLastLimbBreakTimeDisplay.configure(text = "??")
    harryCapshotDisplay.configure(text = "??")
    harryLimbMedianDisplay.configure(text = "??")
    harryShrineTimeDisplay.configure(text = "??")
    harryShardInsertsDisplay.configure(text = "??")

def clearGlobalStat():
    globalRunAvgDisplay.configure(text = "??")
    globalCapshotMedianDisplay.configure(text = "??")
    globalLimbMedianDisplay.configure(text = "??")
    globalWaterMedianDisplay.configure(text = "??")

def displayTerry(setToDisplay):
    clearLimbTimes()

    finalizeTimeDisplay.configure(text = setToDisplay.loadIn.displayFinalize)
    nighttimeTimeDisplay.configure(text = setToDisplay.loadIn.displayItsNightitme)

    if float(setToDisplay.loadIn.displayFinalize) == 0:
        finalizeTimeDisplay.configure(text_color = "white")
    elif float(setToDisplay.loadIn.displayFinalize) < finalizeTransitionBreakpoint:
        finalizeTimeDisplay.configure(text_color = "red")
    else:
        finalizeTimeDisplay.configure(text_color = "white")

    if float(setToDisplay.loadIn.displayItsNightitme) == 0:
        nighttimeTimeDisplay.configure(text_color = "white")
    elif float(setToDisplay.loadIn.displayItsNightitme) > nighttimeBreakpoint:
        nighttimeTimeDisplay.configure(text_color = "red")
    else:
        nighttimeTimeDisplay.configure(text_color = "white")

    firstLimbText = str(setToDisplay.terry.displayFirstLimb) + " [" + str(setToDisplay.terry.displayTimeToVuln) + "]"
    terryFirstLimbBreakTimeDisplay.configure(text = firstLimbText)

    terryCapshotDisplay.configure(text = setToDisplay.terry.displayCapshot)
    terryCapshotTimeDisplay.configure(text = setToDisplay.terry.displayCapshotRealtime)
    terryLastLimbBreakTimeDisplay.configure(text = setToDisplay.terry.displayLastLimbTime)

    for i in range(0, len(setToDisplay.terry.limbsForMedian)):
        setToDisplay.terry.limbDisplays[i + 1].configure(text = "{:.3f}".format(setToDisplay.terry.limbsForMedian[i]))
      
    terryLimbMedianDisplay.configure(text = setToDisplay.terry.displayMedian)

def displayGarry(setToDisplay):
    garryShrineTimeDisplay.configure(text = setToDisplay.garry.displayShrineTime)

    if setToDisplay.garry.displayShardTwoTime != 0:
        shardTimes = str(setToDisplay.garry.displayShardOneTime) + "   " + str(setToDisplay.garry.displayShardTwoTime)
    else:
        shardTimes = str(setToDisplay.garry.displayShardOneTime)

    garryShardInsertsDisplay.configure(text = shardTimes)

    waterTime = str(setToDisplay.garry.displayWaterTime) + " + " + str(setToDisplay.garry.displayspawnDelay)
    garryWaterLimbBreakTimeDisplay.configure(text = waterTime)

    garryCapshotDisplay.configure(text = setToDisplay.garry.displayCapshot)
    garryLastLimbBreakTimeDisplay.configure(text = setToDisplay.garry.displayLastLimbTime)
    garryLimbMedianDisplay.configure(text = setToDisplay.garry.displayMedian)

    for i in range(0, len(setToDisplay.garry.limbsForMedian)):
        setToDisplay.garry.limbDisplays[i + 1].configure(text = "{:.3f}".format(setToDisplay.garry.limbsForMedian[i]))

def displayHarry(setToDisplay):
    harryShrineTimeDisplay.configure(text = setToDisplay.harry.displayShrineTime)

    if setToDisplay.harry.displayShardTwoTime != 0:
        shardTimes = str(setToDisplay.harry.displayShardOneTime) + "   " + str(setToDisplay.harry.displayShardTwoTime)
    else:
        shardTimes = str(setToDisplay.harry.displayShardOneTime)

    harryShardInsertsDisplay.configure(text = shardTimes)

    waterTime = str(setToDisplay.harry.displayWaterTime) + " + " + str(setToDisplay.harry.displayspawnDelay)
    harryWaterLimbBreakTimeDisplay.configure(text = waterTime)

    harryCapshotDisplay.configure(text = setToDisplay.harry.displayCapshot)
    harryLastLimbBreakTimeDisplay.configure(text = setToDisplay.harry.displayLastLimbTime)
    harryLimbMedianDisplay.configure(text = setToDisplay.harry.displayMedian)

    for i in range(0, len(setToDisplay.harry.limbsForMedian)):
        setToDisplay.harry.limbDisplays[i + 1].configure(text = "{:.3f}".format(setToDisplay.harry.limbsForMedian[i]))

    if setToDisplay.harry.lastLimbTimeSeconds == 0:
        harryLastLimbBreakTimeDisplay.configure(text_color = "white")
    elif setToDisplay.harry.lastLimbTimeSeconds < redRunBreakpoint:
        harryLastLimbBreakTimeDisplay.configure(text_color = redAverageColor)
    elif setToDisplay.harry.lastLimbTimeSeconds >= redRunBreakpoint and setToDisplay.harry.lastLimbTimeSeconds < pinkRunBreakpoint:
        harryLastLimbBreakTimeDisplay.configure(text_color = pinkAverageColor)
    else:
        harryLastLimbBreakTimeDisplay.configure(text_color = purpleAverageColor)

# Update global stats
def updateGlobalAvg():
    averageInSeconds = sum(fullNight.runTimesForAverage)/len(fullNight.runTimesForAverage)
    timeVal = str(datetime.timedelta(seconds = averageInSeconds))[2:11]
    
    # Update text and color acordingly
    globalRunAvgDisplay.configure(text = timeVal)
    if averageInSeconds < redRunBreakpoint:
        globalRunAvgDisplay.configure(text_color = redAverageColor)
    elif averageInSeconds >= redRunBreakpoint and averageInSeconds < pinkRunBreakpoint:
        globalRunAvgDisplay.configure(text_color = pinkAverageColor)
    else:
        globalRunAvgDisplay.configure(text_color = purpleAverageColor)


def updateGlobalCapshotMed():
    medianValue = "{:.3f}".format(statistics.median(fullNight.capshotsForMedian))
    
    globalCapshotMedianDisplay.configure(text = medianValue)

def updateGlobalLimbMed():
    medianValue = "{:.3f}".format(statistics.median(fullNight.limbsForMedian))
    
    globalLimbMedianDisplay.configure(text = medianValue)

def updateGlobalWaterMed():
    medianValue = "{:.3f}".format(statistics.median(fullNight.watersForMedian))
    
    globalWaterMedianDisplay.configure(text = medianValue)
    
def eidoGettingUp():
    terryCapshotDisplay.configure(text = "Getting Up!")