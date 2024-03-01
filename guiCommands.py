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
    
