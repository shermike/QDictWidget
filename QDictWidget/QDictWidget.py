'''
Created on 25.07.2012

@author: M.Sherstennikov
'''

from PySide import QtGui, QtCore
from QDictView import QDictView
from QDictModel import QDictModel 

class QDictWidget(QtGui.QWidget):
    
    def __init__(self, parent=None, dc= None):
        QtGui.QWidget.__init__(self, parent)
        
        l = QtGui.QVBoxLayout(self)
        
        self._view = QDictView(self)
        model = QDictModel()
        self._view.setModel(model)
        self._view.setColumnWidth( 0, 256 )
        
        l.addWidget(self._view)
        self.setLayout(l)
        
        if dc:
            model.load(dc)
