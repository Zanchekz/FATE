def startParsing():
    global file
    global fullNight
    global currentSetNr
    global currentSet
    global currentLimb
    global stopParsingBool
    global setsOptionMenu
    global fileRollbackPosition
    global fileRollbackPositionSmall
    
    currentSetNr = 0
    currentSet = None
    currentLimb = 0
    stopParsingBool = False

    setsOptionMenu.destroy()
    setsOptionMenu = customtkinter.CTkOptionMenu(app, values=[], command = changeSetDisplay)
    setsOptionMenu.place(relx = optionsMenuX, rely = optionsMenuY, anchor = tkinter.N)

    clearCurrentSet()
    clearGlobalStat()

    fullNight = FullNight()
    if file == None:
        # file = open(filename, 'r', encoding='utf-8')
        file = open(filename, 'r', encoding='latin-1')
    else:
        file.seek(0)

    fileRollbackPosition = file.tell()
    fileRollbackPositionSmall = file.tell()

    app.after(500, newSet(False, 0))
    
def newSet(isDirectToPlains, nightTime):
    global currentLimb
    global currentSet
    global currentSetNr
    global currentSetShown
    global setsOptionMenu
    global fileRollbackPosition
    
    currentLimb = 0
    currentSetNr += 1
    currentSetShown = currentSetNr

    deltaDisplay400.configure(text = "Delta Time (.400)")
    deltaDisplayNightime.configure(text = "Delta Time (3.600)")
    shrineTimeDisplay.configure(text = "0.000", text_color = "white")
    statusDisplay.configure(text = "Awaiting Status", text_color = "cyan", font=("Arial", 40))

    currentSet = FullSet(currentSetNr)

    # Add set to night
    fullNight.sets.append(currentSet)

    # Update options menu with new Set
    currOptions = setsOptionMenu._values
    setsOptionMenu.destroy()
    
    stringSetNumber = str(currentSetNr)
    currOptions.append(stringSetNumber)

    setsOptionMenu = customtkinter.CTkOptionMenu(app, values = currOptions, command = changeSetDisplay)
    setsOptionMenu.place(relx = optionsMenuX, rely = optionsMenuY, anchor = tkinter.N)

    changeSetDisplay(stringSetNumber)

    clearCurrentSet()

    fileRollbackPosition = file.tell()

    # Start scanning for host enter into plains
    if not isDirectToPlains:
        app.after(sleepBetweenCalls, scanHostLoad)
    # If direct to plains, go straight to terry scanning
    else:
        currentSet.loadIn.itsNighttimeTime = nightTime
        currentSet.isFirstSet = True
        app.after(sleepBetweenCalls, terryScanning)

def scanHostLoad():
    global currentSet
    global fileRollbackPositionSmall
    global currentLimb

    doneHere = False
    reset = False
    orbiterReset = False
    nighttimeTime = 0

    fileRollbackPositionSmall = file.tell()
    line = file.readline()  

    if "\n" not in line or line == "":
        file.seek(fileRollbackPositionSmall)
    else:
        while "\n" in line:
            trimmedTime = re.sub(r'[^0-9.]', '', line[0:8])
            
            # Host enter
            if currentSet.loadIn.hostEnterTime == 0 and searchHostEntering in line:
                try:
                    currentSet.loadIn.hostEnterTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.loadIn.hostEnterTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

                doneHere = True
                break

            # In case of direct to plains
            elif searchItsNightime in line:
                nighttimeTime = float(trimmedTime)
                orbiterReset = True
                break

            try:
                fileRollbackPositionSmall = file.tell()
                line = file.readline()  
                if "\n" not in line or line == "":
                    file.seek(fileRollbackPositionSmall)
                    break
            except:
                print("Error trying to readline\n")
                file.seek(fileRollbackPosition)
                break

    if reset:
        app.after(sleepBetweenCalls, newSet(False, 0))
    elif orbiterReset:
        app.after(sleepBetweenCalls, newSet(True, nighttimeTime))  
    elif not doneHere:
        app.after(sleepBetweenCalls, scanHostLoad)
    elif not stopParsingBool:
        fileRollbackPosition = file.tell()
        app.after(sleepBetweenCalls, scanFinalizeAndNightime) 


def scanFinalizeAndNightime():
    global currentLimb
    global currentSet
    global fileRollbackPositionSmall
    
    doneHere = False
    reset = False

    fileRollbackPositionSmall = file.tell()
    line = file.readline()  

    if "\n" not in line or line == "":
        file.seek(fileRollbackPositionSmall)
    else:
        while "\n" in line:
            trimmedTime = re.sub(r'[^0-9.]', '', line[0:8])

            # Reset
            if searchHostUnload in line:
                reset = True
                break

            # Finalize Eidolon Transition
            elif currentSet.loadIn.finalizeEidolonTransitionTime == 0 and searchFinalizeTransition in line:
                trimmedTime = re.sub(r'[^0-9.]', '', line[0:8])
                
                try:
                    currentSet.loadIn.finalizeEidolonTransitionTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.loadIn.finalizeEidolonTransitionTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

                valToShow = "{:.3f}".format(currentSet.loadIn.finalizeEidolonTransitionTime - currentSet.loadIn.hostEnterTime)
                finalizeTimeDisplay.configure(text = valToShow)
                currentSet.loadIn.displayFinalize = valToShow

                deltaDisplay400.configure(text = valToShow)

                if(float(valToShow) < finalizeTransitionBreakpoint):
                    finalizeTimeDisplay.configure(text_color = "red")
                    statusDisplay.configure(text = "RESET", text_color = "red", font=("Arial", 40))
                else:
                    finalizeTimeDisplay.configure(text_color = "white")

            # It's Nighttime
            elif currentSet.loadIn.itsNighttimeTime == 0 and searchItsNightime in line:
                try:
                    currentSet.loadIn.itsNighttimeTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.loadIn.itsNighttimeTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

                valToShow = "{:.3f}".format(currentSet.loadIn.itsNighttimeTime - currentSet.loadIn.finalizeEidolonTransitionTime)
                nighttimeTimeDisplay.configure(text = valToShow)
                currentSet.loadIn.displayItsNightitme = valToShow

                deltaDisplayNightime.configure(text = valToShow)

                if(float(valToShow) > nighttimeBreakpoint):
                    nighttimeTimeDisplay.configure(text_color = "red")
                    offestTime = "{:.3f}".format(currentSet.loadIn.itsNighttimeTime - currentSet.loadIn.finalizeEidolonTransitionTime - nighttimeBreakpoint)
                    deltaDisplayNightime.configure(text = valToShow + " [" + offestTime + "]")
                    statusDisplay.configure(text = "RESET", text_color = "red", font=("Arial", 40))
                else:
                    statusDisplay.configure(text = "Good", text_color = "green", font=("Arial", 40))
                    nighttimeTimeDisplay.configure(text_color = "white")

                if currentSet.loadIn.itsNighttimeTime > 0 and (currentSet.loadIn.itsNighttimeTime - currentSet.loadIn.finalizeEidolonTransitionTime) > 10:   
                    currentSet.isFirstSet = True

                doneHere = True
                break

            try:
                fileRollbackPositionSmall = file.tell()
                line = file.readline()  
                if "\n" not in line or line == "":
                    file.seek(fileRollbackPositionSmall)
                    break
            except:
                print("Error trying to readline\n")
                file.seek(fileRollbackPosition)
                break

    if reset:
        app.after(sleepBetweenCalls, newSet(False, 0))
    elif not doneHere:
        app.after(sleepBetweenCalls, scanFinalizeAndNightime)
    elif not stopParsingBool:
        currentLimb = 0
        fileRollbackPosition = file.tell()
        app.after(sleepBetweenCalls, terryScanning)

def terryScanning():
    global currentLimb
    global currentSet
    global fileRollbackPosition
    global fileRollbackPositionSmall
    
    doneHere = False
    reset = False
    orbiterReset = False
    nighttimeTime = 0

    fileRollbackPositionSmall = file.tell()
    line = file.readline()  

    if "\n" not in line or line == "":
        file.seek(fileRollbackPositionSmall)
    else:
        while "\n" in line:
            trimmedTime = re.sub(r'[^0-9.]', '', line[0:8])

            # Reset
            if searchHostUnload in line: # if host exited plains
                reset = True
                break

            # In case of direct to plains
            elif searchItsNightime in line: # if reset via orbiter
                nighttimeTime = float(trimmedTime)
                orbiterReset = True
                break

            # Terry spawn
            elif currentSet.terry.vulnerableTime == 0 and searchTeralystSpawned in line: # if no terry vurnerable and terry spawned in log 
                try:
                    currentSet.terry.vulnerableTime = float(trimmedTime) # try calculate vulnerable time
                except:
                    print("Trying to set currentSet.terry.vulnerableTime: \n" + line + "\n") # else error
                    file.seek(fileRollbackPosition)
                    break

            # First limb
            elif currentLimb == 0 and searchWeakpointDestroyed in line: # if no first limb data and limb destroyed in log
                try:
                    currentSet.terry.limbs.append(float(trimmedTime)) # try append pcurrent limb time to limbs array
                except:
                    print("Trying to add currentSet.terry.limbs: \n" + line + "\n")
                    currentSet.terry.limbs.clear()
                    file.seek(fileRollbackPosition)
                    break

                currentSet.terry.firstLimbTime = float(trimmedTime)
                
                firstLimbBreak = float(trimmedTime)

                # If first set, time 1st limb from nighttime
                if currentSet.isFirstSet:   
                    firstLimbBreakSeconds = firstLimbBreak - currentSet.loadIn.itsNighttimeTime
                else:
                    firstLimbBreakSeconds = firstLimbBreak - currentSet.loadIn.finalizeEidolonTransitionTime

                timeToVulnerable = "{:.3f}".format(firstLimbBreak - currentSet.terry.vulnerableTime)
                
                timeVal = str(datetime.timedelta(seconds = firstLimbBreakSeconds))[5:11]
                displayText = timeVal + " [" + timeToVulnerable + "]"
                currentSet.terry.limbDisplays[currentLimb].configure(text = displayText)

                currentSet.terry.displayFirstLimb = str(timeVal)
                currentSet.terry.displayTimeToVuln = str(timeToVulnerable)

                currentLimb += 1

            # Terry limbs
            elif currentLimb > 0 and currentLimb <= 3 and searchWeakpointDestroyed in line:
                try:
                    currentSet.terry.limbs.append(float(trimmedTime))
                except:
                    print("Trying to add terry limb time failed with line: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    for limb in currentSet.terry.limbs:
                        fullNight.limbsForMedian.pop()
                    currentSet.terry.limbs.clear()
                    currentSet.terry.limbsForMedian.clear()
                    currentLimb = 0
                    break

                limbTimeSeconds = "{:.3f}".format(currentSet.terry.limbs[currentLimb] - currentSet.terry.limbs[currentLimb - 1] - zeroMsLimbLoop)
                            
                currentSet.terry.limbsForMedian.append(float(limbTimeSeconds))
                
                currentSet.terry.limbDisplays[currentLimb].configure(text = limbTimeSeconds)

                # If last limb, get down time
                if currentLimb < 3:
                    currentLimb += 1
                else:
                    # If first set, time from nighttime
                    if currentSet.isFirstSet:
                        lastLimbTimeSeconds = currentSet.terry.limbs[currentLimb] - currentSet.loadIn.itsNighttimeTime
                    else:
                        lastLimbTimeSeconds = currentSet.terry.limbs[currentLimb] - currentSet.loadIn.finalizeEidolonTransitionTime

                    currentSet.terry.lastLimbTimeSeconds = lastLimbTimeSeconds
                    timeVal = str(datetime.timedelta(seconds = lastLimbTimeSeconds))[2:11]
                    terryLastLimbBreakTimeDisplay.configure(text = timeVal)
                    currentSet.terry.displayLastLimbTime = timeVal

                    currentSet.terry.timer_task_id = app.after(37000, eidoGettingUp)

                # Update median
                medianValue = "{:.3f}".format(statistics.median(currentSet.terry.limbsForMedian))
                terryLimbMedianDisplay.configure(text = medianValue)
                currentSet.terry.displayMedian = medianValue

                # Update global median
                fullNight.limbsForMedian.append(float(limbTimeSeconds))
                updateGlobalLimbMed()               

             # Capture 
            elif searchEidoCaptured in line:
                app.after_cancel(currentSet.terry.timer_task_id)
                terryCapshotDisplay.configure(text = "??")

                if len(currentSet.terry.limbs) < 4:
                    file.seek(fileRollbackPosition)
                    for limb in currentSet.terry.limbs:
                        fullNight.limbsForMedian.pop()
                    currentSet.terry.limbs.clear()
                    currentSet.terry.limbsForMedian.clear()
                    currentLimb = 0
                    break
                
                try:
                    currentSet.terry.capshotTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.terry.capshotTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

                capshotValue = currentSet.terry.capshotTime - currentSet.terry.limbs[len(currentSet.terry.limbs) - 1] - zeroMsCapshotTime

                valToShow = "{:.3f}".format(capshotValue)

                terryCapshotDisplay.configure(text = valToShow)
                currentSet.terry.displayCapshot = valToShow

                fullNight.capshotsForMedian.append(capshotValue)
                updateGlobalCapshotMed()

                # Real Capshot time
                if currentSet.isFirstSet:   
                    capshotTimeValue = currentSet.terry.capshotTime - currentSet.loadIn.itsNighttimeTime
                else:
                    capshotTimeValue = currentSet.terry.capshotTime - currentSet.loadIn.finalizeEidolonTransitionTime

                valToShowRealtime = str(datetime.timedelta(seconds = capshotTimeValue))[2:11]
                currentSet.terry.displayCapshotRealtime = valToShowRealtime

                terryCapshotTimeDisplay.configure(text = valToShowRealtime)

                doneHere = True
                break              

            # Kill
            elif searchEidoKilled in line:
                app.after_cancel(currentSet.terry.timer_task_id)
                terryCapshotDisplay.configure(text = "??")

                if len(currentSet.terry.limbs) < 4:
                    file.seek(fileRollbackPosition)
                    for limb in currentSet.terry.limbs:
                        fullNight.limbsForMedian.pop()
                    currentSet.terry.limbs.clear()
                    currentSet.terry.limbsForMedian.clear()
                    currentLimb = 0
                    break
                
                reset = True
                break

            try:
                fileRollbackPositionSmall = file.tell()
                line = file.readline()  
                if "\n" not in line or line == "":
                    file.seek(fileRollbackPositionSmall)
                    break
            except:
                print("Error trying to readline\n")
                file.seek(fileRollbackPosition)
                break
    
    if reset:
        app.after(sleepBetweenCalls, newSet(False, 0))
    elif orbiterReset:
        app.after(sleepBetweenCalls, newSet(True, nighttimeTime))  
    elif not doneHere:
        app.after(sleepBetweenCalls, terryScanning)
    elif not stopParsingBool:
        currentLimb = 0
        fileRollbackPosition = file.tell()
        app.after(sleepBetweenCalls, garryScanning)

def garryScanning():
    global currentLimb
    global currentSet
    global fileRollbackPosition
    global fileRollbackPositionSmall

    doneHere = False
    reset = False
    orbiterReset = False
    nighttimeTime = 0

    fileRollbackPositionSmall = file.tell()
    line = file.readline()  

    if "\n" not in line or line == "":
        file.seek(fileRollbackPositionSmall)
    else:
        while "\n" in line:
            trimmedTime = re.sub(r'[^0-9.]', '', line[0:8])
            
            # Reset
            if searchHostUnload in line:
                reset = True
                break

            # In case of direct to plains
            elif searchItsNightime in line:
                nighttimeTime = float(trimmedTime)
                orbiterReset = True
                break

            # Loot drop
            elif currentSet.garry.lootDropTime == 0 and searchLootDrop in line:
                try:
                    currentSet.garry.lootDropTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.garry.lootDropTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

            # Shrine enabled
            elif currentSet.garry.shrineEnabledTime == 0 and searchShrineEnabled in line:
                if currentSet.garry.lootDropTime == 0:
                    print("Trying to set Garry Shrine time without first finding loot drop, somehow. Rolling back\n")
                    file.seek(fileRollbackPosition)
                    break

                try:
                    currentSet.garry.shrineEnabledTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.garry.shrineEnabledTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break
                
                shrineTime = "{:.3f}".format(currentSet.garry.shrineEnabledTime - currentSet.garry.lootDropTime)
                garryShrineTimeDisplay.configure(text = shrineTime)
                shrineTimeDisplay.configure(text = shrineTime)
                currentSet.garry.displayShrineTime = shrineTime

            # Shard host
            elif currentSet.garry.shardOneTime == 0 and searchShardOne in line:
                try:
                    currentSet.garry.shardOneTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.garry.shardOneTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

                valToDisplay = "{:.3f}".format(currentSet.garry.shardOneTime - currentSet.garry.shrineEnabledTime)
                garryShardInsertsDisplay.configure(text = valToDisplay)
                currentSet.garry.displayShardOneTime = valToDisplay

            # Garry spawn
            elif currentSet.garry.spawnTime == 0 and searchWaterEidoSpawn in line:
                try:
                    currentSet.garry.spawnTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.garry.spawnTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

            # Shard client
            elif currentLimb < 2 and currentSet.garry.shardTwoTime == 0 and searchShardTwo in line:
                try:
                    currentSet.garry.shardTwoTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.garry.shardTwoTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

                valToDisplay = "{:.3f}".format(currentSet.garry.shardOneTime - currentSet.garry.shrineEnabledTime) + "   " + "{:.3f}".format(currentSet.garry.shardTwoTime - currentSet.garry.shardOneTime)
                garryShardInsertsDisplay.configure(text = valToDisplay)
                currentSet.garry.displayShardTwoTime = "{:.3f}".format(currentSet.garry.shardTwoTime - currentSet.garry.shardOneTime)
                
                if currentSet.garry.spawnTime != 0:
                    spawnDelay = "{:.3f}".format(currentSet.garry.spawnTime - currentSet.garry.shardTwoTime)
                    waterValToDisplay = "{:.3f}".format(currentSet.garry.waterLimbBreakTime - currentSet.garry.spawnTime)
                    currentSet.garry.displayspawnDelay = spawnDelay
                    garryWaterLimbBreakTimeDisplay.configure(text = waterValToDisplay + " + " + spawnDelay)


            # Water limb break
            elif currentLimb == 0 and searchWeakpointDestroyed in line:
                try:
                    currentSet.garry.waterLimbBreakTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.garry.waterLimbBreakTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    for limb in currentSet.garry.limbs:
                        fullNight.limbsForMedian.pop()
                    currentSet.garry.limbs.clear()
                    currentSet.garry.limbsForMedian.clear()
                    currentLimb = 0
                    break

                currentSet.garry.limbs.append(float(trimmedTime))
                
                # Check if solo/duo, different spawn delay timings
                if currentSet.garry.shardTwoTime == 0:
                    spawnDelay = "{:.3f}".format(currentSet.garry.spawnTime - currentSet.garry.shardOneTime)
                else:
                    spawnDelay = "{:.3f}".format(currentSet.garry.spawnTime - currentSet.garry.shardTwoTime)

                valToDisplay = "{:.3f}".format(currentSet.garry.waterLimbBreakTime - currentSet.garry.spawnTime)
                garryWaterLimbBreakTimeDisplay.configure(text = valToDisplay + " + " + spawnDelay)
                currentSet.garry.displayWaterTime = valToDisplay
                currentSet.garry.displayspawnDelay = spawnDelay
                
                fullNight.watersForMedian.append(currentSet.garry.waterLimbBreakTime - currentSet.garry.spawnTime)
                updateGlobalWaterMed()

                currentLimb += 1

            # Rest of limbs
            elif currentLimb > 0 and currentLimb <= 5 and searchWeakpointDestroyed in line:
                try:
                    currentSet.garry.limbs.append(float(trimmedTime))
                except:
                    print("Trying to add garry limb time failed with line: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    for limb in currentSet.garry.limbs:
                        fullNight.limbsForMedian.pop()
                    currentSet.garry.limbs.clear()
                    currentSet.garry.limbsForMedian.clear()
                    currentLimb = 0
                    break

                limbTimeSeconds = "{:.3f}".format(currentSet.garry.limbs[currentLimb] - currentSet.garry.limbs[currentLimb - 1] - zeroMsLimbLoop)
                
                currentSet.garry.limbsForMedian.append(float(limbTimeSeconds))

                currentSet.garry.limbDisplays[currentLimb].configure(text = limbTimeSeconds)

                # If last limb, get down time
                if currentLimb < 5:
                    currentLimb += 1
                else:
                    # If first set, time from nighttime
                    if currentSet.isFirstSet:   
                        lastLimbTimeSeconds = currentSet.garry.limbs[currentLimb] - currentSet.loadIn.itsNighttimeTime
                    else:
                        lastLimbTimeSeconds = currentSet.garry.limbs[currentLimb] - currentSet.loadIn.finalizeEidolonTransitionTime
                    
                    currentSet.garry.lastLimbTimeSeconds = lastLimbTimeSeconds
                    timeVal = str(datetime.timedelta(seconds = lastLimbTimeSeconds))[2:11]
                    garryLastLimbBreakTimeDisplay.configure(text = timeVal)
                    currentSet.garry.displayLastLimbTime = timeVal

                # Update median
                medianValue = "{:.3f}".format(statistics.median(currentSet.garry.limbsForMedian))
                garryLimbMedianDisplay.configure(text = medianValue)
                currentSet.garry.displayMedian = medianValue

                # Update global median
                fullNight.limbsForMedian.append(float(limbTimeSeconds))
                updateGlobalLimbMed()

            # Capture 
            elif searchEidoCaptured in line:
                if len(currentSet.garry.limbs) < 6:
                    file.seek(fileRollbackPosition)
                    for limb in currentSet.garry.limbs:
                        fullNight.limbsForMedian.pop()
                    currentSet.garry.limbs.clear()
                    currentSet.garry.limbsForMedian.clear()
                    currentLimb = 0
                    break
                
                try:
                    currentSet.garry.capshotTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.garry.capshotTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

                capshotValue = currentSet.garry.capshotTime - currentSet.garry.limbs[len(currentSet.garry.limbs) - 1] - zeroMsCapshotTime

                valToShow = "{:.3f}".format(capshotValue)

                garryCapshotDisplay.configure(text = valToShow)
                currentSet.garry.displayCapshot = valToShow
                
                fullNight.capshotsForMedian.append(capshotValue)
                updateGlobalCapshotMed()
                
                doneHere = True
                break              

            # Kill
            elif searchEidoKilled in line:
                reset = True
                break

            try:
                fileRollbackPositionSmall = file.tell()
                line = file.readline()  
                if "\n" not in line or line == "":
                    file.seek(fileRollbackPositionSmall)
                    break  
            except:
                print("Error trying to readline\n")
                file.seek(fileRollbackPosition)
                break
    
    if reset:
        app.after(sleepBetweenCalls, newSet(False, 0))
    elif orbiterReset:
        app.after(sleepBetweenCalls, newSet(True, nighttimeTime))  
    elif not doneHere:
        app.after(sleepBetweenCalls, garryScanning)
    elif not stopParsingBool:
        currentLimb = 0
        fileRollbackPosition = file.tell()
        app.after(sleepBetweenCalls, harryScanning)

def harryScanning():
    global currentLimb
    global currentSet
    global setsOptionMenu
    global fileRollbackPosition
    global fileRollbackPositionSmall

    doneHere = False
    reset = False
    orbiterReset = False
    nighttimeTime = 0

    fileRollbackPositionSmall = file.tell()
    line = file.readline()  

    if "\n" not in line or line == "":
        file.seek(fileRollbackPositionSmall)
    else:
        while "\n" in line:
            trimmedTime = re.sub(r'[^0-9.]', '', line[0:8])

            # Reset
            if searchHostUnload in line:
                reset = True
                break

            # In case of direct to plains
            elif searchItsNightime in line:
                nighttimeTime = float(trimmedTime)
                orbiterReset = True
                break

            # Loot drop
            elif currentSet.harry.lootDropTime == 0 and searchLootDrop in line:
                try:
                    currentSet.harry.lootDropTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.harry.lootDropTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

            # Shrine enabled
            elif currentSet.harry.shrineEnabledTime == 0 and searchShrineEnabled in line:
                if currentSet.harry.lootDropTime == 0:
                    print("Trying to set Harry Shrine time without first finding loot drop, somehow. Rolling back\n")
                    file.seek(fileRollbackPosition)
                    break

                try:
                    currentSet.harry.shrineEnabledTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.harry.shrineEnabledTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

                shrineTime = "{:.3f}".format(currentSet.harry.shrineEnabledTime - currentSet.harry.lootDropTime)
                harryShrineTimeDisplay.configure(text = shrineTime)
                shrineTimeDisplay.configure(text = shrineTime)
                currentSet.harry.displayShrineTime = shrineTime

            # Shard host
            elif currentSet.harry.shardOneTime == 0 and searchShardOne in line:
                try:
                    currentSet.harry.shardOneTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.harry.shardOneTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

                valToDisplay = "{:.3f}".format(currentSet.harry.shardOneTime - currentSet.harry.shrineEnabledTime)
                harryShardInsertsDisplay.configure(text = valToDisplay)
                currentSet.harry.displayShardOneTime = valToDisplay

            # Harry spawn
            elif currentSet.harry.spawnTime == 0 and searchWaterEidoSpawn in line:
                try:
                    currentSet.harry.spawnTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.harry.spawnTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

            # Shard client
            elif currentLimb < 2 and currentSet.harry.shardTwoTime == 0 and searchShardTwo in line:
                try:
                    currentSet.harry.shardTwoTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.harry.shardTwoTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

                valToDisplay = "{:.3f}".format(currentSet.harry.shardOneTime - currentSet.harry.shrineEnabledTime) + "   " + "{:.3f}".format(currentSet.harry.shardTwoTime - currentSet.harry.shardOneTime)
                harryShardInsertsDisplay.configure(text = valToDisplay)
                currentSet.harry.displayShardTwoTime = "{:.3f}".format(currentSet.harry.shardTwoTime - currentSet.harry.shardOneTime)

                if currentSet.harry.spawnTime != 0:
                    spawnDelay = "{:.3f}".format(currentSet.harry.spawnTime - currentSet.harry.shardTwoTime)
                    waterValToDisplay = "{:.3f}".format(currentSet.harry.waterLimbBreakTime - currentSet.harry.spawnTime)
                    currentSet.harry.displayspawnDelay = spawnDelay
                    harryWaterLimbBreakTimeDisplay.configure(text = waterValToDisplay + " + " + spawnDelay)

            # Water limb break
            elif currentLimb == 0 and searchWeakpointDestroyed in line:
                try:
                    currentSet.harry.waterLimbBreakTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.harry.waterLimbBreakTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    for limb in currentSet.harry.limbs:
                        fullNight.limbsForMedian.pop()
                    currentSet.harry.limbs.clear()
                    currentSet.harry.limbsForMedian.clear()
                    currentLimb = 0
                    break

                currentSet.harry.limbs.append(float(line[0:8]))
                
                # Check if solo/duo, different spawn delay timings
                if currentSet.garry.shardTwoTime != 0:
                    spawnDelay = "{:.3f}".format(currentSet.harry.spawnTime - currentSet.harry.shardTwoTime)
                else:
                    spawnDelay = "{:.3f}".format(currentSet.harry.spawnTime - currentSet.harry.shardOneTime)

                valToDisplay = "{:.3f}".format(currentSet.harry.waterLimbBreakTime - currentSet.harry.spawnTime)
                harryWaterLimbBreakTimeDisplay.configure(text = valToDisplay + " + " + spawnDelay)
                currentSet.harry.displayWaterTime = valToDisplay
                currentSet.harry.displayspawnDelay = spawnDelay
                
                fullNight.watersForMedian.append(currentSet.harry.waterLimbBreakTime - currentSet.harry.spawnTime)
                updateGlobalWaterMed()

                currentLimb += 1

            # Rest of limbs
            elif currentLimb > 0 and currentLimb <= 5 and searchWeakpointDestroyed in line:
                try:
                    currentSet.harry.limbs.append(float(trimmedTime))
                except:
                    print("Trying to add harry limb time failed with line: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    for limb in currentSet.harry.limbs:
                        fullNight.limbsForMedian.pop()
                    currentSet.harry.limbs.clear()
                    currentSet.harry.limbsForMedian.clear()
                    currentLimb = 0
                    break

                limbTimeSeconds = "{:.3f}".format(currentSet.harry.limbs[currentLimb] - currentSet.harry.limbs[currentLimb - 1] - zeroMsLimbLoop)
                
                currentSet.harry.limbsForMedian.append(float(limbTimeSeconds))
                
                currentSet.harry.limbDisplays[currentLimb].configure(text = limbTimeSeconds)

                # If last limb, get down time
                if currentLimb < 5:
                    currentLimb += 1
                else:
                    # If first set, time from nighttime
                    if currentSet.isFirstSet:   
                        lastLimbTimeSeconds = currentSet.harry.limbs[currentLimb] - currentSet.loadIn.itsNighttimeTime
                    else:
                        lastLimbTimeSeconds = currentSet.harry.limbs[currentLimb] - currentSet.loadIn.finalizeEidolonTransitionTime

                    currentSet.harry.lastLimbTimeSeconds = lastLimbTimeSeconds
                    timeVal = str(datetime.timedelta(seconds = lastLimbTimeSeconds))[2:11]
                    harryLastLimbBreakTimeDisplay.configure(text = timeVal)
                    currentSet.harry.displayLastLimbTime = timeVal
                    
                    if lastLimbTimeSeconds < redRunBreakpoint:
                        harryLastLimbBreakTimeDisplay.configure(text_color = redAverageColor)
                    elif lastLimbTimeSeconds >= redRunBreakpoint and lastLimbTimeSeconds < pinkRunBreakpoint:
                        harryLastLimbBreakTimeDisplay.configure(text_color = pinkAverageColor)
                    else:
                        harryLastLimbBreakTimeDisplay.configure(text_color = purpleAverageColor)

                    fullNight.runTimesForAverage.append(lastLimbTimeSeconds)
                    updateGlobalAvg()

                # Update median
                medianValue = "{:.3f}".format(statistics.median(currentSet.harry.limbsForMedian))
                harryLimbMedianDisplay.configure(text = medianValue)
                currentSet.harry.displayMedian = medianValue

                # Update global median
                fullNight.limbsForMedian.append(float(limbTimeSeconds))
                updateGlobalLimbMed()

            # Capture 
            elif searchEidoCaptured in line:
                if len(currentSet.harry.limbs) < 6:
                    file.seek(fileRollbackPosition)
                    for limb in currentSet.harry.limbs:
                        fullNight.limbsForMedian.pop()
                    currentSet.harry.limbs.clear()
                    currentSet.harry.limbsForMedian.clear()
                    currentLimb = 0
                    break
                
                try:
                    currentSet.harry.capshotTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.harry.capshotTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break
                
                capshotValue = currentSet.harry.capshotTime - currentSet.harry.limbs[len(currentSet.harry.limbs) - 1] - zeroMsCapshotTime

                valToShow = "{:.3f}".format(capshotValue)

                harryCapshotDisplay.configure(text = valToShow)
                currentSet.harry.displayCapshot = valToShow
                
                fullNight.capshotsForMedian.append(capshotValue)
                updateGlobalCapshotMed()

                fileRollbackPosition = file.tell()

                doneHere = True
                break              

            # Kill
            elif searchEidoKilled in line:
                reset = True
                break

            try:
                fileRollbackPositionSmall = file.tell()
                line = file.readline()  
                if "\n" not in line or line == "":
                    file.seek(fileRollbackPositionSmall)
                    break
            except:
                print("Error trying to readline\n")
                file.seek(fileRollbackPosition)
                break
    
    if reset:
        app.after(sleepBetweenCalls, newSet(False, 0))
    elif orbiterReset:
        app.after(sleepBetweenCalls, newSet(True, nighttimeTime))  
    elif not doneHere:
        app.after(sleepBetweenCalls, harryScanning)
    elif not stopParsingBool:
        # Update options menu with time in current set
        currOptions = setsOptionMenu._values
        setsOptionMenu.destroy()
        
        stringSetNumber = str(currentSetNr)
        newName = stringSetNumber + " - " + str(currentSet.harry.displayLastLimbTime)
        currOptions.pop()
        currOptions.append(newName)

        setsOptionMenu = customtkinter.CTkOptionMenu(app, values = currOptions, command = changeSetDisplay)
        setsOptionMenu.place(relx = optionsMenuX, rely = optionsMenuY, anchor = tkinter.N)
        setsOptionMenu.set(newName)

        app.after(sleepBetweenCalls, newSet(False, 0))
