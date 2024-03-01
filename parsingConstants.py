# Set the filename and open the file
# filename = os.getenv('LOCALAPPDATA') + '\Warframe\EE.log'
filename = os.getenv('LOCALAPPDATA') + '\Warframe\EE.log'
file = None
fileRollbackPosition = None
fileRollbackPositionSmall = None

# Various miscelaneous variables and values
stopParsingBool = False
sleepBetweenCalls = 1000

#for seal???
fullNight = None

# Search String constants
searchHostEntering = "EidolonMP.lua: Host entering plains with MissionInfo:"
searchFinalizeTransition = "EidolonMP.lua: EIDOLONMP: Finalize Eidolon transition"
searchItsNightime = "TeralystEncounter.lua: It's nighttime!"

searchEidoCaptured = "TeralystAvatarScript.lua: Teralyst Captured"
searchEidoKilled = "TeralystAvatarScript.lua: Teralyst Killed"

searchTeralystSpawned = "TeralystEncounter.lua: Teralyst spawned"
searchTeralystNotSpawning = ["TeralystEncounter.lua: Teralyst didn't spawn, but should have", "TeralystEncounter.lua: Couldn't find any teralyst spawns, so not spawning one."]
searchSongComplete = "TeralystAvatarScript.lua: Swan Song Complete"
searchWeakpointDestroyed = "TeralystAvatarScript.lua: Weakpoint Destroyed"

searchWaterEidoSpawn = "Eidolon spawning SUCCESS"

searchLootDrop = "SnapPickupToGround.lua: Snapping pickup to ground (DefaultArcanePickup)"
searchShrineEnabled = "TeralystEncounter.lua: Shrine enabled"
searchShardOne = "TeralystEncounter.lua: A shard has been put in the Eidolon Shrine. Shards Consumed = 1"
searchShardTwo = "TeralystEncounter.lua: A shard has been put in the Eidolon Shrine. Shards Consumed = 2"

searchHostUnload = "EidolonMP.lua: EIDOLONMP: Level fully destroyed"