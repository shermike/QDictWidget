'''
Created on 25.07.2012

@author: M.Sherstennikov
'''

import collections
import json
from PySide import QtGui, QtCore
from QDictView import QDictView
from QDictModel import QDictModel
from QDictDelegate import QDictDelegate

class QDictWidget(QtGui.QWidget):
    
    def __init__(self, parent=None, dc= None):
        QtGui.QWidget.__init__(self, parent)
        
        l = QtGui.QVBoxLayout(self)
        
        self._view = QDictView(self)
        self._model = QDictModel()
        self._view.setModel(self._model)
        self._view.setColumnWidth( 0, 256 )
        self._view.setItemDelegate(QDictDelegate(self._view))
        
        l.addWidget(self._view)
        self.setLayout(l)
        
        if dc:
            self._model.load(dc)
            
    def save(self, fname, fmt='json'):
        self._model.save(fname, fmt)

    def copy(self):
        clipboard = QtGui.QApplication.clipboard()
        data = collections.OrderedDict()
        
        for i in self._view.selectedIndexes():
            item = self._model.data(i, QtCore.Qt.UserRole)
            d = item.to_dict(data)
        
        text = json.dumps(data, indent=2)
        clipboard.setText(text)

            
    def paste(self):
        index = self._view.currentIndex()
        item = self._model.data(index, QtCore.Qt.UserRole)
        if not item or (not isinstance(item.data, dict) and not isinstance(item.data, list)):
            return
        
        clipboard = QtGui.QApplication.clipboard()
        text = clipboard.text()
        data = json.loads(text, object_pairs_hook=collections.OrderedDict)
        self._model.setData(index, data, QtCore.Qt.UserRole)
        #self._model.insertRows(self._model.rowCount(index), 1, index)
        #idx = self._model.index(self._model.rowCount(index), 0, index)
        #self._model.setData(index, data, QtCore.Qt.UserRole)
        
    def cut(self, copy=True):       
        if copy:
            self.copy()
            
        for i in self.selectedItems():
            print i.text(0)
            parent = i.parent()
            if parent:
                parent.takeChild(parent.indexOfChild(i))
            else:
                self.takeTopLevelItem(self.indexOfTopLevelItem(i))
            #self.removeItemWidget(i, 0)
    
    def keyPressEvent(self, event):
        if event.modifiers() | QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_C:
            self.copy()
        elif event.modifiers() | QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_V:
            self.paste()
        elif event.modifiers() | QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_X:
            self.cut()
        elif event.key() == QtCore.Qt.Key_Delete:
            self.cut(copy=False)
        elif event.key() == QtCore.Qt.Key_Insert:
            self.insert()
        else:
            QtGui.QWidget.keyPressEvent(self, event)