import tkinter
import customtkinter
import datetime
import statistics
import re
import os

# Set the filename and open the file
# filename = os.getenv('LOCALAPPDATA') + '\Warframe\EE.log'
filename = os.getenv('LOCALAPPDATA') + '\Warframe\EE.log'
file = None
fileRollbackPosition = None
fileRollbackPositionSmall = None

# System Settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
customtkinter.deactivate_automatic_dpi_awareness()

# App window - Size and Title
app = customtkinter.CTk()
app.geometry("960x960")
app.title("FATE")

fullSetFrame = customtkinter.CTkFrame(app, width = app._current_width - 20, height = app._current_height/2 - 10)
fullSetFrame.pack_propagate(0)
fullSetFrame.place(relx = .5, rely = .35, anchor = tkinter.N)

globalOverviewFrame = customtkinter.CTkFrame(app, width = app._current_width - 20, height = app._current_height/8 - 10)
globalOverviewFrame.pack_propagate(0)
globalOverviewFrame.place(relx = .5, rely = .85, anchor = tkinter.N)

textColor = "light gray"
redAverageColor = "#EB532A"
pinkAverageColor = "#EC87F8"
purpleAverageColor = "#B28DFB"

columnRelValues = [0.01, 0.2, 0.34, 0.6, 0.83]
lineRelValues = [0, 0.06, 0.14, 0.20, 0.34, 0.40, 0.48, 0.54, 0.70, 0.76, 0.84, 0.90]
limbSpaceToPrevious = .08

optionsMenuX = .30
optionsMenuY = .28
stopParsingButtonX = .499
stopParsingButtonY = .273
limbBreakpointTextX = .70
limbBreakpointInput1X = .64
limbBreakpointInput2X = .70
limbBreakpointInput3X = .76
limbBreakpointInputY = .28

# Various miscelaneous variables and values
stopParsingBool = False
sleepBetweenCalls = 1000
# sleepBetweenCalls = 10

currentSetNr = 0
currentSet = None

redRunBreakpoint = 405
pinkRunBreakpoint = 410

zeroMsLimbLoop = 17.186
zeroMsCapshotTime = 48.100
currentLimb = 0
finalizeTransitionBreakpoint = 0.350
nighttimeBreakpoint = 3.610

limbColor1Breakpoint = 0
limbColor2Breakpoint = 0
limbColor3Breakpoint = 0

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

# Options menu for selecting which set to display
def changeSetDisplay(optionName):
    global fullNight
    global currentSetShown

    setsOptionMenu.set(optionName)

    setNr = int(optionName[:2])
    currentSetShown = setNr

    setToDisplay = fullNight.sets[setNr - 1]

    displayTerry(setToDisplay)
    displayGarry(setToDisplay)
    displayHarry(setToDisplay)

setsOptionMenuLabel = customtkinter.CTkLabel(app, text = "Select set to show", text_color = textColor, font = ("Arial", 18))
setsOptionMenuLabel.place(relx = optionsMenuX, rely = optionsMenuY - .03, anchor = tkinter.N)
setsOptionMenu = customtkinter.CTkOptionMenu(app, values=[], command = changeSetDisplay)
setsOptionMenu.place(relx = optionsMenuX, rely = optionsMenuY, anchor = tkinter.N)

# limbBreakpointText = customtkinter.CTkLabel(app, text = "Limb Color Breakpoints", text_color = textColor, font = ("Arial", 18))
# limbBreakpointText.place(relx = limbBreakpointTextX, rely = limbBreakpointInputY - .03, anchor = tkinter.N)
# limb1Entry = customtkinter.CTkEntry(app, placeholder_text="Red", width = 50)
# limb1Entry.place(relx = limbBreakpointInput1X, rely = limbBreakpointInputY, anchor = tkinter.N)
# limb2Entry = customtkinter.CTkEntry(app, placeholder_text="Pink", width = 50)
# limb2Entry.place(relx = limbBreakpointInput2X, rely = limbBreakpointInputY, anchor = tkinter.N)
# limb3Entry = customtkinter.CTkEntry(app, placeholder_text="Purple", width = 50)
# limb3Entry.place(relx = limbBreakpointInput3X, rely = limbBreakpointInputY, anchor = tkinter.N)


# Full Set UI elements
# Host load things
finalizeTimeTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Finalize time", text_color = textColor, font = ("Arial", 18))
finalizeTimeTextDisplay.place(relx = columnRelValues[4], rely = lineRelValues[0], anchor = tkinter.NW)
finalizeTimeDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
finalizeTimeDisplay.place(relx = columnRelValues[4], rely = lineRelValues[1], anchor = tkinter.NW)

nighttimeTimeTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Nighttime time", text_color = textColor, font = ("Arial", 18))
nighttimeTimeTextDisplay.place(relx = columnRelValues[4], rely = lineRelValues[2], anchor = tkinter.NW)
nighttimeTimeDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
nighttimeTimeDisplay.place(relx = columnRelValues[4], rely = lineRelValues[3], anchor = tkinter.NW)

# Terry
terryFirstLimbBreakTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "First Limb Time", text_color = textColor, font = ("Arial", 18))
terryFirstLimbBreakTextDisplay.place(relx = columnRelValues[0], rely = lineRelValues[0], anchor = tkinter.NW)
terryFirstLimbBreakTimeDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
terryFirstLimbBreakTimeDisplay.place(relx = columnRelValues[0], rely = lineRelValues[1], anchor = tkinter.NW)

terryLastLimbBreakTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Last Limb Time", text_color = textColor, font = ("Arial", 18))
terryLastLimbBreakTextDisplay.place(relx = columnRelValues[0], rely = lineRelValues[2], anchor = tkinter.NW)
terryLastLimbBreakTimeDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
terryLastLimbBreakTimeDisplay.place(relx = columnRelValues[0], rely = lineRelValues[3], anchor = tkinter.NW)

terryCapshotTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Capshot", text_color = textColor, font = ("Arial", 18))
terryCapshotTextDisplay.place(relx = columnRelValues[1], rely = lineRelValues[0], anchor = tkinter.NW)
terryCapshotDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
terryCapshotDisplay.place(relx = columnRelValues[1], rely = lineRelValues[1], anchor = tkinter.NW)

terryCapshotTimeTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Capshot time", text_color = textColor, font = ("Arial", 18))
terryCapshotTimeTextDisplay.place(relx = columnRelValues[1], rely = lineRelValues[2], anchor = tkinter.NW)
terryCapshotTimeDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??:??:??", text_color = "white", font = ("Arial", 18))
terryCapshotTimeDisplay.place(relx = columnRelValues[1], rely = lineRelValues[3], anchor = tkinter.NW)

terryLimbsTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Limbs", text_color = textColor, font = ("Arial", 18))
terryLimbsTextDisplay.place(relx = columnRelValues[2], rely = lineRelValues[0], anchor = tkinter.NW)
terryLimb1Display = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
terryLimb1Display.place(relx = columnRelValues[2] , rely = lineRelValues[1], anchor = tkinter.NW)
terryLimb2Display = customtkinter.CTkLabel(fullSetFrame, text = "", text_color = "white", font = ("Arial", 18))
terryLimb2Display.place(relx = columnRelValues[2] + limbSpaceToPrevious, rely = lineRelValues[1], anchor = tkinter.NW)
terryLimb3Display = customtkinter.CTkLabel(fullSetFrame, text = "", text_color = "white", font = ("Arial", 18))
terryLimb3Display.place(relx = columnRelValues[2] + limbSpaceToPrevious*2, rely = lineRelValues[1], anchor = tkinter.NW)

terryLimbMedianTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Limb Median", text_color = textColor, font = ("Arial", 18))
terryLimbMedianTextDisplay.place(relx = columnRelValues[2], rely = lineRelValues[2], anchor = tkinter.NW)
terryLimbMedianDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
terryLimbMedianDisplay.place(relx = columnRelValues[2], rely = lineRelValues[3], anchor = tkinter.NW)

# Garry
garryWaterLimbBreakTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Water Limb Time", text_color = textColor, font = ("Arial", 18))
garryWaterLimbBreakTextDisplay.place(relx = columnRelValues[0], rely = lineRelValues[4], anchor = tkinter.NW)
garryWaterLimbBreakTimeDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
garryWaterLimbBreakTimeDisplay.place(relx = columnRelValues[0], rely = lineRelValues[5], anchor = tkinter.NW)

garryLastLimbBreakTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Last Limb Time", text_color = textColor, font = ("Arial", 18))
garryLastLimbBreakTextDisplay.place(relx = columnRelValues[0], rely = lineRelValues[6], anchor = tkinter.NW)
garryLastLimbBreakTimeDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
garryLastLimbBreakTimeDisplay.place(relx = columnRelValues[0], rely = lineRelValues[7], anchor = tkinter.NW)

garryCapshotTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Capshot", text_color = textColor, font = ("Arial", 18))
garryCapshotTextDisplay.place(relx = columnRelValues[1], rely = lineRelValues[4], anchor = tkinter.NW)
garryCapshotDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
garryCapshotDisplay.place(relx = columnRelValues[1], rely = lineRelValues[5], anchor = tkinter.NW)

garryLimbsTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Limbs", text_color = textColor, font = ("Arial", 18))
garryLimbsTextDisplay.place(relx = columnRelValues[2], rely = lineRelValues[4], anchor = tkinter.NW)
garryLimb1Display = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
garryLimb1Display.place(relx = columnRelValues[2], rely = lineRelValues[5], anchor = tkinter.NW)
garryLimb2Display = customtkinter.CTkLabel(fullSetFrame, text = "", text_color = "white", font = ("Arial", 18))
garryLimb2Display.place(relx = columnRelValues[2] + limbSpaceToPrevious, rely = lineRelValues[5], anchor = tkinter.NW)
garryLimb3Display = customtkinter.CTkLabel(fullSetFrame, text = "", text_color = "white", font = ("Arial", 18))
garryLimb3Display.place(relx = columnRelValues[2] + limbSpaceToPrevious*2, rely = lineRelValues[5], anchor = tkinter.NW)
garryLimb4Display = customtkinter.CTkLabel(fullSetFrame, text = "", text_color = "white", font = ("Arial", 18))
garryLimb4Display.place(relx = columnRelValues[2] + limbSpaceToPrevious*3, rely = lineRelValues[5], anchor = tkinter.NW)
garryLimb5Display = customtkinter.CTkLabel(fullSetFrame, text = "", text_color = "white", font = ("Arial", 18))
garryLimb5Display.place(relx = columnRelValues[2] + limbSpaceToPrevious*4, rely = lineRelValues[5], anchor = tkinter.NW)

garryLimbMedianTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Limb Median", text_color = textColor, font = ("Arial", 18))
garryLimbMedianTextDisplay.place(relx = columnRelValues[2], rely = lineRelValues[6], anchor = tkinter.NW)
garryLimbMedianDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
garryLimbMedianDisplay.place(relx = columnRelValues[2], rely = lineRelValues[7], anchor = tkinter.NW)

garryShrineTimeTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Shrine Time", text_color = textColor, font = ("Arial", 18))
garryShrineTimeTextDisplay.place(relx = columnRelValues[4], rely = lineRelValues[4], anchor = tkinter.NW)
garryShrineTimeDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
garryShrineTimeDisplay.place(relx = columnRelValues[4], rely = lineRelValues[5], anchor = tkinter.NW)

garryShardInsertsTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Shard Times", text_color = textColor, font = ("Arial", 18))
garryShardInsertsTextDisplay.place(relx = columnRelValues[4], rely = lineRelValues[6], anchor = tkinter.NW)
garryShardInsertsDisplay = customtkinter.CTkLabel(fullSetFrame, text = "?? ??", text_color = "white", font = ("Arial", 18))
garryShardInsertsDisplay.place(relx = columnRelValues[4], rely = lineRelValues[7], anchor = tkinter.NW)

# Harry
harryWaterLimbBreakTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Water Limb Time", text_color = textColor, font = ("Arial", 18))
harryWaterLimbBreakTextDisplay.place(relx = columnRelValues[0], rely = lineRelValues[8], anchor = tkinter.NW)
harryWaterLimbBreakTimeDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
harryWaterLimbBreakTimeDisplay.place(relx = columnRelValues[0], rely = lineRelValues[9], anchor = tkinter.NW)

harryLastLimbBreakTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Last Limb Time", text_color = textColor, font = ("Arial", 18))
harryLastLimbBreakTextDisplay.place(relx = columnRelValues[0], rely = lineRelValues[10], anchor = tkinter.NW)
harryLastLimbBreakTimeDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
harryLastLimbBreakTimeDisplay.place(relx = columnRelValues[0], rely = lineRelValues[11], anchor = tkinter.NW)

harryCapshotTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Capshot", text_color = textColor, font = ("Arial", 18))
harryCapshotTextDisplay.place(relx = columnRelValues[1], rely = lineRelValues[8], anchor = tkinter.NW)
harryCapshotDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
harryCapshotDisplay.place(relx = columnRelValues[1], rely = lineRelValues[9], anchor = tkinter.NW)

harryLimbsTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Limbs", text_color = textColor, font = ("Arial", 18))
harryLimbsTextDisplay.place(relx = columnRelValues[2], rely = lineRelValues[8], anchor = tkinter.NW)
harryLimb1Display = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
harryLimb1Display.place(relx = columnRelValues[2], rely = lineRelValues[9], anchor = tkinter.NW)
harryLimb2Display = customtkinter.CTkLabel(fullSetFrame, text = "", text_color = "white", font = ("Arial", 18))
harryLimb2Display.place(relx = columnRelValues[2] + limbSpaceToPrevious, rely = lineRelValues[9], anchor = tkinter.NW)
harryLimb3Display = customtkinter.CTkLabel(fullSetFrame, text = "", text_color = "white", font = ("Arial", 18))
harryLimb3Display.place(relx = columnRelValues[2] + limbSpaceToPrevious*2, rely = lineRelValues[9], anchor = tkinter.NW)
harryLimb4Display = customtkinter.CTkLabel(fullSetFrame, text = "", text_color = "white", font = ("Arial", 18))
harryLimb4Display.place(relx = columnRelValues[2] + limbSpaceToPrevious*3, rely = lineRelValues[9], anchor = tkinter.NW)
harryLimb5Display = customtkinter.CTkLabel(fullSetFrame, text = "", text_color = "white", font = ("Arial", 18))
harryLimb5Display.place(relx = columnRelValues[2] + limbSpaceToPrevious*4, rely = lineRelValues[9], anchor = tkinter.NW)

harryLimbMedianTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Limb Median", text_color = textColor, font = ("Arial", 18))
harryLimbMedianTextDisplay.place(relx = columnRelValues[2], rely = lineRelValues[10], anchor = tkinter.NW)
harryLimbMedianDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
harryLimbMedianDisplay.place(relx = columnRelValues[2], rely = lineRelValues[11], anchor = tkinter.NW)

harryShrineTimeTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Shrine Time", text_color = textColor, font = ("Arial", 18))
harryShrineTimeTextDisplay.place(relx = columnRelValues[4], rely = lineRelValues[8], anchor = tkinter.NW)
harryShrineTimeDisplay = customtkinter.CTkLabel(fullSetFrame, text = "??", text_color = "white", font = ("Arial", 18))
harryShrineTimeDisplay.place(relx = columnRelValues[4], rely = lineRelValues[9], anchor = tkinter.NW)

harryShardInsertsTextDisplay = customtkinter.CTkLabel(fullSetFrame, text = "Shard Times", text_color = textColor, font = ("Arial", 18))
harryShardInsertsTextDisplay.place(relx = columnRelValues[4], rely = lineRelValues[10], anchor = tkinter.NW)
harryShardInsertsDisplay = customtkinter.CTkLabel(fullSetFrame, text = "?? ??", text_color = "white", font = ("Arial", 18))
harryShardInsertsDisplay.place(relx = columnRelValues[4], rely = lineRelValues[11], anchor = tkinter.NW)

# Global overview
globalRunAvgTextDisplay = customtkinter.CTkLabel(globalOverviewFrame, text = "Run Avg.", text_color = textColor, font = ("Arial", 18))
globalRunAvgTextDisplay.place(relx = columnRelValues[0], rely = .2, anchor = tkinter.NW)
globalRunAvgDisplay = customtkinter.CTkLabel(globalOverviewFrame, text = "??", text_color = textColor, font = ("Arial", 18))
globalRunAvgDisplay.place(relx = columnRelValues[0], rely = .45, anchor = tkinter.NW)

globalCapshotMedianTextDisplay = customtkinter.CTkLabel(globalOverviewFrame, text = "Capshot Med.", text_color = textColor, font = ("Arial", 18))
globalCapshotMedianTextDisplay.place(relx = columnRelValues[1], rely = .2, anchor = tkinter.NW)
globalCapshotMedianDisplay = customtkinter.CTkLabel(globalOverviewFrame, text = "??", text_color = textColor, font = ("Arial", 18))
globalCapshotMedianDisplay.place(relx = columnRelValues[1], rely = .45, anchor = tkinter.NW)

globalLimbMedianTextDisplay = customtkinter.CTkLabel(globalOverviewFrame, text = "Limb Med.", text_color = textColor, font = ("Arial", 18))
globalLimbMedianTextDisplay.place(relx = columnRelValues[2], rely = .2, anchor = tkinter.NW)
globalLimbMedianDisplay = customtkinter.CTkLabel(globalOverviewFrame, text = "??", text_color = textColor, font = ("Arial", 18))
globalLimbMedianDisplay.place(relx = columnRelValues[2], rely = .45, anchor = tkinter.NW)

globalWaterMedianTextDisplay = customtkinter.CTkLabel(globalOverviewFrame, text = "Water Med.", text_color = textColor, font = ("Arial", 18))
globalWaterMedianTextDisplay.place(relx = columnRelValues[3] - .1, rely = .2, anchor = tkinter.NW)
globalWaterMedianDisplay = customtkinter.CTkLabel(globalOverviewFrame, text = "??", text_color = textColor, font = ("Arial", 18))
globalWaterMedianDisplay.place(relx = columnRelValues[3] - .1, rely = .45, anchor = tkinter.NW)

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

# Eido related classes
class LoadIn:
    def __init__(self) -> None:
    
        self.itsNighttimeTime = 0
        self.finalizeEidolonTransitionTime = 0
        self.hostEnterTime = 0

        self.displayFinalize = 0
        self.displayItsNightitme = 0

class Terry:
    def __init__(self) -> None:

        self.vulnerableTime = 0
        self.firstLimbTime = 0
        self.capshotTime = 0
        self.lastLimbTimeSeconds = 0

        self.limbs = []
        self.limbsForMedian = []
        self.limbDisplays = []
        self.limbDisplays.append(terryFirstLimbBreakTimeDisplay)
        self.limbDisplays.append(terryLimb1Display)
        self.limbDisplays.append(terryLimb2Display)
        self.limbDisplays.append(terryLimb3Display)

        self.displayFirstLimb = 0
        self.displayTimeToVuln = 0
        self.displayCapshot = 0
        self.displayCapshotRealtime = 0
        self.displayLastLimbTime = 0
        self.displayMedian = 0
        

class Garry:
    def __init__(self) -> None:
        
        self.lootDropTime = 0
        self.shrineEnabledTime = 0
        self.shardOneTime = 0
        self.shardTwoTime = 0
        self.spawnDelay = 0
        self.spawnTime = 0
        self.waterLimbBreakTime = 0
        self.capshotTime = 0
        self.lastLimbTimeSeconds = 0

        self.limbs = []
        self.limbsForMedian = []
        self.limbDisplays = []
        self.limbDisplays.append(garryWaterLimbBreakTimeDisplay)
        self.limbDisplays.append(garryLimb1Display)
        self.limbDisplays.append(garryLimb2Display)
        self.limbDisplays.append(garryLimb3Display)
        self.limbDisplays.append(garryLimb4Display)
        self.limbDisplays.append(garryLimb5Display)

        self.displayShrineTime = 0
        self.displayWaterTime = 0
        self.displayspawnDelay = 0
        self.displayShardOneTime = 0
        self.displayShardTwoTime = 0
        self.displayCapshot = 0
        self.displayLastLimbTime = 0
        self.displayMedian = 0
    
class Harry:
    def __init__(self) -> None:

        self.lootDropTime = 0
        self.shrineEnabledTime = 0
        self.shardOneTime = 0
        self.shardTwoTime = 0
        self.spawnDelay = 0
        self.spawnTime = 0
        self.waterLimbBreakTime = 0
        self.capshotTime = 0
        self.lastLimbTimeSeconds = 0

        self.limbs = []
        self.limbsForMedian = []
        self.limbDisplays = []
        self.limbDisplays.append(harryWaterLimbBreakTimeDisplay)
        self.limbDisplays.append(harryLimb1Display)
        self.limbDisplays.append(harryLimb2Display)
        self.limbDisplays.append(harryLimb3Display)
        self.limbDisplays.append(harryLimb4Display)
        self.limbDisplays.append(harryLimb5Display)

        self.displayShrineTime = 0
        self.displayWaterTime = 0
        self.displayspawnDelay = 0
        self.displayShardOneTime = 0
        self.displayShardTwoTime = 0
        self.displayCapshot = 0
        self.displayLastLimbTime = 0
        self.displayMedian = 0

# Full set class
class FullSet:    
    def __init__(self, setNr):

        self.setNumber = setNr
        self.isFirstSet = False

        self.loadIn = LoadIn()
        self.terry = Terry()
        self.garry = Garry()
        self.harry = Harry()
        self.lastLimbBreakTime = 0
        self.extractTime = 0

class FullNight:
    def __init__(self) -> None:
        self.sets = []
        self.average = 0

        self.runTimesForAverage = []
        self.capshotsForMedian = []
        self.limbsForMedian = []
        self.watersForMedian = []

fullNight = None

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


# More UI Elements
leftFrame = customtkinter.CTkFrame(app, width = 300, height = 200)
leftFrame.pack_propagate(0)
leftFrame.place(relx = .3, rely = .03, anchor = tkinter.N)

rightFrame = customtkinter.CTkFrame(app, width = 300, height = 200)
rightFrame.pack_propagate(0)
rightFrame.place(relx = .7, rely = .03, anchor = tkinter.N)

deltaDisplay400 = customtkinter.CTkLabel(leftFrame, text="Delta Time (.400)", text_color="white", font=("Arial", 24))
deltaDisplay400.place(relx = .5, rely = .17, anchor = tkinter.N)
deltaDisplayNightime = customtkinter.CTkLabel(leftFrame, text="Delta Time (3.600)", text_color="white", font=("Arial", 24))
deltaDisplayNightime.place(relx = .5, rely = .32, anchor = tkinter.N)

statusDisplay = customtkinter.CTkLabel(leftFrame, text="Awaiting Status", text_color="cyan", font=("Arial", 40))
statusDisplay.place(relx = .5, rely = .52, anchor = tkinter.N)

shrineTimeText = customtkinter.CTkLabel(rightFrame, text="Shrine Time", text_color="white", font=("Arial", 28))
shrineTimeText.place(relx = .5, rely = .22, anchor = tkinter.N)
shrineTimeDisplay = customtkinter.CTkLabel(rightFrame, text="0.000", text_color="white", font=("Arial", 24))
shrineTimeDisplay.place(relx = .5, rely = .4, anchor = tkinter.N)

restartParsingButton = None
stopParsingButton = None

previousSetButton = None
nextSetButton = None
currentSetShown = 0

def previousSet():
    global currentSetShown
    
    if currentSetShown > 0:
        currentSetShown -= 1
        changeSetDisplay(str(currentSetShown))
    return

def nextSet():
    global currentSetShown
    
    if currentSetShown < currentSetNr:
        currentSetShown += 1
        changeSetDisplay(str(currentSetShown))
    return

# Next/Prev sets buttons 
previousSetButton = customtkinter.CTkButton(
    app,
    text="<",
    font=("Arial", 14),
    width = 20,
    height = 20,
    command = previousSet
)
previousSetButton.place(relx = optionsMenuX - .13, rely = optionsMenuY + .003, anchor = tkinter.N)

nextSetButton = customtkinter.CTkButton(
    app,
    text=">",
    font=("Arial", 14),
    width = 20,
    height = 20,
    command = nextSet
)
nextSetButton.place(relx = optionsMenuX - .1, rely = optionsMenuY + .003, anchor = tkinter.N)


def stopParsing():
    global stopParsingBool
    global stopParsingButton
    global restartParsingButton

    stopParsingBool = True

    stopParsingButton.destroy()

    restartParsingButton = customtkinter.CTkButton(app, text="Restart", font=("Arial", 20), width = 100, height = 40, command = restartParsing)
    restartParsingButton.place(relx = stopParsingButtonX, rely = stopParsingButtonY, anchor = tkinter.N)


def restartParsing():
    global stopParsingButton
    global restartParsingButton

    restartParsingButton.destroy()

    stopParsingButton = customtkinter.CTkButton(app, text="Stop", font=("Arial", 20), width = 100, height = 40, command = stopParsing)
    stopParsingButton.place(relx = stopParsingButtonX, rely = stopParsingButtonY, anchor = tkinter.N)

    app.after(200, startParsing)

# Stop parsing button
stopParsingButton = customtkinter.CTkButton(
    app,
    text="Stop",
    font=("Arial", 20),
    width = 100,
    height = 40,
    command = stopParsing
)
stopParsingButton.place(relx = stopParsingButtonX, rely = stopParsingButtonY, anchor = tkinter.N)

# Search String constants
searchHostEntering = "EidolonMP.lua: Host entering plains with MissionInfo:"
searchFinalizeTransition = "EidolonMP.lua: EIDOLONMP: Finalize Eidolon transition"
searchItsNightime = "TeralystEncounter.lua: It's nighttime!"

searchEidoCaptured = "TeralystAvatarScript.lua: Teralyst Captured"
searchEidoKilled = "TeralystAvatarScript.lua: Teralyst Killed"

searchTeralystSpawned = "TeralystEncounter.lua: Teralyst spawned"
searchWeakpointDestroyed = "TeralystAvatarScript.lua: Weakpoint Destroyed"

searchWaterEidoSpawn = "Eidolon spawning SUCCESS"

searchLootDrop = "SnapPickupToGround.lua: Snapping pickup to ground (DefaultArcanePickup)"
searchShrineEnabled = "TeralystEncounter.lua: Shrine enabled"
searchShardOne = "TeralystEncounter.lua: A shard has been put in the Eidolon Shrine. Shards Consumed = 1"
searchShardTwo = "TeralystEncounter.lua: A shard has been put in the Eidolon Shrine. Shards Consumed = 2"

searchHostUnload = "EidolonMP.lua: EIDOLONMP: Level fully destroyed"

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
            if searchHostUnload in line:
                reset = True
                break

            # In case of direct to plains
            elif searchItsNightime in line:
                nighttimeTime = float(trimmedTime)
                orbiterReset = True
                break

            # Terry spawn
            elif currentSet.terry.vulnerableTime == 0 and searchTeralystSpawned in line:
                try:
                    currentSet.terry.vulnerableTime = float(trimmedTime)
                except:
                    print("Trying to set currentSet.terry.vulnerableTime: \n" + line + "\n")
                    file.seek(fileRollbackPosition)
                    break

            # First limb
            elif currentLimb == 0 and searchWeakpointDestroyed in line:
                try:
                    currentSet.terry.limbs.append(float(trimmedTime))
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
            
                # Update median
                medianValue = "{:.3f}".format(statistics.median(currentSet.terry.limbsForMedian))
                terryLimbMedianDisplay.configure(text = medianValue)
                currentSet.terry.displayMedian = medianValue

                # Update global median
                fullNight.limbsForMedian.append(float(limbTimeSeconds))
                updateGlobalLimbMed()                

            # Capture 
            elif searchEidoCaptured in line:
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




# Run parser function
app.after(500, startParsing)

# Run app window
app.mainloop()


