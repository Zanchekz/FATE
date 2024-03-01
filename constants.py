import os
import re
import statistics
import datetime

# Set the filename and open the file
# filename = os.getenv('LOCALAPPDATA') + '\Warframe\EE.log'
filename = os.getenv('LOCALAPPDATA') + '\Warframe\EE.log'
file = None
fileRollbackPosition = None
fileRollbackPositionSmall = None

# Various miscelaneous variables and values
stopParsingBool = False
sleepBetweenCalls = 1000

# Search String constants
searchHostEntering = "EidolonMP.lua: Host entering plains with MissionInfo:"
searchFinalizeTransition = "EidolonMP.lua: EIDOLONMP: Finalize Eidolon transition"
searchItsNightime = "TeralystEncounter.lua: It's nighttime!"

searchEidoCaptured = "TeralystAvatarScript.lua: Teralyst Captured"
searchEidoKilled = "TeralystAvatarScript.lua: Teralyst Killed"

searchTeralystSpawned = "TeralystEncounter.lua: Teralyst spawned"
searchTeralystNotSpawning = ["TeralystEncounter.lua: Teralyst didn't spawn, but should have", "TeralystEncounter.lua: Couldn't find any teralyst spawns, so not spawning one."]
searchWeakpointDestroyed = "TeralystAvatarScript.lua: Weakpoint Destroyed"

searchWaterEidoSpawn = "Eidolon spawning SUCCESS"

searchLootDrop = "SnapPickupToGround.lua: Snapping pickup to ground (DefaultArcanePickup)"
searchShrineEnabled = "TeralystEncounter.lua: Shrine enabled"
searchShardOne = "TeralystEncounter.lua: A shard has been put in the Eidolon Shrine. Shards Consumed = 1"
searchShardTwo = "TeralystEncounter.lua: A shard has been put in the Eidolon Shrine. Shards Consumed = 2"

searchHostUnload = "EidolonMP.lua: EIDOLONMP: Level fully destroyed"

# GUI constants
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

#misc constants
currentSetNr = 0
currentSet = None
fullNight = None

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