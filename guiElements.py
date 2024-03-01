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