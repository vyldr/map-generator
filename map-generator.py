from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

from MainWindow import Ui_MainWindow
import mapgen


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.newMapButton.clicked.connect(self.generate_map)
        self.saveButton.clicked.connect(self.saveFile)
        self.map_generator = mapgen.Mapgen()
        self.generate_map()

    def generate_map(self):
        self.map_generator.mapgen()
        # print(self.map_generator.MMtext)
        self.displayPNG()

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

    # Display the map as a PNG
    def displayPNG(self):

        # Layers
        wallArray = self.map_generator.layers["wall_array"]
        crystalArray = self.map_generator.layers["crystal_array"]
        oreArray = self.map_generator.layers["ore_array"]

        # Create the image
        scale = self.map_preview.width() // len(wallArray)
        offset = self.map_preview.width() % len(wallArray) // 2
        img = Image.new('RGBA',
                        (self.map_preview.width(),
                         self.map_preview.height()),
                        color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

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

        # Draw the background
        draw.rectangle([offset,
                        offset,
                        self.map_preview.width() - offset,
                        self.map_preview.height() - offset],
                        fill=(0, 0, 0))

        # Draw the tiles
        for i in range(len(wallArray)):
            for j in range(len(wallArray[0])):
                # Draw the tile
                draw.rectangle([j * scale + offset + 1,
                                i * scale + offset + 1,
                                j * scale + offset + (scale - 1),
                                i * scale + offset + (scale - 1)],
                               fill=colors[wallArray[i][j]])

                # Draw the crystal and ore indicators
                if crystalArray[i][j] > 0:
                    draw.rectangle([
                        j * scale + offset + 2,
                        i * scale + offset + 4,
                        j * scale + offset + 4,
                        i * scale + offset + 2],
                        fill=colors["42"])
                if oreArray[i][j] > 0:
                    draw.rectangle([
                        j * scale + offset + 5,
                        i * scale + offset + 4,
                        j * scale + offset + 7,
                        i * scale + offset + 2],
                        fill=colors["46"])

        # Display the image
        image = ImageQt(img)
        pixmap = QtGui.QPixmap.fromImage(image).copy()
        self.map_preview.setPixmap(pixmap)


# Do the thing
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
