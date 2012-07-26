'''
Created on 25.07.2012

@author: M.Sherstennikov
'''
from PySide import QtGui, QtCore

class QDictView(QtGui.QTreeView):
    
    def __init__(self, parent):
        QtGui.QTreeView.__init__(self, parent)
        
        self.setSelectionMode(self.ExtendedSelection)
        self.setAlternatingRowColors(True)
        self.setRootIsDecorated(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        