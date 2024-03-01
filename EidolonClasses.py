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
