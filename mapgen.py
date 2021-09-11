import random


class Mapgen:

    def init_parameters(self):
        self.parameters = {
            "length":               32,                             # How long to make the map
            "width":                32,                             # How wide to make the map
            "size":                 32,                          # Overrides length and width
            "solidDensity":         random.random() * 0.3 + 0.2,    # How much solid rock to generate
            "wallDensity":          random.random() * 0.3 + 0.3,    # How much other rock to generate
            "oreDensity":           random.random() * 0.3 + 0.3,    # How common ore is
            "crystalDensity":       random.random() * 0.3 + 0.2,    # How common energy crystals are
            "oreSeamDensity":       random.random() * 0.25,         # How common ore seams are
            "crystalSeamDensity":   random.random() * 0.5,          # How common energy crystal seams are
            "rechargeSeamDensity":  random.random() * 0.08 + 0.01,  # How common recharge seams are
            "floodLevel":           random.random() * 0.75,         # The height to be flooded with water or lava
            "floodType":            ["water", "lava"][random.randint(0, 1)],  # Whether to flood with water or lava
            "flowDensity":          random.random() * 0.005,        # How common erosion sources are
            "flowInterval":         random.randint(20, 180),        # How slow erosion spreads
            "preFlow":              random.randint(3, 8),           # How much erosion should spread before the level starts
            "landslideDensity":     random.random() * 0.4,          # How common landslide sources are
            "landslideInterval":    random.randint(10, 90),         # How long between landslides
            "slugDensity":          random.random() * 0.01,         # How common slimy slug holes are
            "terrain":              random.randint(0, 25),          # How much the height of the terrain varies
            "biome":                ["ice", "rock", "lava"][random.randint(0, 2)],  # Which biome to use
            "smoothness":           16,          # How smoothly the terrain slopes
            "oxygen":               0 - 1,       # How much oxygen to start with
            "stats":                False,        # Whether to show the statistics
            "save":                 False,        # Whether to save the file
            "name":                 'Untitled',  # What to name the file
            "overwrite":            False,       # Whether to overwrite an existing level
            "show":                 False,       # Whether to show the map, does not work on Windows
        }

    def __init__(self):
        self.seed = str(random.randint(0, 2 ** 64))
        self.init_parameters()
        self.data = {}

    def mapgen(self):

        # Load the seed
        random.seed(self.seed)
        seeds = {
            "solid_seed": random.random(),
            "other_seed": random.random(),
            "ore_seed": random.random(),
            "crystal_seed": random.random(),
            "height_seed": random.random(),
            "slug_seed": random.random(),
            "ecs_seed": random.random(),
            "os_seed": random.random(),
            "rs_seed": random.random(),
            "erosion_seed": random.random(),
            "landslide_seed": random.random(),
            "base_seed": random.random(),
        }

        # Set length and width
        if self.parameters["size"]:
            # Round up to the next chunk
            self.parameters["size"] = (self.parameters["size"] + 7) // 8 * 8
            self.parameters["length"] = self.parameters["size"]
            self.parameters["width"] = self.parameters["size"]

        # Optionally set oxygen
        if self.parameters["oxygen"] == -1:
            self.parameters["oxygen"] = self.parameters["length"] * self.parameters["width"] * 3

        # Create feature maps
        self.data["solid_array"] = self.createArray(
            self.parameters["length"], self.parameters["width"], -1)  # Solid rock
        self.data["wall_array"] = self.createArray(
            self.parameters["length"], self.parameters["width"], -1)  # Other rock

        # Create the solid rock
        random.seed(seeds["solid_seed"])
        self.randomize(self.data["solid_array"], 1 - self.parameters["solidDensity"])
        self.speleogenesis(self.data["solid_array"])
        self.cleanup(self.data["solid_array"])
        self.fillExtra(self.data["solid_array"])

        # Create the other rocks
        random.seed(seeds["other_seed"])
        self.randomize(self.data["wall_array"], 1 - self.parameters["wallDensity"])
        self.speleogenesis(self.data["wall_array"])
        self.cleanup(self.data["wall_array"])
        self.details(self.data["wall_array"], 3)

        # Merge the permnent and temporary features
        for i in range(self.parameters["length"]):
            for j in range(self.parameters["width"]):
                if self.data["solid_array"][i][j] == -1:
                    self.data["wall_array"][i][j] = 4

        # Create ore
        random.seed(seeds["ore_seed"])
        self.data["ore_array"] = self.createArray(self.parameters["length"], self.parameters["width"], -1)
        self.randomize(self.data["ore_array"], 1 - self.parameters["oreDensity"])
        self.speleogenesis(self.data["ore_array"])
        self.cleanup(self.data["ore_array"])
        self.details(self.data["ore_array"], 4)

        # Create crystals
        random.seed(seeds["crystal_seed"])
        self.data["crystal_array"] = self.createArray(self.parameters["length"], self.parameters["width"], -1)
        self.randomize(self.data["crystal_array"], 1 - self.parameters["crystalDensity"])
        self.speleogenesis(self.data["crystal_array"])
        self.cleanup(self.data["crystal_array"])
        self.details(self.data["crystal_array"], 5)

        # Creat a height map
        random.seed(seeds["height_seed"])
        self.data["height_array"] = self.heightMap(
            self.parameters["length"] + 1, self.parameters["width"] + 1, random.randint(0, 25), self.parameters["smoothness"])

        # Flood the low areas
        self.flood(self.data["wall_array"], self.data["height_array"],
                   self.parameters["floodLevel"], self.parameters["floodType"])

        # Organize the maps
        for i in range(self.parameters["length"]):
            for j in range(self.parameters["width"]):
                if self.data["wall_array"][i][j] not in range(1, 4):
                    self.data["crystal_array"][i][j] = 0
                    self.data["ore_array"][i][j] = 0

        # Slimy Slug holes
        random.seed(seeds["slug_seed"])
        self.aSlimySlugIsInvadingYourBase(self.data["wall_array"], self.parameters["slugDensity"])

        # Energy Crystal Seams
        random.seed(seeds["ecs_seed"])
        self.addSeams(self.data["wall_array"], self.data["crystal_array"],
                      self.parameters["crystalSeamDensity"], 10)

        # Ore Seams
        random.seed(seeds["os_seed"])
        self.addSeams(self.data["wall_array"], self.data["ore_array"], self.parameters["oreSeamDensity"], 11)

        # Recharge seams
        random.seed(seeds["rs_seed"])
        self.addRechargeSeams(self.data["wall_array"], self.parameters["rechargeSeamDensity"])

        # Lava Flows / Erosion
        random.seed(seeds["erosion_seed"])
        self.data["flow_list"] = []
        if self.parameters["floodType"] == "lava":  # Lava
            self.data["flow_list"] = self.createFlowList(
                self.data["wall_array"],
                self.parameters["flowDensity"],
                self.data["height_array"],
                self.parameters["preFlow"],
                self.parameters["terrain"])

        # Set unstable walls and landslide rubble
        random.seed(seeds["landslide_seed"])
        self.data["landslide_list"] = self.aLandslideHasOccured(
            self.data["wall_array"], self.parameters["landslideDensity"])

        # Set the starting point
        random.seed(seeds["base_seed"])
        self.data["base"] = self.chooseBase(self.data["wall_array"])
        if not self.data["base"]:  # Make sure there is space to build
            return False
        self.setBase(self.data["base"], self.data["wall_array"], self.data["height_array"])

        # Finally done
        return True

    # Add Energy Crystal and Ore seams

    def addSeams(self, array, resourceArray, density, seam_type):
        for i in range(len(array)):
            for j in range(len(array[0])):
                if random.random() < density:
                    if resourceArray[i][j] > 2:
                        array[i][j] = seam_type

    # Add recharge seams in to replace solid rock

    def addRechargeSeams(self, array, density):
        for i in range(1, len(array) - 1):
            for j in range(1, len(array[0]) - 1):

                # Unconditional random for more consistency
                rand = random.random() < density

                # Only if the space is already solid rock
                if array[i][j] == 4:  # Solid rock
                    # Only if at least two opposite sides are solid rock
                    if ((((array[i + 1][j] == 4) and
                          (array[i - 1][j] == 4)) or
                         ((array[i][j + 1] == 4) and
                          (array[i][j - 1] == 4))) and
                        # Only if at least one side is not solid rock
                            ((array[i + 1][j] != 4) or
                             (array[i - 1][j] != 4) or
                             (array[i][j + 1] != 4) or
                             (array[i][j - 1] != 4))):
                        if rand:
                            array[i][j] = 12  # Recharge seam

    # A landslide has occured

    def aLandslideHasOccured(self, array, stability):
        landslideArray = self.createArray(len(array), len(array[0]), -1)
        self.randomize(landslideArray, 1 - stability)
        self.speleogenesis(landslideArray)
        self.details(landslideArray, 3)

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

    # A Slimy Slug is invading your base!

    def aSlimySlugIsInvadingYourBase(self, array, slugDensity):
        for i in range(len(array)):
            for j in range(len(array[0])):
                # Randomly set Slimy Slug holes
                if random.random() < slugDensity:
                    if array[i][j] == 0:  # Ground
                        array[i][j] = 9  # Slimy Slug hole

    # Choose a starting point

    def chooseBase(self, array):
        # Find all possible starting points
        possibleBaseList = []
        for i in range(1, len(array) - 2):
            for j in range(1, len(array[0]) - 2):
                # Choose a random value as the location preference
                preference = random.random()
                # Check for a 2x2 ground section to build on
                if ((array[i][j] == 0) and
                    (array[i + 1][j] == 0) and
                    (array[i][j + 1] == 0) and
                        (array[i + 1][j + 1] == 0)):
                    possibleBaseList.append((i, j, preference))

        # Make sure there is somewhere to build
        if len(possibleBaseList) == 0:
            return False

        # Sort by preference
        possibleBaseList.sort(key=lambda x: x[2])

        # Choose one  TODO: Maybe add multiple bases or larger bases
        return (possibleBaseList[0][0], possibleBaseList[0][1])

    # Clean up small map features

    def cleanup(self, array):
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

    def mm_text(self):

        # Count all the crystals we can reach
        crystalCount = self.countAccessibleCrystals(
            self.data["wall_array"], self.data["base"], self.data["ore_array"], False)
        if crystalCount >= 14:  # More than enough crystals to get vehicles
            crystalCount = self.countAccessibleCrystals(
                self.data["wall_array"], self.data["base"], self.data["ore_array"], True)

        # Basic info
        MMtext = (
            'info{\n' +
            'rowcount:' + str(len(self.data["wall_array"])) + '\n' +
            'colcount:' + str(len(self.data["wall_array"][0])) + '\n' +
            'camerapos:Translation: X=' + str(self.data["base"][1] * 300 + 300) +
            ' Y=' + str(self.data["base"][0] * 300 + 300) +
            ' Z=' + str(self.data["height_array"][self.data["base"][0]][self.data["base"][1]]) +
            ' Rotation: P=44.999992 Y=180.000000 R=0.000000 Scale X=1.000 Y=1.000 Z=1.000\n' +
            'biome:' + self.parameters["biome"] + '\n' +
            'creator:Map Generator for Manic Miners\n' +
            (('oxygen:' + str(self.parameters["oxygen"]) + '/' + str(self.parameters["oxygen"]) + '\n') if self.parameters["oxygen"] else '') +
            'levelname:' + self.parameters["name"] + '\n' +
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
        converted_walls = self.createArray(len(self.data["wall_array"]), len(self.data["wall_array"][0]), None)
        for i in range(len(self.data["wall_array"])):
            for j in range(len(self.data["wall_array"][0])):
                converted_walls[i][j] = conversion[self.data["wall_array"][i][j]]

        # List undiscovered caverns
        caveList = self.findCaves(self.data["wall_array"], self.data["base"])

        # Hide undiscovered caverns
        for cave in caveList:
            for space in cave:
                converted_walls[space[0]][space[1]] = str(
                    int(converted_walls[space[0]][space[1]]) + 100)

        # Add to the file
        for i in range(len(converted_walls)):
            for j in range(len(converted_walls[0])):
                MMtext += converted_walls[i][j] + ','
            MMtext += '\n'
        MMtext += '}\n'

        # Add the heights
        MMtext += 'height{\n'
        for i in range(len(self.data["height_array"])):
            for j in range(len(self.data["height_array"][0])):
                MMtext += str(self.data["height_array"][i][j]) + ','
            MMtext += '\n'
        MMtext += '}\n'

        # Add the resources
        MMtext += 'resources{\n'

        # Crystals
        MMtext += 'crystals:\n'
        for i in range(len(converted_walls)):
            for j in range(len(converted_walls[0])):
                MMtext += str(self.data["ore_array"][i][j]) + ','
            MMtext += '\n'

        # Ore
        MMtext += 'ore:\n'
        for i in range(len(converted_walls)):
            for j in range(len(converted_walls[0])):
                MMtext += str(self.data["ore_array"][i][j]) + ','
            MMtext += '\n'
        MMtext += '}\n'

        # Objectives
        MMtext += 'objectives{\n'
        # Collect half of the crystals, maximum of 999
        MMtext += 'resources: ' + str(min((crystalCount // 2), 999)) + ',0,0\n'
        MMtext += '}\n'

        # Buildings
        MMtext += 'buildings{\n'
        MMtext += (
            'BuildingToolStore_C\n' +
            'Translation: X=' + str(self.data["base"][1] * 300 + 150.000) +
            ' Y=' + str(self.data["base"][0] * 300 + 150.000) +
            ' Z=' + str(self.data["height_array"][self.data["base"][0]][self.data["base"][1]] + (50 if 'udts' in self.parameters else 0)) +
            ' Rotation: P=' + ('180' if 'udts' in self.parameters else '0') + '.000000 Y=89.999992 R=0.000000 Scale X=1.000 Y=1.000 Z=1.000\n' +
            'Level=1\n' +
            'Teleport=True\n' +
            'Health=MAX\n' +
            # X = chunk number
            # Y = row within chunk
            # Z = col within chunk
            'Powerpaths=X=' + str((len(converted_walls[0]) // 8) * (self.data["base"][0] // 8) + (self.data["base"][1] // 8)) +
            ' Y=' + str(self.data["base"][0] % 8) +
            ' Z=' + str(self.data["base"][1] % 8) +
            '/X=' + str((len(converted_walls[0]) // 8) * ((self.data["base"][0] + 1) // 8) + (self.data["base"][1] // 8)) +
            ' Y=' + str((self.data["base"][0] + 1) % 8) +
            ' Z=' + str(self.data["base"][1] % 8) + '/\n'
        )
        MMtext += '}\n'

        # A landslide has occured
        MMtext += 'landslideFrequency{\n'
        for i in range(1, len(self.data["landslide_list"]) + 1):
            if len(self.data["landslide_list"][i - 1]):
                MMtext += str(i * self.parameters["landslideInterval"]) + ':'
            for space in self.data["landslide_list"][i - 1]:
                MMtext += str(space[1]) + ',' + str(space[0]) + '/'
            if len(self.data["landslide_list"][i - 1]):
                MMtext += '\n'
        MMtext += '}\n'

        # Erosion
        MMtext += 'lavaspread{\n'
        for i in range(1, len(self.data["flow_list"]) + 1):
            if len(self.data["flow_list"][i - 1]):
                MMtext += str(i * self.parameters["flowInterval"]) + ':'
            for space in self.data["flow_list"][i - 1]:
                MMtext += str(space[1]) + ',' + str(space[0]) + '/'
            if len(self.data["flow_list"][i - 1]):
                MMtext += '\n'
        MMtext += '}\n'

        # Miners
        MMtext += 'miners{\n'
        MMtext += '}\n'

        # Briefing
        MMtext += 'briefing{\n'
        MMtext += 'You must collect ' + \
            str(min((crystalCount // 2), 999)) + ' energy crystals.  \n'
        MMtext += '}\n'

        return MMtext

    # Count how many crystals we can actually get

    def countAccessibleCrystals(self, array, base, crystalArray, vehicles):
        spaces = [base]
        tmap = self.createArray(len(array), len(array[0]), -1)

        # Choose the types of tiles we can cross
        types = [0, 1, 2, 3, 8, 9, 10, 11, 13]
        if vehicles:  # With vehicles we can cross water and lava
            types = [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 13]

        # Mark which spaces could be accessible
        for i in range(1, len(array) - 1):  # Leave a margin of 1
            for j in range(1, len(array[0]) - 1):
                if array[i][j] in types:
                    tmap[i][j] = 0  # Accessible

        tmap[base[0]][base[1]] = 1
        i = 0
        while i < len(spaces):
            # Use shorter variable names for frequently used values
            x = spaces[i][0]
            y = spaces[i][1]

            # Check each adjacent space
            if tmap[x - 1][y] == 0:
                tmap[x - 1][y] = 1
                spaces.append((x - 1, y))
            if tmap[x + 1][y] == 0:
                tmap[x + 1][y] = 1
                spaces.append((x + 1, y))
            if tmap[x][y - 1] == 0:
                tmap[x][y - 1] = 1
                spaces.append((x, y - 1))
            if tmap[x][y + 1] == 0:
                tmap[x][y + 1] = 1
                spaces.append((x, y + 1))

            i += 1

        # Count crystals in our list
        count = 0
        for space in spaces:
            count += crystalArray[space[0]][space[1]]

        return count

    # Create an array and fill it with something

    def createArray(self, x, y, fill):
        array = [None] * x
        for i in range(x):
            array[i] = [None] * y
            for j in range(y):
                array[i][j] = fill

        return array

    # Create a list of lava flow spaces

    def createFlowList(self, array, density, height, preFlow, terrain):
        flowArray = self.createArray(len(array), len(array[0]), -1)
        spillList = []
        sources = []

        # Find places where lava flows are possible
        for i in range(len(array)):
            for j in range(len(array[0])):
                if random.random() < density:
                    if array[i][j] == 0:
                        sources.append((i, j))  # Possible lava source
                if array[i][j] in range(4):
                    flowArray[i][j] = 0  # Possible spill zone

        # Start spilling from each source
        for source in sources:
            array[source[0]][source[1]] = 7  # Lava
            flowList = [source]
            flowArray[source[0]][source[1]] = 1  # Checked

            # Find spill zones
            i = 0
            while i < len(flowList):
                adjacent = [
                    (flowList[i][0] + 1, flowList[i][1]),
                    (flowList[i][0] - 1, flowList[i][1]),
                    (flowList[i][0], flowList[i][1] + 1),
                    (flowList[i][0], flowList[i][1] - 1),
                ]

                # Sum of all corners.  Not really elevation but close enough
                sourceElevation = (
                    (height[flowList[i][0]][flowList[i][1]]) +
                    (height[flowList[i][0] + 1][flowList[i][1]]) +
                    (height[flowList[i][0]][flowList[i][1] + 1]) +
                    (height[flowList[i][0] + 1][flowList[i][1] + 1])
                )

                # Add to flowList if not checked and lower elevation
                for space in adjacent:
                    # Sum of all corners.  Not really elevation but close enough
                    elevation = (
                        (height[space[0]][space[1]]) +
                        (height[space[0] + 1][space[1]]) +
                        (height[space[0]][space[1] + 1]) +
                        (height[space[0] + 1][space[1] + 1])
                    )
                    if flowArray[space[0]][space[1]] == 0 and sourceElevation > elevation - (terrain * 3):
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

        return spillList

    # Set the details based on the distance from open areas

    def details(self, array, maxDistance):
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
                    array[i][j] = random.randint(
                        array[i][j] - 1, array[i][j] + 1)
                    if array[i][j] <= 0:
                        array[i][j] = 1
                    if array[i][j] > maxDistance:
                        array[i][j] = maxDistance

    # Fill in all open areas except for the largest one

    def fillExtra(self, array):

        # Create the obstacle map
        # 0:  Unchecked open space
        # 1:  Checked open space
        # -1: Obstacle
        tmap = self.createArray(len(array), len(array[0]), 0)
        for i in range(0, len(array)):
            for j in range(0, len(array[0])):
                if array[i][j] != 0:
                    tmap[i][j] = -1

        # Make a list of open spaces
        spaces = self.openSpaces(tmap, False)

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

    def fillSquare(self, i, j, array, length, width, squareSize, value):
        # Loop through each space in the square and stay in bounds
        for k in range(max(i, 0), min(i + squareSize, length)):
            for l in range(max(j, 0), min(j + squareSize, width)):
                array[k][l] += value

    # Make a list of undiscovered caverns

    def findCaves(self, array, base):
        # Mark our obstacles
        tmap = self.createArray(len(array), len(array[0]), -1)

        # Mark the open spaces
        for i in range(1, len(array)):
            for j in range(1, len(array[0])):
                if array[i][j] in [0, 6, 7, 8, 9, 13]:  # Open air spaces
                    tmap[i][j] = 0

        # Create the list of caverns
        caveList = self.openSpaces(tmap, True)

        # Find which cavern contains our base and remove it
        for i in range(len(caveList)):
            if base in caveList[i]:
                caveList.pop(i)
                break

        return caveList

    # Flood low areas with a specified liquid

    def flood(self, array, heightArray, floodLevel, floodType):
        length = len(array)
        width = len(array[0])

        if floodType == "water":
            floodType = 6
        else:
            floodType = 7

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

    def heightMap(self, length, width, terrain, smoothness):
        array = self.createArray(length, width, 0)

        # Make sure the terrain value makes sense
        terrain = max(terrain, 1)

        # Loop through each square
        for i in range(-smoothness, length, 1):
            for j in range(-smoothness, width, 1):
                # Sets of four overlapping squares
                value = random.randint(-int(terrain), int(terrain))
                self.fillSquare(i, j, array, length, width, smoothness, value)

        return array

    # Search for open spaces

    def openSpaces(self, array, corners):
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

                        # Optionally also check the corners
                        if corners:
                            if array[x - 1][y - 1] == 0:
                                array[x - 1][y - 1] = 1
                                space.append((x - 1, y - 1))
                            if array[x + 1][y - 1] == 0:
                                array[x + 1][y - 1] = 1
                                space.append((x + 1, y - 1))
                            if array[x - 1][y + 1] == 0:
                                array[x - 1][y + 1] = 1
                                space.append((x - 1, y + 1))
                            if array[x + 1][y + 1] == 0:
                                array[x + 1][y + 1] = 1
                                space.append((x + 1, y + 1))

                        # Mark the current space as checked
                        array[x][y] = 1

                        # Move on to the next coordinate
                        index += 1

                    # # Add the list to the list of lists
                    spaces.append(space)

        return spaces

    # Fill an array with random values

    def randomize(self, array, probability):
        for i in range(1, len(array) - 1):
            for j in range(1, len(array[0]) - 1):
                if random.random() < probability:
                    array[i][j] = 0

    # Set up the base at the chosen location

    def setBase(self, base, array, height):
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

    def speleogenesis(self, array):
        changed = True
        while changed:  # Run until nothing changes
            changed = False
            tmap = self.createArray(len(array), len(array[0]), 4)

            # Copy the array
            for i in range(len(array)):
                for j in range(len(array[0])):
                    tmap[i][j] = array[i][j]

            # Decide which spaces to change
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

                    # Change to empty if all neighbors are empty
                    if adjacent == 0:
                        if array[i][j] != 0:
                            changed = True
                            array[i][j] = 0

                    # Change to filled if at least three neighbors are filled
                    elif adjacent >= 3:
                        if array[i][j] != -1:
                            changed = True
                            array[i][j] = -1
