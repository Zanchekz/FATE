import tkinter
import customtkinter

import constants
from parsing import startParsing
from PIL import Image

# System Settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
customtkinter.deactivate_automatic_dpi_awareness()

# App window - Size and Title
app = customtkinter.CTk()
app.geometry("960x960")
app.title("FATE")
app.iconbitmap("C:/Users/Vlados/Downloads/randomicon.ico")

fullSetFrame = customtkinter.CTkFrame(app, width = app._current_width - 20, height = app._current_height/2 - 10)
fullSetFrame.pack_propagate(0)
fullSetFrame.place(relx = .5, rely = .35, anchor = tkinter.N)

globalOverviewFrame = customtkinter.CTkFrame(app, width = app._current_width - 20, height = app._current_height/8 - 10)
globalOverviewFrame.pack_propagate(0)
globalOverviewFrame.place(relx = .5, rely = .85, anchor = tkinter.N)

# GUI commands for widgets
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

# Option menu for set to display
setsOptionMenuLabel = customtkinter.CTkLabel(app, text = "Select set to show", text_color = textColor, font = ("Arial", 18))
setsOptionMenuLabel.place(relx = optionsMenuX, rely = optionsMenuY - .03, anchor = tkinter.N)
setsOptionMenu = customtkinter.CTkOptionMenu(app, values=[], command = changeSetDisplay)
setsOptionMenu.place(relx = optionsMenuX, rely = optionsMenuY, anchor = tkinter.N)

# Next/Prev sets buttons 
previousSetButton = customtkinter.CTkButton(app, text="<", font=("Arial", 14), width = 20, height = 20, command = previousSet)
previousSetButton.place(relx = optionsMenuX - .13, rely = optionsMenuY + .003, anchor = tkinter.N)

nextSetButton = customtkinter.CTkButton(app, text=">", font=("Arial", 14), width = 20, height = 20, command = nextSet)
nextSetButton.place(relx = optionsMenuX - .1, rely = optionsMenuY + .003, anchor = tkinter.N)

# Stop parsing button
stopParsingButton = customtkinter.CTkButton(app, text="Stop", font=("Arial", 20), width = 100, height = 40, command = stopParsing)
stopParsingButton.place(relx = stopParsingButtonX, rely = stopParsingButtonY, anchor = tkinter.N)

# Sealed
seal_light = Image.open("C:/Users/Vlados/Downloads/sealer.png")
seal_dark = Image.open("C:/Users/Vlados/Downloads/sealer.png")
sealImage = customtkinter.CTkImage(seal_light, seal_dark, size=(300, 130))
sealLabel = customtkinter.CTkLabel(app, image = sealImage, fg_color = "transparent", bg_color = "transparent", text = "")
sealLabel.place(x = 820, y = 70)

class Terry:
    def __init__(self) -> None:

        self.vulnerableTime = 0
        self.firstLimbTime = 0
        self.capshotTime = 0
        self.lastLimbTimeSeconds = 0
        self.timer_task_id = ''

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

#Night related classes
class LoadIn:
    def __init__(self) -> None:
    
        self.itsNighttimeTime = 0
        self.finalizeEidolonTransitionTime = 0
        self.hostEnterTime = 0

        self.displayFinalize = 0
        self.displayItsNightitme = 0

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