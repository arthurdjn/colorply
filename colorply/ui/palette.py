# -*- coding: utf-8 -*-
# Created on Sat Jul 13 20:53:48 2019
# @author: arthurd



import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton

def set_dark_theme(app):
    """
    Set a darker theme on the PyQt window.

    Parameters
    ----------
    app : PyQt Application
        The application to change theme.

    Returns
    -------
    app : PyQt Application
        The new application an theme.
    """
    
    
    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
         
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(16, 99, 135).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)
    
    return app


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  
    
    set_dark_theme(app)
    MainWindow = QtWidgets.QMainWindow()
    button = QPushButton("test", MainWindow)
    
    MainWindow.show()
  
    sys.exit(app.exec_())
    
    
    
    
    