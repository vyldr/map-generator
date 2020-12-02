import time
import os
import sys
import mapgen


def main():

    map_generator = mapgen.Mapgen()
    parameters = map_generator.parameters

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

    # Start the timer
    start = time.process_time()

    # Keep trying until we get one or give up after 100 times
    success = map_generator.mapgen()
    if success:
        if parameters["save"]:
            saveFile(parameters["name"], map_generator.MMtext, parameters["overwrite"])

    else:
        print("Unable to create a map with those parameters")

   # Stop timing
    finish = time.process_time()

    # Optionally show the stats
    print()
    if parameters["stats"]:
        print('Parameters:')
        for key in parameters:
            print('    ', key, ': ', parameters[key], sep='')

        print('\nResults:')
        print('    Size: ', parameters["length"], 'x', parameters["width"])
        print('    Tiles:', parameters["length"] * parameters["width"])
        print('    Time: ', finish - start, 'seconds')
        if finish - start == 0:
            print('Finished with infinite speed!')
        else:
            print('    Speed:', (parameters["length"] * parameters["width"]) / (finish - start), 'tiles per second')
        print()

    if parameters["stats"]:
        input()


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
                colors[array1[i][j]],  # Background
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
            value = int((array[i][j] - min) /
                        (difference if difference else 1) * 255)
            print('\033[48;2;', 0, ';', value, ';',
                  0, 'm', '  ', sep='', end='')
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


# Display the map as a PNG
def displayPNG(wallArray, crystalArray, oreArray, landslideList, flowList):

    # Get the image library here so it is only required if it will be used
    from PIL import Image, ImageDraw

    # Create the image
    scale = 14
    img = Image.new('RGB', (len(
        wallArray[0]) * scale + 1, len(wallArray) * scale + 1), color=(0, 0, 0))

    # Color conversions
    colors = {
        '1':   (24, 0, 59),  # Ground
        '101': (24, 0, 59),  # Ground
        '26':  (166, 72, 233),  # Dirt
        '30':  (139, 43, 199),  # Loose Rock
        '34':  (108, 10, 163),  # Hard Rock
        '38':  (59, 0, 108),  # Solid Rock
        '11':  (6, 45, 182),  # Water
        '111': (6, 45, 182),  # Water
        '6':   (239, 79, 16),  # Lava
        '106': (239, 79, 16),  # Lava
        '63':  (56, 44, 73),  # Landslide rubble
        '163': (56, 44, 73),  # Landslide rubble
        '12':  (150, 150, 0),  # Slimy Slug hole
        '112': (150, 150, 0),  # Slimy Slug hole
        '42':  (185, 255, 25),  # Energy Crystal Seam
        '46':  (146, 62, 20),  # Ore Seam
        '50':  (250, 255, 14),  # Recharge Seam
        '14':  (190, 190, 190),  # Building power path
        '114': (190, 190, 190),  # Building power path
    }

    # Draw the tiles
    draw = ImageDraw.Draw(img)
    for i in range(len(wallArray)):
        for j in range(len(wallArray[0])):
            # Draw the tile
            draw.rectangle([j * scale + 1, i * scale + 1, j * scale + (scale - 1),
                            i * scale + (scale - 1)], fill=colors[wallArray[i][j]])

            # Draw the crystal and ore indicators
            if crystalArray[i][j] > 0:
                draw.rectangle([
                    j * scale + 2,
                    i * scale + scale - 4,
                    j * scale + 4,
                    i * scale + scale - 2],
                    fill=colors["42"])
            if oreArray[i][j] > 0:
                draw.rectangle([
                    j * scale + 5,
                    i * scale + scale - 4,
                    j * scale + 7,
                    i * scale + scale - 2],
                    fill=colors["46"])

    # Rotate to match starting camera
    img = img.rotate(270)

    # Display the image
    img.show()
    # img.save("output.png")


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


# Save the output to a file
def saveFile(filename, content, overwrite):
    # Remove spaces from the filename
    filename = filename.replace(' ', '')

    # Make sure the filename is unique
    counter = 0  # Increment if the file exists
    if overwrite == False:
        while os.path.isfile(filename + (str(counter) if counter else '') + '.dat'):
            counter += 1
    filename += (str(counter) if counter else '') + '.dat'

    # Save the file
    f = open(filename, 'w')
    f.write(content)
    f.close()
    print("Saved to:", filename)
    print('   ', os.path.join(os.getcwd(), filename))
    print()


# Do the thing
main()
