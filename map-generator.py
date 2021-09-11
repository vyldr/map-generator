import random

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtGui
from PIL import Image, ImageDraw, ImageOps
from PIL.ImageQt import ImageQt

from MainWindow import Ui_MainWindow
import mapgen


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.view_combobox.addItems(
            ['Map view', 'Height view', 'Spoiler mode'])
        self.view_combobox.currentTextChanged.connect(self.updateView)
        self.randomize_button.clicked.connect(self.randomize_input)
        self.generate_button.clicked.connect(self.new_map)
        self.save_button.clicked.connect(self.saveFile)
        self.seed_lineEdit.textEdited.connect(self.setSeed)

        # Start the map generator
        self.map_generator = mapgen.Mapgen()

        # Set up resizing the map preview
        self.map_preview.resizeEvent = self.displayPreview

        # Which preview are we showing?
        self.view = 'Map view'

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
        self.flood_level_slider.valueChanged.connect(self.update_flood_level)
        self.flood_type_combobox.addItems(['water', 'lava'])
        self.flood_type_combobox.currentTextChanged.connect(self.update_flood_type)
        self.erosion_sources_slider.valueChanged.connect(self.update_erosion_sources)
        self.landslide_sources_slider.valueChanged.connect(self.update_landslide_sources)
        self.slugs_slider.valueChanged.connect(self.update_slugs)

        # Set a lock to prevent updates
        self.generator_locked = False

        # Set the input values
        self.set_input_values()

        self.generate_map()

    def set_input_values(self):

        # Lock
        self.generator_locked = True

        # Update each input
        self.map_size_slider.setValue(
            self.map_generator.parameters['size'] // 8)
        self.biome_combobox.setCurrentText(self.map_generator.parameters['biome'])
        self.solid_rock_slider.setValue(
            int((self.map_generator.parameters['solidDensity'] - 0.2) / 0.004))
        self.other_rock_slider.setValue(
            int((self.map_generator.parameters['wallDensity'] - 0.2) / 0.004))
        self.energy_crystals_slider.setValue(
            int(self.map_generator.parameters['crystalDensity'] / 0.008))
        self.ore_slider.setValue(
            int(self.map_generator.parameters['oreDensity'] / 0.008))
        self.ecs_slider.setValue(
            int(self.map_generator.parameters['crystalSeamDensity'] / 0.006))
        self.os_slider.setValue(
            int(self.map_generator.parameters['oreSeamDensity'] / 0.006))
        self.rs_slider.setValue(
            int(self.map_generator.parameters['rechargeSeamDensity'] / 0.003))
        self.flood_level_slider.setValue(
            int(self.map_generator.parameters['floodLevel'] * 100))
        self.flood_type_combobox.setCurrentText(self.map_generator.parameters['floodType'])
        self.erosion_sources_slider.setValue(
            int(self.map_generator.parameters['flowDensity'] * 1000))
        self.landslide_sources_slider.setValue(
            int(self.map_generator.parameters['landslideDensity'] / 0.004))
        self.slugs_slider.setValue(
            int(self.map_generator.parameters['slugDensity'] / 0.001))

        # Unlock
        self.generator_locked = False

    def generate_map(self):
        if not self.generator_locked:
            success = self.map_generator.mapgen()
            self.seed_lineEdit.setText(self.map_generator.seed)
            self.displayPreview()

            # Enable/disable the save button
            if success:
                self.save_button.setEnabled(True)
                self.save_button.setToolTip('')
            else:
                self.save_button.setEnabled(False)
                self.save_button.setToolTip('Can\'t save maps with no tool store')

    def randomize_input(self):
        size = self.map_generator.parameters['size']
        self.map_generator.init_parameters()
        self.map_generator.parameters['size'] = size
        self.set_input_values()
        self.new_map()

    def new_map(self):
        self.map_generator.seed = str(random.randint(0, 2 ** 64))
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
            output_file.write(self.map_generator.mm_text())
            output_file.close()

    # Set the random seed

    def setSeed(self, value):
        self.map_generator.seed = value
        self.generate_map()


    def updateView(self, value):
        self.view = value
        self.displayPreview()

    # Display a preview in the preview window

    def displayPreview(self, e=None):
        if self.view == 'Map view':
            self.displayPreviewMap()

        if self.view == 'Height view':
            self.displayPreviewHeight()

        if self.view == 'Spoiler mode':
            self.displayNoPreview()

    # Display a black screen
    def displayNoPreview(self):

        # Create the image
        img = Image.new('RGBA', (1, 1), color=(0, 0, 0, 0))

        # Display the image
        image = ImageQt(img)
        pixmap = QtGui.QPixmap.fromImage(image).copy()
        self.map_preview.setPixmap(pixmap)


    # Display a preview of the heightmap

    def displayPreviewHeight(self):
        width = self.map_preview.width()
        height = self.map_preview.height()
        square_size = min(width, height)

        # Layers
        heightArray = self.map_generator.data["height_array"]

        # Find the range of heights
        lowest = heightArray[0][0]
        highest = heightArray[0][0]

        for i in range(len(heightArray) * len(heightArray[0])):
            lowest = min(
                lowest, heightArray[i // len(heightArray)][i % len(heightArray[0])])
            highest = max(
                highest, heightArray[i // len(heightArray)][i % len(heightArray[0])])

        highest = max(highest, abs(lowest))
        lowest = -highest

        heightRange = highest - lowest

        # Create the image
        scale = square_size // len(heightArray)
        offset = square_size % len(heightArray) // 2
        img = Image.new('RGBA',
                        (square_size,
                         square_size),
                        color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw the background
        draw.rectangle([offset,
                        offset,
                        square_size - offset,
                        square_size - offset],
                       fill=(0, 0, 0))

        # Draw the tiles
        for i in range(len(heightArray)):
            for j in range(len(heightArray[0])):
                # Draw the tile
                draw.rectangle([j * scale + offset + 1,
                                i * scale + offset + 1,
                                j * scale + offset + (scale - 1),
                                i * scale + offset + (scale - 1)],
                               # low = blue, high = red
                               fill='hsl(' + str(250-(heightArray[i][j] - lowest) / heightRange * 250) + ', 100%, 50%)')
                #    fill=(0, int((heightArray[i][j] - lowest) / heightRange * 256), 0))

        # Center the image
        border_x = (width - square_size) // 2
        border_y = (height - square_size) // 2
        img = ImageOps.expand(img, border=(
            border_x, border_y, border_x, border_y), fill=(0, 0, 0, 0))

        # Display the image
        image = ImageQt(img)
        pixmap = QtGui.QPixmap.fromImage(image).copy()
        self.map_preview.setPixmap(pixmap)

    # Display a preview of the wall/floor tiles and resources
    def displayPreviewMap(self):

        width = self.map_preview.width()
        height = self.map_preview.height()
        square_size = min(width, height)

        # Layers
        wallArray = self.map_generator.data["wall_array"]
        crystalArray = self.map_generator.data["crystal_array"]
        oreArray = self.map_generator.data["ore_array"]

        # Create the image
        scale = square_size // len(wallArray)
        offset = square_size % len(wallArray) // 2
        img = Image.new('RGBA',
                        (square_size,
                         square_size),
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
                        square_size - offset,
                        square_size - offset],
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

        # Center the image
        border_x = (width - square_size) // 2
        border_y = (height - square_size) // 2
        img = ImageOps.expand(img, border=(
            border_x, border_y, border_x, border_y), fill=(0, 0, 0, 0))

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
        value = value * 0.003
        self.map_generator.parameters['rechargeSeamDensity'] = value
        self.generate_map()

    def update_flood_level(self, value):
        value = value / 100
        self.map_generator.parameters['floodLevel'] = value
        self.generate_map()

    def update_flood_type(self, value):
        self.map_generator.parameters['floodType'] = value
        self.generate_map()

    def update_erosion_sources(self, value):
        value = value / 1000
        self.map_generator.parameters['flowDensity'] = value
        self.generate_map()

    def update_landslide_sources(self, value):
        value = value * 0.004
        self.map_generator.parameters['landslideDensity'] = value
        self.generate_map()

    def update_slugs(self, value):
        value = value * 0.001
        self.map_generator.parameters['slugDensity'] = value
        self.generate_map()


# Do the thing
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
