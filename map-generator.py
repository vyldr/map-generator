from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog

from MainWindow import Ui_MainWindow
import mapgen


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


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.newMapButton.clicked.connect(self.generate_map)
        self.saveButton.clicked.connect(self.saveFile)
        self.map_generator = mapgen.Mapgen()

    def generate_map(self):
        self.map_generator.mapgen()
        print(self.map_generator.MMtext)

    # Save the output to a file
    def saveFile(self):

        # Set up the save dialog
        save_dialog = QFileDialog()
        save_dialog.setAcceptMode(QFileDialog.AcceptSave)
        save_dialog.setWindowTitle('Save Map')
        save_dialog.setNameFilter('Manic Miners level files (*.dat)')
        save_dialog.setDefaultSuffix('dat')
        if save_dialog.exec():

            # Save the file
            filename = save_dialog.selectedFiles()[0]
            output_file = open(filename, 'w')
            output_file.write(self.map_generator.MMtext)
            output_file.close()
            print("Saved to:", filename)
            print()


# Do the thing
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
