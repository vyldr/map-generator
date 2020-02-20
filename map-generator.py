import random
import time
import os.path
import sys

def main():
    parameters = {
        "length":               64,                             # How long to make the map
        "width":                64,                             # How wide to make the map
        "size":                 False,                          # Overrides length and width
        "solidDensity":         random.random() * 0.5,          # How much solid rock to generate
        "wallDensity":          random.random() * 0.3 + 0.3,    # How much other rock to generate
        "oreDensity":           random.random() * 0.3 + 0.3,    # How common ore is
        "crystalDensity":       random.random() * 0.3 + 0.2,    # How common energy crystals are
        "oreSeamDensity":       random.random() * 0.25,         # How common ore seams are
        "crystalSeamDensity":   random.random() * 0.5,          # How common energy crystal seams are
        "rechargeSeamDensity":  random.random() * 0.08 + 0.01,  # How common recharge seams are
        "floodLevel":           random.random() * 0.75,         # The height to be flooded with water or lava
        "floodType":            False,                          # Whether to flood with water or lava
        "flowDensity":          random.random() * 0.005,        # How common erosion sources are
        "flowInterval":         random.randint(30, 180),        # How slow erosion spreads
        "preFlow":              random.randint(3, 8),           # How much erosion should spread before the level starts
        "landslideDensity":     random.random() * 0.7,          # How common landslide sources are
        "landslideInterval":    random.randint(10, 300),        # How long between landslides
        "monsterDensity":       random.random() * 0.0,          # How common monster sources are
        "monsterInterval":      random.randint(30, 120),        # How long between monster attacks
        "slugDensity":          random.random() * 0.08,         # How common slimy slug holes are
        "terrain":              5,          # How much the height of the terrain varies
        "smoothness":           16,         # How smoothly the terrain slopes
        "oxygen":               False,      # How much oxygen to start with
        "biome":                False,      # Which biome to use
        "show":                 False,      # Whether to show the map
        "stats":                True,       # Whether to show the statistics
        "save":                 True,       # Whether to save the file
        "name":                 'Untitled', # What to name the file
    }

    # Apply any args from the command line
    for i in range(1, len(sys.argv) - 1):
        if sys.argv[i][0] == '-':
            if isInt(sys.argv[i + 1]):
                parameters[sys.argv[i][1:]] = int(sys.argv[i + 1])
            elif isFloat(sys.argv[i + 1]):
                parameters[sys.argv[i][1:]] = float(sys.argv[i + 1])
            elif isBool(sys.argv[i + 1]):
                parameters[sys.argv[i][1:]] = isTrue(sys.argv[i + 1])
            else:
                parameters[sys.argv[i][1:]] = sys.argv[i + 1]

    # Keep trying until we get one or give up after 100 times
    attempts = 1
    done = False
    while not done and attempts < 100:
        output = mapgen(parameters)
        if output != False:
            if parameters["save"] == True:
                saveFile(parameters["name"], output)
            done = True
        attempts += 1


def mapgen(params):
    # Start the timer
    start = time.process_time()

    # Set length and width
    if params["size"]:
        params["length"] = params["size"]
        params["width"] = params["size"]

    # Optionally set oxygen
    if not params["oxygen"]:
        params["oxygen"] = params["length"] * params["width"] * 3

    # Create feature maps
    solidArray = createArray(params["length"], params["width"], -1)  # Solid rock
    wallArray = createArray(params["length"], params["width"], -1)  # Other rock

    # Create the solid rock
    randomize(solidArray, 1 - params["solidDensity"])
    smooth(solidArray)
    cleanup(solidArray)
    if fillExtra(solidArray) == False:  # This is a chance to test map sanity
        return False

    # Create the other rocks
    randomize(wallArray, 1 - params["wallDensity"])
    smooth(wallArray)
    cleanup(wallArray)
    details(wallArray, 3)

    # Merge the permnent and temporary features
    for i in range(params["length"]):
        for j in range(params["width"]):
            if solidArray[i][j] == -1:
                wallArray[i][j] = 4

    # Create ore
    oreArray = createArray(params["length"], params["width"], -1)
    randomize(oreArray, 1 - params["oreDensity"])
    smooth(oreArray)
    cleanup(oreArray)
    details(oreArray, 4)

    # Create crystals
    crystalArray = createArray(params["length"], params["width"], -1)
    randomize(crystalArray, 1 - params["crystalDensity"])
    smooth(crystalArray)
    cleanup(crystalArray)
    details(crystalArray, 5)

    # Creat a height map
    heightArray = heightMap(params["length"] + 1, params["width"] + 1, params["terrain"], params["smoothness"])

    # Choose a biome
    if not params["biome"]:
        params["biome"] = ["ice","rock","lava"][random.randint(0, 2)]

    # Optionally set the flood type
    if params["floodType"] == "water":
        params["floodType"] = 6  # Water
    if params["floodType"] == "lava":
        params["floodType"] = 7  # Lava

    # It seems wrong to have water in a lava biome or lava in an ice biome
    if not params["floodType"]:
        if params["biome"] == "ice":
            params["floodType"] = 6  # Water
        elif params["biome"] == "lava":
            params["floodType"]= 7  # Lava
        else:  # Rock
            params["floodType"] = random.randint(6, 7)  # Water or lava

    # Flood the low areas
    flood(wallArray, heightArray, params["floodLevel"], params["floodType"])

    # Organize the maps
    for i in range(params["length"]):
        for j in range(params["width"]):
            if wallArray[i][j] not in range(1, 4):
                crystalArray[i][j] = 0
                oreArray[i][j] = 0

    # Lava Flows / Erosion
    flowList = []
    if params["biome"] == 'lava':
        params["flowDensity"] *= 3
    if params["floodType"] == 7:
        flowList = createFlowList(wallArray, params["flowDensity"], heightArray, params["preFlow"])

    # Set unstable walls and landslide rubble
    landslideList = aLandslideHasOccured(wallArray, params["landslideDensity"])

    # Set monster spawn points.  I have no idea if this works
    monsterList = aMonsterHasAppeared(wallArray, params["monsterDensity"])

    # Slimy Slug holes
    aSlimySlugIsInvadingYourBase(wallArray, params["slugDensity"])

    # Energy Crystal Seams
    addSeams(wallArray, crystalArray, params["crystalSeamDensity"], 10)

    # Ore Seams
    addSeams(wallArray, oreArray, params["oreSeamDensity"], 11)

    # Recharge seams
    addRechargeSeams(wallArray, params["rechargeSeamDensity"], 12)

    # Set the starting point
    base = chooseBase(wallArray)
    if base == False:  # Make sure there is space to build
        return False
    setBase(base[0], wallArray, heightArray)

    # List undiscovered caverns
    caveList = findCaves(wallArray, base[0])


    # Finish up

    MMtext = convertToMM(
        wallArray,
        caveList,
        params["biome"],
        heightArray,
        crystalArray,
        oreArray,
        params["monsterInterval"],
        monsterList,
        params["landslideInterval"],
        landslideList,
        params["flowInterval"],
        flowList,
        base,
        params["oxygen"],
        params["name"],
    )

    # Optionally display the map
    if params["show"] == True:
        display(wallArray)
    if params["show"] == "height":
        displayArr(heightArray)
    if params["show"] == "both":
        display(wallArray)
        displayArr(heightArray)

    # Stop timing
    finish = time.process_time()

    # Optionally show the stats
    if params["stats"]:
        print('Parameters:')
        for key in params.keys():
            print('    ', key, ': ', params[key], sep='')

        print('\nResults:')
        print('    Size: ', params["length"], 'x', params["width"])
        print('    Tiles:', params["length"] * params["width"])
        print('    Time: ', finish - start, 'seconds')
        print('    Speed:', (params["length"] * params["width"]) / (finish - start), 'tiles per second')

    return MMtext


# Add Energy Crystal and Ore seams
def addSeams(array, resourceArray, density, type):
    for i in range(len(array)):
        for j in range(len(array[0])):
            if resourceArray[i][j] > 2 and random.random() < density:
                array[i][j] = type


# Add recharge seams in to replace solid rock
def addRechargeSeams(array, density, type):
    for i in range(1, len(array) - 1):
        for j in range(1, len(array[0]) - 1):
            # Only if at least two opposite sides have solid rock
            if ((((array[i + 1][j] == 4) and
                (array[i - 1][j] == 4)) or
                ((array[i][j + 1] == 4) and
                (array[i][j - 1] == 4))) and
                # Only if at least one side is or can become ground
                ((array[i + 1][j] < 4) or (array[i - 1][j] < 4) or (array[i][j + 1] < 4) or (array[i][j - 1] < 4))):
                if random.random() < density:
                    array[i][j] = 12  # Recharge seam



# A landslide has occured
def aLandslideHasOccured(array, stability):
    landslideArray = createArray(len(array), len(array[0]), -1)
    randomize(landslideArray, 1 - stability)
    details(landslideArray, 3)

    # Build the list
    landslideList = [[], [], []]  # Three different landslide frequencies
    for i in range(1, len(array) - 1):
        for j in range(1, len(array[0]) - 1):
            # Fill in rubble
            if landslideArray[i][j] > 0 and array[i][j] == 0:  # Ground
                array[i][j] = 8  # Landslide rubble
            # Landslides are possible here
            if landslideArray[i][j] > 0 and array[i][j] in range(1, 4):
                landslideList[landslideArray[i][j] - 1].append((i, j))

    return landslideList


# A monster has appered!
def aMonsterHasAppeared(array, population):
    monsterArray = createArray(len(array), len(array[0]), -1)
    randomize(monsterArray, 1 - population)
    smooth(monsterArray)
    details(monsterArray, 3)

    # Build the list
    monsterList = [[], [], []]  # Three different monster frequencies
    for i in range(1, len(array) - 1):
        for j in range(1, len(array[0]) - 1):
            # Sleeping monsters
            # if monsterArray[i][j] > 0 and array[i][j] == 0:  # Ground
                # TODO: add sleeping monsters here
            # Monsters can appear here
            if monsterArray[i][j] > 0 and array[i][j] in range(1, 4):
                monsterList[monsterArray[i][j] - 1].append((i, j))

    return monsterList


# A Slimy Slug is invading your base!
def aSlimySlugIsInvadingYourBase(array, slugDensity):
    for i in range(len(array)):
        for j in range(len(array[0])):
            # Randomly set Slimy Slug holes
            if array[i][j] == 0:  # Ground
                if random.random() < slugDensity:
                    array[i][j] = 9  # Slimy Slug hole


# Choose a starting point
def chooseBase(array):
    # Find all possible starting points
    possibleBaseList = []
    for i in range(1, len(array) - 2):
        for j in range(1, len(array[0]) - 2):
            # Check for a 2x2 ground section to build on
            if ((array[i][j] == 0) and
                (array[i + 1][j] == 0) and
                (array[i][j + 1] == 0) and
                (array[i + 1][j + 1] == 0)):
                possibleBaseList.append((i, j))

    # Make sure there is somewhere to build
    if len(possibleBaseList) == 0:
        return False

    # Choose one  TODO: Maybe choose multiple bases
    return [possibleBaseList[random.randint(0, len(possibleBaseList) - 1)]]


# Clean up small map features
def cleanup(array):
    changed = True
    while changed == True:
        changed = False
        for i in range(1, len(array) - 1):
            for j in range(1, len(array[0]) - 1):
                if (((array[i - 1][j] == 0) and (array[i + 1][j] == 0)) or ((array[i][j - 1] == 0) and (array[i][j + 1] == 0))):
                    if array[i][j] != 0:
                        array[i][j] = 0
                        changed = True


# Convert to Manic Miners file format
def convertToMM(walls,
                caveList,
                biome,
                height,
                crystals,
                ore,
                monsterInterval,
                monsterList,
                landslideInterval,
                landslideList,
                flowInterval,
                flowList,
                base,
                oxygen,
                name,
            ):
    # Basic info
    MMtext = (
        'info{\n' +
        'rowcount:' + str(len(walls)) + '\n' +
        'colcount:' + str(len(walls[0])) + '\n' +
        'camerapos:Translation: X=' + str(base[0][1] * 300 + 300) +
                              ' Y=' + str(base[0][0] * 300 + 300) +
                              ' Z=' + str(height[base[0][0]][base[0][1]]) +
                              ' Rotation: P=0.000000 Y=0.000000 R=0.000000 Scale X=1.000 Y=1.000 Z=1.000\n' +
        'cameraangle:0,45,0\n' +
        'biome:' + biome + '\n' +
        'creator:Map Generator for Manic Miners\n' +
        'oxygen:' + str(oxygen) + '/' + str(oxygen) + '\n' +
        'camerazoom:600.0\n' +
        'levelname:' + name + '\n' +
        'erosioninitialwaittime:10\n' +
        '}\n'
    )

    # Convert the tile numbers
    MMtext += 'tiles{\n'
    conversion = {
        0:  '1',   # Ground
        1:  '26',  # Dirt
        2:  '30',  # Loose Rock
        3:  '34',  # Hard Rock
        4:  '38',  # Solid Rock
        6:  '11',  # Water
        7:  '6',   # Lava
        8:  '63',  # Landslide rubble
        9:  '12',  # Slimy Slug hole
        10: '42',  # Energy Crystal Seam
        11: '46',  # Ore Seam
        12: '50',  # Recharge Seam
        13: '14',  # Building power path
    }

    # Apply the conversion
    for i in range(len(walls)):
        for j in range(len(walls[0])):
            walls[i][j] = conversion[walls[i][j]]

    # Hide undiscovered caverns
    for cave in caveList:
        for space in cave:
            walls[space[0]][space[1]] = str(int(walls[space[0]][space[1]]) + 100)

    # Add to the file
    for i in range(len(walls)):
        for j in range(len(walls[0])):
            MMtext += walls[i][j] + ','
        MMtext += '\n'
    MMtext += '}\n'

    # Add the heights
    MMtext += 'height{\n'
    for i in range(len(height)):
        for j in range(len(height[0])):
            MMtext += str(height[i][j]) + ','
        MMtext += '\n'
    MMtext += '}\n'

    # Add the resources
    MMtext += 'resources{\n'

    # Crystals
    MMtext += 'crystals:\n'
    for i in range(len(walls)):
        for j in range(len(walls[0])):
            MMtext += str(crystals[i][j]) + ','
        MMtext += '\n'

    # Ore
    MMtext += 'ore:\n'
    for i in range(len(walls)):
        for j in range(len(walls[0])):
            MMtext += str(ore[i][j]) + ','
        MMtext += '\n'
    MMtext += '}\n'

    # Objectives
    crystalCount = 0
    for i in range(len(walls)):
        for j in range(len(walls[0])):
            crystalCount += crystals[i][j]
    MMtext += 'objectives{\n'
    # Collect half of the crystals
    MMtext += 'resources: ' + str(crystalCount // 2) + ',0,0\n'
    MMtext += '}\n'

    # Buildings
    MMtext += 'buildings{\n'
    MMtext += (
        'BuildingToolStore_C\n' +
        'Translation: X=' + str(base[0][1] * 300 + 150.000) +
                    ' Y=' + str(base[0][0] * 300 + 150.000) +
                    ' Z=' + str(height[base[0][0]][base[0][1]]) +
                    '1.000 Rotation: P=0.000000 Y=-89.999992 R=0.000000 Scale X=1.000 Y=1.000 Z=1.000\n' +
        'Level=1\n' +
        'Teleport=True\n' +
        'Health=MAX\n' +
        'Powerpaths=X=14 Y=7 Z=5/X=14 Y=7 Z=4/\n'  # TODO: Solve this part
    )
    MMtext += '}\n'

    # Monsters.  I hope this works
    MMtext += 'monsters{\n'
    MMtext += '}\n'
    MMtext += 'monsterInterval{\n'
    for i in range(1, len(monsterList) + 1):
        if len(monsterList[i - 1]):
            MMtext += str(i * monsterInterval) + ':'
        for space in monsterList[i - 1]:
            MMtext += str(space[0]) + ',' + str(space[1]) + '/'
        if len(monsterList[i - 1]):
            MMtext += '\n'
    MMtext += '}\n'

    # A landslide has occured
    MMtext += 'landslideInterval{\n'
    for i in range(1, len(landslideList) + 1):
        if len(landslideList[i - 1]):
            MMtext += str(i * landslideInterval) + ':'
        for space in landslideList[i - 1]:
            MMtext += str(space[0]) + ',' + str(space[1]) + '/'
        if len(landslideList[i - 1]):
            MMtext += '\n'
    MMtext += '}\n'

    # Erosion
    MMtext += 'lavaspread{\n'
    for i in range(1, len(flowList) + 1):
        if len(flowList[i - 1]):
            MMtext += str(i * flowInterval) + ':'
        for space in flowList[i - 1]:
            MMtext += str(space[0]) + ',' + str(space[1]) + '/'
        if len(flowList[i - 1]):
            MMtext += '\n'
    MMtext += '}\n'

    # Miners
    MMtext += 'miners{\n'
    MMtext += '}\n'

    # Briefing
    MMtext += 'briefing{\n'
    MMtext += 'You must collect ' + str(crystalCount // 2) + ' energy crystals.  \n'
    MMtext += '}\n'

    return MMtext


# Create an array and fill it with something
def createArray(x, y, fill):
    array = [None] * x
    for i in range(x):
        array[i] = [None] * y
        for j in range(y):
            array[i][j] = fill

    return array


# Create a list of lava flow spaces
def createFlowList(array, density, height, preFlow):
    flowArray = createArray(len(array), len(array[0]), -1)
    spillList = []
    flowSourceList = []
    sources = []

    # Find places where lava flows are possible
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == 0:
                flowSourceList.append((i, j))  # Possible lava source
            if array[i][j] in range(4):
                flowArray[i][j] = 0  # Possible spill zone

    # Choose sources
    for i in range(len(flowSourceList), 0, -1):
        if random.random() < density:
            sources.append(flowSourceList[i-1])

    # Start spilling from each source
    for source in sources:
        array[source[0]][source[1]] = 7  # Lava
        flowList = [source]
        flowArray[source[0]][source[1]] = 1  # Checked

        # Sum of all corners.  Not really elevation but close enough
        sourceElevation = (
            (height[source[0]][source[1]]) +
            (height[source[0] + 1][source[1]]) +
            (height[source[0]][source[1] + 1]) +
            (height[source[0] + 1][source[1] + 1])
        )

        # Find spill zones
        i = 0
        while i < len(flowList):
            adjacent = [
                (flowList[i][0] + 1, flowList[i][1]),
                (flowList[i][0] - 1, flowList[i][1]),
                (flowList[i][0], flowList[i][1] + 1),
                (flowList[i][0], flowList[i][1] - 1),
            ]
            # Add to flowList if not checked and lower elevation
            for space in adjacent:
                # Sum of all corners.  Not really elevation but close enough
                elevation = (
                    (height[space[0]][space[1]]) +
                    (height[space[0] + 1][space[1]]) +
                    (height[space[0]][space[1] + 1]) +
                    (height[space[0] + 1][space[1] + 1])
                )
                if flowArray[space[0]][space[1]] == 0 and sourceElevation > elevation:
                    flowList.append(space)
                    flowArray[space[0]][space[1]] = 1  # Checked
            i += 1



        # Add the flowList to the spillList
        spillList.append(flowList)

        # Clean up the array for reuse
        for space in flowList:
            flowArray[space[0]][space[1]] = 0

    # Preflow the lavaflows so the sources are not just lonely lava squares
    for i in range(preFlow):
        totalSources = len(sources)
        for j in range(totalSources):
        # for source in sources:
            adjacent = [
                (sources[j][0] + 1, sources[j][1]),
                (sources[j][0] - 1, sources[j][1]),
                (sources[j][0], sources[j][1] + 1),
                (sources[j][0], sources[j][1] - 1),
            ]
            for space in adjacent:
                if array[space[0]][space[1]] == 0:
                    array[space[0]][space[1]] = 7  # Lava
                    sources.append(space)

    # TODO: Check whether it matters if the source space is included in the list

    return spillList


# Set the details based on the distance from open areas
def details(array, maxDistance):
    # Set type equal to distance from edge
    for n in range(maxDistance):
        for i in range(1, len(array) - 1):
            for j in range(1, len(array[0]) - 1):
                if (((array[i - 1][j] == n or
                      array[i + 1][j] == n or
                      array[i][j - 1] == n or
                      array[i][j + 1] == n))
                      and (array[i][j] == -1)):
                    array[i][j] = n + 1

    # Fix anything we missed earlier
    for i in range(1, len(array) - 1):
        for j in range(1, len(array[0]) - 1):
            if array[i][j] == -1:
                array[i][j] = maxDistance

    # Randomly blur the values
    for i in range(1, len(array) - 1):
        for j in range(1, len(array[0]) - 1):
            if array[i][j] >= 1:
                array[i][j] = random.randint(array[i][j] - 1, array[i][j] + 1)
                if array[i][j] <= 0:
                    array[i][j] = 1
                if array[i][j] > maxDistance:
                    array[i][j] = maxDistance


# Display on the command line
def display(array1):
    colors = {
        '1':  '\033[48;2;24;0;59m',  # Ground
        '101':  '\033[48;2;24;0;59m',  # Ground
        '26':  '\033[48;2;166;72;233m',  # Dirt
        '30':  '\033[48;2;139;43;199m',  # Loose Rock
        '34':  '\033[48;2;108;10;163m',  # Hard Rock
        '38':  '\033[48;2;59;0;108m',  # Solid Rock
        5:  '\033[48;2;61;38;20m',  # Unused
        '11':  '\033[48;2;6;45;182m',  # Water
        '111':  '\033[48;2;6;45;182m',  # Water
        '6':  '\033[48;2;239;79;16m',  # Lava
        '106':  '\033[48;2;239;79;16m',  # Lava
        '63':  '\033[48;2;24;0;59m',  # Landslide rubble
        '163':  '\033[48;2;24;0;59m',  # Landslide rubble
        '12':  '\033[48;2;150;150;0m',  # Slimy Slug hole
        '112':  '\033[48;2;150;150;0m',  # Slimy Slug hole
        '42': '\033[48;2;185;255;25m',  # Energy Crystal Seam
        '46': '\033[48;2;146;62;20m',  # Ore Seam
        '50': '\033[48;2;250;255;14m',  # Recharge Seam
        '14': '\033[48;2;190;190;190m',  # Building power path
        '114': '\033[48;2;190;190;190m',  # Building power path
    }
    for i in range(len(array1)):
        for j in range(len(array1[0])):
            # Different color for each type
            print(
                colors[array1[i][j]], # Background
                '\033[38;2;0;255;16m',  # Text
                '  ',
                # '\033[38;2;255;255;255m',  # White text
                # ' ',
                end='', sep='')
        print('\033[0m')  # Reset the background and new line


# Display a 2D int array visually with scaled values
def displayArr(array, stats=False):
    # Find the limits
    min = array[0][0]
    max = array[0][0]
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] < min:
                min = array[i][j]
            if array[i][j] > max:
                max = array[i][j]

    difference = max - min

    # Print the array
    for i in range(len(array)):
        for j in range(len(array[0])):
            value = int((array[i][j] - min) / (difference if difference else 1) * 255)
            print('\033[48;2;', 0, ';', value, ';', 0, 'm', '  ', sep='', end='')
        print('\033[0m')  # Reset the background and new line

    # Optionally display the unique values and their differences
    if stats:
        set = []
        differences = []
        for i in range(len(array)):
            for j in range(len(array[0])):
                if array[i][j] not in set:
                    set.append(array[i][j])
        set.sort()
        print(set)
        for i in range(len(set) - 1):
            differences.append(set[i + 1] - set[i])
        print(differences)


# Display on the command line
def displaySingle(array):
    colors = {
        0: '\033[48;2;5;21;16m',
        1: '\033[48;2;178;120;61m',
        2: '\033[48;2;153;102;51m',
        3: '\033[48;2;128;84;43m',
        4: '\033[48;2;102;66;33m',
        5: '\033[48;2;61;38;20m',
        -1: '\033[48;2;255;0;20m',
    }
    for i in range(len(array)):
        for j in range(len(array[0])):
            # Different color for each type
            print(
                colors[array[i][j]], # Background
                '  ',
                end='', sep='')
        print('\033[0m')  # Reset the background and new line


# Fill in all open areas except for the largest one
def fillExtra(array):

    # Create the obstacle map
    # 0:  Unchecked open space
    # 1:  Checked open space
    # -1: Obstacle
    tmap = createArray(len(array), len(array[0]), 0)
    for i in range(0, len(array)):
        for j in range(0, len(array[0])):
            if array[i][j] != 0:
                tmap[i][j] = -1

    # Make a list of open spaces
    spaces = openSpaces(tmap)

    # Make sure the map even makes sense
    if len(spaces) < 1:  # The map failed
        return False


    # Fill in all except the largest
    spaces.sort(key=len, reverse=True)  # Move the largest to the front
    spaces.pop(0)  # Remove the largest
    for space in spaces:
        for coord in space:
            array[coord[0]][coord[1]] = -1

    # Report that the map makes sense
    return True


# Fill in a square section of an array
def fillSquare(i, j, array, length, width, squareSize, value):
    # Loop through each space in the square and stay in bounds
    for k in range(max(i, 0), min(i + squareSize, length)):
        for l in range(max(j, 0), min(j + squareSize, width)):
            array[k][l] += value


# Make a list of undiscovered caverns
def findCaves(array, base):
    # Mark our obstacles
    tmap = createArray(len(array), len(array[0]), -1)

    # Mark the open spaces
    for i in range(1, len(array)):
        for j in range(1, len(array[0])):
            if array[i][j] in [0, 6, 7, 8, 9, 13]:  # Open air spaces
                tmap[i][j] = 0

    # Create the list of caverns
    caveList = openSpaces(tmap)

    # Find which cavern contains our base and remove it
    for i in range(len(caveList)):
        if base in caveList[i]:
            caveList.insert(0, caveList.pop(i))
            break

    return caveList


# Flood low areas with a specified liquid
def flood(array, heightArray, floodLevel, floodType):
    length = len(array)
    width = len(array[0])

    # Find the flood height
    minimum = heightArray[0][0]
    maximum = heightArray[0][0]
    for i in range(length + 1):
        for j in range(width + 1):
            maximum = max(heightArray[i][j], maximum)
            minimum = min(heightArray[i][j], minimum)
    difference = maximum - minimum
    floodHeight = int(difference * floodLevel + minimum)

    # Level anything below floodHeight
    for i in range(length + 1):
        for j in range(width + 1):
            heightArray[i][j] = max(heightArray[i][j], floodHeight)

    # Finally pour the lava! (or water)
    for i in range(length):
        for j in range(width):
            if (array[i][j] == 0 and
                heightArray[i][j] == floodHeight and
                heightArray[i + 1][j] == floodHeight and
                heightArray[i][j + 1] == floodHeight and
                heightArray[i + 1][j + 1] == floodHeight):
                array[i][j] = floodType


# Create a height map
def heightMap(length, width, terrain, smoothness):
    array = createArray(length, width, 0)

    # Make sure the terrain value makes sense
    terrain = max(terrain, 1)

    # Loop through each square
    for i in range(-smoothness, length, 1):
        for j in range(-smoothness, width, 1):
            # Sets of four overlapping squares
            value = random.randint(0, int(terrain))
            fillSquare(i, j, array, length, width, smoothness, value)

    return array


# Check if a string is a bool
def isBool(s):
    if s == "True" or s == "true" or s == "False" or s == "false":
        return True
    return False


# Check if a string is a float
def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Check if a string is an int
def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# Check if a string is true
def isTrue(s):
    if s == "True" or s == "true":
        return True
    return False


# Search for open spaces
def openSpaces(array):
    spaces = []  # List of lists of coordinates
    for i in range(1, len(array) - 1):  # Leave a margin of 1
        for j in range(1, len(array[0]) - 1):
            if array[i][j] == 0:  # Open space found!
                array[i][j] = 1  # Mark the space
                space = []  # List of coordinates in the space
                index = 0
                space.append((i, j))
                while index < len(space):
                    # Use shorter variable names for frequently used values
                    x = space[index][0]
                    y = space[index][1]

                    # Check each adjacent space
                    if array[x - 1][y] == 0:
                        array[x - 1][y] = 1
                        space.append((x - 1, y))
                    if array[x + 1][y] == 0:
                        array[x + 1][y] = 1
                        space.append((x + 1, y))
                    if array[x][y - 1] == 0:
                        array[x][y - 1] = 1
                        space.append((x, y - 1))
                    if array[x][y + 1] == 0:
                        array[x][y + 1] = 1
                        space.append((x, y + 1))

                    # Mark the current space as checked
                    array[x][y] = 1

                    # Move on to the next coordinate
                    index += 1

                # # Add the list to the list of lists
                spaces.append(space)

    return spaces


# Fill an array with random values
def randomize(array, probability):
    for i in range(1, len(array) - 1):
        for j in range(1, len(array[0]) - 1):
            if random.random() < probability:
                array[i][j] = 0


# Save the output to a file
def saveFile(filename, content):
    # Make sure the filename is unique
    counter = 0  # Increment if the file exists
    while os.path.isfile(filename + (str(counter) if counter else '') + '.dat'):
        counter += 1
    filename += (str(counter) if counter else '') + '.dat'

    # Save the file
    f = open(filename, 'w')
    f.write(content)
    f.close()
    print("Saved to:", filename)


# Set up the base at the chosen location
def setBase(base, array, height):
    # Place building power paths under the tool store
    array[base[0]][base[1]] = 13  # Building power path
    array[base[0] + 1][base[1]] = 13  # Building power path

    # Change geography to accomodate our buildings
    average = ((height[base[0]][base[1]] +
                height[base[0] + 1][base[1]] +
                height[base[0]][base[1] + 1] +
                height[base[0] + 1][base[1] + 1])
                // 4)
    average = int(average)
    height[base[0]][base[1]] = average
    height[base[0] + 1][base[1]] = average
    height[base[0]][base[1] + 1] = average
    height[base[0] + 1][base[1] + 1] = average


# Shape the random mess into caves
def smooth(array):
    changed = True
    while changed:  # Run until nothing changes
        changed = False
        # tmap = deepcopy(array)
        tmap = createArray(len(array), len(array[0]), 4)
        for i in range(len(array)):
            for j in range(len(array[0])):
                tmap[i][j] = array[i][j]
        for i in range(1, len(array) - 1):
            for j in range(1, len(array[0]) - 1):
                # Count adjacent spaces
                adjacent = 0
                if tmap[i + 1][j] == -1:
                    adjacent += 1
                if tmap[i - 1][j] == -1:
                    adjacent += 1
                if tmap[i][j + 1] == -1:
                    adjacent += 1
                if tmap[i][j - 1] == -1:
                    adjacent += 1

                # Change the values
                if adjacent == 0:
                    if array[i][j] != 0:
                        changed = True
                        array[i][j] = 0
                elif adjacent >= 3:
                    if array[i][j] != -1:
                        changed = True
                        array[i][j] = -1


main()
