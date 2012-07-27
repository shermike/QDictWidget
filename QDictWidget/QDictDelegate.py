'''
Created on 26.07.2012

@author: M.Sherstennikov
'''
from PySide import QtGui, QtCore
from QDictModelItem import QDictModelItem

class QDictDelegate(QtGui.QItemDelegate):

    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
    
    def createEditor(self, parent, option, index):
        if not index.isValid():
            return None
        
        item = index.model().data(index, QtCore.Qt.UserRole)
        
        if index.column() == 0 and item.parent and isinstance(item.parent.data, list):
            return None
        
        if isinstance(item.data, bool):
            box = QtGui.QComboBox(parent)
            box.addItems(['False', 'True'])
            box.setCurrentIndex(int(item.data))
            #box.showPopup()
            return box
        
        return QtGui.QItemDelegate.createEditor(self, parent, option, index)
    
    def setModelData(self, editor, model, index):
        if not index.isValid():
            return None
        
        if isinstance(editor, QtGui.QComboBox):
            index.model().setData(index, editor.currentText(), QtCore.Qt.EditRole)
        else:
            QtGui.QItemDelegate.setModelData(self, editor, model, index)