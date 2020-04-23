# -*- coding: utf-8 -*-
# Created on Sun Jul 14 10:17:54 2019
# @author: Cédric Perion | Arthur Dujardin


"""
This is the python-colorply GUI.
"""

import sys

# PyQt
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QFileDialog, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QComboBox, QProgressBar, QLabel
from PyQt5.QtCore import pyqtSignal, QThread  # Threading

# Colorply modules
from colorply.process.improcess import add_cloud_channel
from colorply.ui.palette import set_dark_theme


class RunThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        super(RunThread, self).__init__()

    def run(self, window):
        """
        Run the process in a different thread.

        Parameters
        ----------
        window : PyQT5 window
            The main window.

        Returns
        -------
        None.
        """

        imDir = window.imageDirLine.text()
        oriDir = window.imageOri.text()
        imExt = "." + str(window.imageExt.currentText())
        cal = window.calibDirLine.text()
        inPly = window.inPlyLine.text()
        outPly = window.outPlyLine.text()
        channel = window.imageChannelLine.text()
        modestr = str(window.computeMethod.currentText())
        mode = window.modeDict[modestr]

        # A sexy way to check if none of the fields are empty
        if len(oriDir) * len(imDir) * len(cal) * len(inPly) * len(outPly) * len(channel):

            try:
                window.warningLabel.setVisible(False)
                window.progress.setValue(1.0)
                window.progress.setMaximum(1.0)
                window.progress.setVisible(True)
                var = add_cloud_channel(inPly, cal, oriDir, imDir, imExt, channel, mode, outPly, window.progress)
                if var:
                    window.warningLabel.setText("All done !")
                    window.warningLabel.setVisible(True)
                return


            except FileNotFoundError:
                window.progress.setVisible(False)
                window.warningLabel.setText("One of the files / folders has not been found.")
                window.warningLabel.setVisible(True)
                return

        else:
            window.warningLabel.setVisible(True)
            window.progress.setVisible(False)
            return


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # QThread.__init__(self)
        self.initUI()

    def initUI(self):
        """
        Initialyze the window with different buttons and actions.

        Returns
        -------
        None.
        """

        self.setWindowTitle('Python-colorply')

        hbox1 = QHBoxLayout()  # image directory line
        hbox2 = QHBoxLayout()  # orientation image directory
        hbox3 = QHBoxLayout()  # calibration directory line
        hbox4 = QHBoxLayout()  # input ply line
        hbox5 = QHBoxLayout()  # output ply line
        hbox6 = QHBoxLayout()  # channel, compute method and run button line
        hbox7 = QHBoxLayout()
        vbox = QVBoxLayout()

        # Image extension
        self.imageExt = QComboBox()
        self.extList = ["JPG", "jpg", "TIF", "tif", "PNG", "png", "CR2", "DNG"]  # list of all extension available     
        for k in range(len(self.extList)):  # adding the possibilities
            self.imageExt.addItem(self.extList[k])
        self.imageExt.setFixedWidth(50)

        # Compute method
        self.computeMethod = QComboBox()
        # dictionnary of all methods available
        self.modeDict = {
            "Average": "avg",
            "Random": "alea",
            "Weighted Average": "wavg",
            "Distance": "dist",
        }
        # adding the methods to a drop down menu
        for k in self.modeDict:
            self.computeMethod.addItem(k)

        # Text lines
        self.imageDirLine = QLineEdit()
        self.imageOri = QLineEdit()
        self.imageChannelLabel = QLabel("Channel name :")
        self.imageChannelLine = QLineEdit()
        self.calibDirLine = QLineEdit()
        self.inPlyLine = QLineEdit()
        self.outPlyLine = QLineEdit()

        self.warningLabel = QLabel("Error: please fill all the fields !")
        self.warningLabel.setVisible(False)

        # Buttons
        imageChooseButton = QPushButton("Choose your image folder")
        imageChooseButton.setFixedWidth(194)
        imageChooseButton.clicked.connect(self.select_image_dir)

        oriChooseButton = QPushButton("Choose orientation folder")
        oriChooseButton.setFixedWidth(250)
        oriChooseButton.clicked.connect(self.select_ori_dir)

        calibChooseButton = QPushButton("Choose your calibration file")
        calibChooseButton.setFixedWidth(250)
        calibChooseButton.clicked.connect(self.select_calib_dir)

        inPlyChooseButton = QPushButton("Choose your input PLY file")
        inPlyChooseButton.setFixedWidth(250)
        inPlyChooseButton.clicked.connect(self.select_input_ply)

        outPlyChooseButton = QPushButton("Choose your output PLY file")
        outPlyChooseButton.setFixedWidth(250)
        outPlyChooseButton.clicked.connect(self.select_output_ply)

        computeButton = QPushButton("RUN")
        computeButton.clicked.connect(self.compute)

        # Progress bar
        self.progress = QProgressBar(self)
        self.progress.setVisible(False)

        # Boxes
        hbox1.addWidget(self.imageDirLine)
        hbox1.addWidget(imageChooseButton)
        hbox1.addWidget(self.imageExt)

        hbox2.addWidget(self.imageOri)
        hbox2.addWidget(oriChooseButton)

        hbox3.addWidget(self.calibDirLine)
        hbox3.addWidget(calibChooseButton)

        hbox4.addWidget(self.inPlyLine)
        hbox4.addWidget(inPlyChooseButton)

        hbox5.addWidget(self.outPlyLine)
        hbox5.addWidget(outPlyChooseButton)

        hbox6.addWidget(self.computeMethod)
        hbox6.addWidget(self.imageChannelLabel)
        hbox6.addWidget(self.imageChannelLine)
        hbox6.addWidget(computeButton)

        hbox7.addWidget(self.progress)
        hbox7.addWidget(self.warningLabel)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)

        vbox.addStretch(1)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)

        self.setLayout(vbox)

    def select_image_dir(self):
        """
        Select the image directory from the window.

        Returns
        -------
        None.
        """

        fname = QFileDialog.getExistingDirectory(self, 'Select image directory')
        if fname:
            self.imageDirLine.setText(fname)

    def select_ori_dir(self):
        """
        Select the MicMac orientation directory from the window.

        Returns
        -------
        None.
        """

        fname = QFileDialog.getExistingDirectory(self, 'Select image orientation directory')
        if fname:
            self.imageOri.setText(fname)

    def select_calib_dir(self):
        """
        Select the MicMac calibration directory from the window.

        Returns
        -------
        None.
        """

        fname = QFileDialog.getOpenFileName(self, 'Select calibration file')
        if fname[0]:
            self.calibDirLine.setText(fname[0])

    def select_input_ply(self):
        """
        Select the input ply file from the window.

        Returns
        -------
        None.
        """

        fname = QFileDialog.getOpenFileName(self, 'Select input PLY file')
        if fname[0]:
            self.inPlyLine.setText(fname[0])

    def select_output_ply(self):
        """
        Select the output ply file from the window.

        Returns
        -------
        None.
        """

        fname = QFileDialog.getSaveFileName(self, 'Select output PLY file name')
        if fname[0]:
            self.outPlyLine.setText(fname[0])

    def compute(self):
        """
        Run the process module, with different threads.

        Returns
        -------
        None.
        """

        thread = RunThread()
        thread.run(self)


def colorply_window():
    """
    Create the main window of Colorply.

    Returns
    -------
    None.
    """

    app = QApplication(sys.argv)
    app = set_dark_theme(app)
    window = MainWindow()
    window.show()
    app.exec_()
