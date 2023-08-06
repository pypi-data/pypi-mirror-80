import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot

from pubsub import pub

import astrocabtools.cube_ans.src.ui.ui_rectangleSelection

__all__=["RectangleSelectionC"]

class RectangleSelectionC(QDialog, astrocabtools.cube_ans.src.ui.ui_rectangleSelection.Ui_rectangleSelection):

    def __init__(self, parent=None):
        super(RectangleSelectionC, self).__init__(parent)
        self.setupUi(self)

        pub.subscribe(self.set_coordinates, 'rectangleSelected')

        self.updateButton.clicked.connect(self.update_rectangle)

        self.rectangleSelectionComboBox.currentIndexChanged.connect(self.change_state_coordinates)

    def set_coordinates(self, ix, iy, ex, ey):
        ixRound = self.set_round_value(ix)
        iyRound = self.set_round_value(iy)
        exRound = self.set_round_value(ex)
        eyRound = self.set_round_value(ey)

        topLeftX = 0
        topLeftY = 0

        topRightX = 0
        topRightY = 0

        bottomLeftX = 0
        bottomLeftY = 0

        bottomRightX = 0
        bottomRightY = 0


        #Same pixel
        if ixRound == exRound and iyRound == eyRound:
            topLeftX = ixRound
            topRightX = ixRound
            bottomLeftX = ixRound
            bottomRightX = ixRound

            topLeftY = iyRound
            topRightY = iyRound
            bottomLeftY = iyRound
            bottomRightY = iyRound

        #Start Top left rectangle
        elif ixRound < exRound and iyRound > eyRound:

            topLeftX = ixRound
            topRightX = exRound
            bottomLeftX = ixRound
            bottomRightX = exRound

            topLeftY = iyRound
            topRightY = eyRound
            bottomLeftY = iyRound
            bottomRightY = eyRound

        #Start Bottom left rectangle
        elif ixRound < exRound and iyRound < eyRound:

            topLeftX = ixRound
            topRightX = exRound
            bottomLeftX = ixRound
            bottomRightX = exRound

            topLeftY = eyRound
            topRightY = eyRound
            bottomLeftY = iyRound
            bottomRightY = iyRound

        #Start Top right rectangle
        elif ixRound > exRound and iyRound > eyRound:

            topLeftX = exRound
            topRightX = ixRound
            bottomLeftX = exRound
            bottomRightX = ixRound

            topLeftY = iyRound
            topRightY = iyRound
            bottomLeftY = eyRound
            bottomRightY = eyRound

        #Start Bottom right rectangle
        elif ixRound > exRound and iyRound < eyRound:

            topLeftX = exRound
            topRightX = ixRound
            bottomLeftX = exRound
            bottomRightX = ixRound

            topLeftY = eyRound
            topRightY = eyRound
            bottomLeftY = iyRound
            bottomRightY = iyRound

        #Same X and goes from left to right Y
        elif ixRound == exRound and iyRound > eyRound:

            topLeftX = ixRound
            topRightX = ixRound
            bottomLeftX = ixRound
            bottomRightX = ixRound

            topLeftY = iyRound
            topRightY = eyRound
            bottomLeftY = iyRound
            bottomRightY = eyRound

        #Same X and goes from right to left Y
        elif ixRound == exRound and iyRound < eyRound:

            topLeftX = exRound
            topRightX = ixRound
            bottomLeftX = exRound
            bottomRightX = ixRound

            topLeftY = eyRound
            topRightY = iyRound
            bottomLeftY = eyRound
            bottomRightY = iyRound

        #Same Y and goes from top to bottom X
        elif ixRound < exRound and iyRound == eyRound:

            topLeftX = ixRound
            topRightX = exRound
            bottomLeftX = ixRound
            bottomRightX = exRound

            topLeftY = iyRound
            topRightY = iyRound
            bottomLeftY = iyRound
            bottomRightY = iyRound

        #Same Y and goes from bottom to top X
        elif ixRound > exRound and iyRound == eyRound:

            topLeftX = exRound
            topRightX = ixRound
            bottomLeftX = exRound
            bottomRightX = ixRound

            topLeftY = iyRound
            topRightY = iyRound
            bottomLeftY = iyRound
            bottomRightY = iyRound

        self.topLeftXLineEdit.setText(str(topLeftX))
        self.topLeftXLineEdit.setText(str(topLeftX))
        self.topLeftXLineEdit.setText(str(topLeftX))
        self.topLeftXLineEdit.setText(str(topLeftX))
        self.topLeftXLineEdit.setText(str(topLeftX))
        self.topLeftYLineEdit.setText(str(topLeftY))

        self.topRightXLineEdit.setText(str(topRightX))
        self.topRightYLineEdit.setText(str(topRightY))

        self.bottomLeftXLineEdit.setText(str(bottomLeftX))
        self.bottomLeftYLineEdit.setText(str(bottomLeftY))

        self.bottomRightXLineEdit.setText(str(bottomRightX))
        self.bottomRightYLineEdit.setText(str(bottomRightY))

    def change_state_coordinates(self, index):
        """Set enabled state of all line edit based on the item selected"""

        if index == 0:

            self.topLeftXLineEdit.setReadOnly(True)
            self.topLeftYLineEdit.setReadOnly(True)

            self.topRightXLineEdit.setReadOnly(True)
            self.topRightYLineEdit.setReadOnly(True)

            self.bottomLeftXLineEdit.setReadOnly(True)
            self.bottomLeftYLineEdit.setReadOnly(True)

            self.bottomRightXLineEdit.setReadOnly(True)
            self.bottomRightYLineEdit.setReadOnly(True)

        elif index == 1:

            self.topLeftXLineEdit.setReadOnly(False)
            self.topLeftYLineEdit.setReadOnly(False)

            self.topRightXLineEdit.setReadOnly(True)
            self.topRightYLineEdit.setReadOnly(True)

            self.bottomLeftXLineEdit.setReadOnly(True)
            self.bottomLeftYLineEdit.setReadOnly(True)

            self.bottomRightXLineEdit.setReadOnly(False)
            self.bottomRightYLineEdit.setReadOnly(False)

        elif index == 2:

            self.topLeftXLineEdit.setReadOnly(True)
            self.topLeftYLineEdit.setReadOnly(True)

            self.topRightXLineEdit.setReadOnly(False)
            self.topRightYLineEdit.setReadOnly(False)

            self.bottomLeftXLineEdit.setReadOnly(False)
            self.bottomLeftYLineEdit.setReadOnly(False)

            self.bottomRightXLineEdit.setReadOnly(True)
            self.bottomRightYLineEdit.setReadOnly(True)

    @pyqtSlot()
    def update_rectangle(self):
        """Get data from the active line edit coordinates and create the rectangle on the plot"""

        index = self.rectangleSelectionComboBox.currentIndex()

        try:
            if index == 0:
                self.update_alert("Error: No coordinates avaliable")
            elif index == 1:
                coord1 = (int(self.topLeftXLineEdit.text()), int(self.topLeftYLineEdit.text()))
                coord2 = (int(self.bottomRightXLineEdit.text()), int(self.bottomRightYLineEdit.text()))
                pub.sendMessage('rectangleCoordinates', coord1 = coord1, coord2 = coord2)
            else:
                coord1 = (int(self.topRightXLineEdit.text()), int(self.topRightYLineEdit.text()))
                coord2 = (int(self.bottomLeftXLineEdit.text()), int(self.bottomLeftYLineEdit.text()))
                pub.sendMessage('rectangleCoordinates', coord1 = coord2, coord2 = coord1)

        except Exception as e:
            self.generic_alert("Error while getting coordinate data")
    def set_round_value(self, data):
        if data %1 >= 0.5:
            return int(math.ceil(data))
        else:
            return int(round(data))

    def update_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()

    def generic_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()
