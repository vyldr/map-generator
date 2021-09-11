# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 558)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(300, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(300, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 300, 689))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(300, 0))
        self.scrollAreaWidgetContents.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.seed_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.seed_label.setObjectName("seed_label")
        self.verticalLayout_2.addWidget(self.seed_label)
        self.seed_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.seed_lineEdit.setObjectName("seed_lineEdit")
        self.verticalLayout_2.addWidget(self.seed_lineEdit)
        self.map_size_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.map_size_label.setObjectName("map_size_label")
        self.verticalLayout_2.addWidget(self.map_size_label)
        self.map_size_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.map_size_slider.setMinimum(1)
        self.map_size_slider.setMaximum(16)
        self.map_size_slider.setSingleStep(1)
        self.map_size_slider.setPageStep(1)
        self.map_size_slider.setProperty("value", 4)
        self.map_size_slider.setOrientation(QtCore.Qt.Horizontal)
        self.map_size_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.map_size_slider.setTickInterval(1)
        self.map_size_slider.setObjectName("map_size_slider")
        self.verticalLayout_2.addWidget(self.map_size_slider)
        self.biome_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.biome_label.setObjectName("biome_label")
        self.verticalLayout_2.addWidget(self.biome_label)
        self.biome_combobox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.biome_combobox.setObjectName("biome_combobox")
        self.verticalLayout_2.addWidget(self.biome_combobox)
        self.solid_rock_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.solid_rock_label.setObjectName("solid_rock_label")
        self.verticalLayout_2.addWidget(self.solid_rock_label)
        self.solid_rock_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.solid_rock_slider.setOrientation(QtCore.Qt.Horizontal)
        self.solid_rock_slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.solid_rock_slider.setObjectName("solid_rock_slider")
        self.verticalLayout_2.addWidget(self.solid_rock_slider)
        self.other_rock_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.other_rock_label.setObjectName("other_rock_label")
        self.verticalLayout_2.addWidget(self.other_rock_label)
        self.other_rock_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.other_rock_slider.setOrientation(QtCore.Qt.Horizontal)
        self.other_rock_slider.setObjectName("other_rock_slider")
        self.verticalLayout_2.addWidget(self.other_rock_slider)
        self.energy_crystals_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.energy_crystals_label.setObjectName("energy_crystals_label")
        self.verticalLayout_2.addWidget(self.energy_crystals_label)
        self.energy_crystals_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.energy_crystals_slider.setOrientation(QtCore.Qt.Horizontal)
        self.energy_crystals_slider.setObjectName("energy_crystals_slider")
        self.verticalLayout_2.addWidget(self.energy_crystals_slider)
        self.ore_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ore_label.setObjectName("ore_label")
        self.verticalLayout_2.addWidget(self.ore_label)
        self.ore_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.ore_slider.setOrientation(QtCore.Qt.Horizontal)
        self.ore_slider.setObjectName("ore_slider")
        self.verticalLayout_2.addWidget(self.ore_slider)
        self.ecs_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ecs_label.setObjectName("ecs_label")
        self.verticalLayout_2.addWidget(self.ecs_label)
        self.ecs_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.ecs_slider.setOrientation(QtCore.Qt.Horizontal)
        self.ecs_slider.setObjectName("ecs_slider")
        self.verticalLayout_2.addWidget(self.ecs_slider)
        self.os_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.os_label.setObjectName("os_label")
        self.verticalLayout_2.addWidget(self.os_label)
        self.os_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.os_slider.setOrientation(QtCore.Qt.Horizontal)
        self.os_slider.setObjectName("os_slider")
        self.verticalLayout_2.addWidget(self.os_slider)
        self.rs_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.rs_label.setObjectName("rs_label")
        self.verticalLayout_2.addWidget(self.rs_label)
        self.rs_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.rs_slider.setOrientation(QtCore.Qt.Horizontal)
        self.rs_slider.setObjectName("rs_slider")
        self.verticalLayout_2.addWidget(self.rs_slider)
        self.flood_level_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.flood_level_label.setObjectName("flood_level_label")
        self.verticalLayout_2.addWidget(self.flood_level_label)
        self.flood_level_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.flood_level_slider.setOrientation(QtCore.Qt.Horizontal)
        self.flood_level_slider.setObjectName("flood_level_slider")
        self.verticalLayout_2.addWidget(self.flood_level_slider)
        self.flood_type_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.flood_type_label.setObjectName("flood_type_label")
        self.verticalLayout_2.addWidget(self.flood_type_label)
        self.flood_type_combobox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.flood_type_combobox.setObjectName("flood_type_combobox")
        self.verticalLayout_2.addWidget(self.flood_type_combobox)
        self.erosion_sources_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.erosion_sources_label.setObjectName("erosion_sources_label")
        self.verticalLayout_2.addWidget(self.erosion_sources_label)
        self.erosion_sources_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.erosion_sources_slider.setOrientation(QtCore.Qt.Horizontal)
        self.erosion_sources_slider.setObjectName("erosion_sources_slider")
        self.verticalLayout_2.addWidget(self.erosion_sources_slider)
        self.landslide_sources_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.landslide_sources_label.setObjectName("landslide_sources_label")
        self.verticalLayout_2.addWidget(self.landslide_sources_label)
        self.landslide_sources_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.landslide_sources_slider.setOrientation(QtCore.Qt.Horizontal)
        self.landslide_sources_slider.setObjectName("landslide_sources_slider")
        self.verticalLayout_2.addWidget(self.landslide_sources_slider)
        self.slugs_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.slugs_label.setObjectName("slugs_label")
        self.verticalLayout_2.addWidget(self.slugs_label)
        self.slugs_slider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.slugs_slider.setOrientation(QtCore.Qt.Horizontal)
        self.slugs_slider.setObjectName("slugs_slider")
        self.verticalLayout_2.addWidget(self.slugs_slider)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.view_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.view_combobox.setObjectName("view_combobox")
        self.horizontalLayout_2.addWidget(self.view_combobox)
        self.randomize_button = QtWidgets.QPushButton(self.centralwidget)
        self.randomize_button.setObjectName("randomize_button")
        self.horizontalLayout_2.addWidget(self.randomize_button)
        self.generate_button = QtWidgets.QPushButton(self.centralwidget)
        self.generate_button.setObjectName("generate_button")
        self.horizontalLayout_2.addWidget(self.generate_button)
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_2.addWidget(self.save_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.map_preview = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.map_preview.sizePolicy().hasHeightForWidth())
        self.map_preview.setSizePolicy(sizePolicy)
        self.map_preview.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.map_preview.setText("")
        self.map_preview.setScaledContents(True)
        self.map_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.map_preview.setObjectName("map_preview")
        self.horizontalLayout_3.addWidget(self.map_preview)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Map Generator"))
        self.seed_label.setText(_translate("MainWindow", "Seed"))
        self.map_size_label.setText(_translate("MainWindow", "Map size"))
        self.biome_label.setText(_translate("MainWindow", "Biome"))
        self.solid_rock_label.setText(_translate("MainWindow", "Solid Rock"))
        self.other_rock_label.setText(_translate("MainWindow", "Other Rock"))
        self.energy_crystals_label.setText(_translate("MainWindow", "Energy Crystals"))
        self.ore_label.setText(_translate("MainWindow", "Ore"))
        self.ecs_label.setText(_translate("MainWindow", "Energy Crystal Seams"))
        self.os_label.setText(_translate("MainWindow", "Ore Seams"))
        self.rs_label.setText(_translate("MainWindow", "Recharge Seams"))
        self.flood_level_label.setText(_translate("MainWindow", "Water/Lava Flood Level"))
        self.flood_type_label.setText(_translate("MainWindow", "Water or Lava"))
        self.erosion_sources_label.setText(_translate("MainWindow", "Erosion Sources"))
        self.landslide_sources_label.setText(_translate("MainWindow", "Landslide Sources"))
        self.slugs_label.setText(_translate("MainWindow", "Slimy Slug Holes"))
        self.randomize_button.setText(_translate("MainWindow", "Randomize"))
        self.generate_button.setText(_translate("MainWindow", "Generate"))
        self.save_button.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
