import random

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtGui
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

from MainWindow import Ui_MainWindow
import mapgen


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.newMapButton.clicked.connect(self.new_map)
        self.saveButton.clicked.connect(self.saveFile)

        # Start the map generator
        self.map_generator = mapgen.Mapgen()

        # Set up the inputs
        self.map_size_slider.valueChanged.connect(self.update_map_size)
        self.biome_combobox.addItems(['rock', 'ice', 'lava'])
        self.biome_combobox.currentTextChanged.connect(self.update_biome)
        self.solid_rock_slider.valueChanged.connect(self.update_solid_rock)
        self.other_rock_slider.valueChanged.connect(self.update_other_rock)
        self.energy_crystals_slider.valueChanged.connect(self.update_energy_crystals)
        self.ore_slider.valueChanged.connect(self.update_ore)
        self.ecs_slider.valueChanged.connect(self.update_ecs)
        self.os_slider.valueChanged.connect(self.update_os)
        self.rs_slider.valueChanged.connect(self.update_rs)

        # Set the input values
        self.set_input_values()

        self.generate_map()

    def set_input_values(self):
        self.map_size_slider.setValue(self.map_generator.parameters['size'] / 8)
        self.biome_combobox.setCurrentText(self.map_generator.parameters['biome'])
        self.solid_rock_slider.setValue((self.map_generator.parameters['solidDensity'] - 0.2) / 0.004)
        self.other_rock_slider.setValue((self.map_generator.parameters['wallDensity'] - 0.2) / 0.004)
        self.energy_crystals_slider.setValue(self.map_generator.parameters['crystalDensity'] / 0.008)
        self.ore_slider.setValue(self.map_generator.parameters['oreDensity'] / 0.008)
        self.ecs_slider.setValue(self.map_generator.parameters['crystalSeamDensity'] / 0.006)
        self.os_slider.setValue(self.map_generator.parameters['oreSeamDensity'] / 0.006)
        self.rs_slider.setValue(self.map_generator.parameters['rechargeSeamDensity'] / 0.01)

    def generate_map(self):
        self.map_generator.mapgen()
        # print(self.map_generator.MMtext)
        self.displayPNG()

    def new_map(self):
        self.map_generator.init_parameters()
        self.set_input_values()
        self.map_generator.seed = random.random()
        self.generate_map()


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
            0:   (24, 0, 59),  # Ground
            1:  (166, 72, 233),  # Dirt
            2:  (139, 43, 199),  # Loose Rock
            3:  (108, 10, 163),  # Hard Rock
            4:  (59, 0, 108),  # Solid Rock
            6:  (6, 45, 182),  # Water
            7:   (239, 79, 16),  # Lava
            8:  (56, 44, 73),  # Landslide rubble
            9:  (150, 150, 0),  # Slimy Slug hole
            10:  (185, 255, 25),  # Energy Crystal Seam
            11:  (146, 62, 20),  # Ore Seam
            12:  (250, 255, 14),  # Recharge Seam
            13:  (190, 190, 190),  # Building power path
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
                        fill=colors[10])
                if oreArray[i][j] > 0:
                    draw.rectangle([
                        j * scale + offset + 5,
                        i * scale + offset + 4,
                        j * scale + offset + 7,
                        i * scale + offset + 2],
                        fill=colors[11])

        # Display the image
        image = ImageQt(img)
        pixmap = QtGui.QPixmap.fromImage(image).copy()
        self.map_preview.setPixmap(pixmap)

    def update_map_size(self, value):
        value *= 8
        self.map_generator.parameters['size'] = value
        self.generate_map()

    def update_biome(self, value):
        self.map_generator.parameters['biome'] = value

    def update_solid_rock(self, value):
        value = value * 0.004 + 0.2
        self.map_generator.parameters['solidDensity'] = value
        self.generate_map()

    def update_other_rock(self, value):
        value = value * 0.004 + 0.2
        self.map_generator.parameters['wallDensity'] = value
        self.generate_map()

    def update_energy_crystals(self, value):
        value = value * 0.008
        self.map_generator.parameters['crystalDensity'] = value
        self.generate_map()

    def update_ore(self, value):
        value = value * 0.008
        self.map_generator.parameters['oreDensity'] = value
        self.generate_map()

    def update_ecs(self, value):
        value = value * 0.006
        self.map_generator.parameters['crystalSeamDensity'] = value
        self.generate_map()

    def update_os(self, value):
        value = value * 0.006
        self.map_generator.parameters['oreSeamDensity'] = value
        self.generate_map()

    def update_rs(self, value):
        value = value * 0.01
        self.map_generator.parameters['rechargeSeamDensity'] = value
        self.generate_map()

# Do the thing
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
