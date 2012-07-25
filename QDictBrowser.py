'''
Created on 25.06.2012

@author: Mike
'''
from PySide import QtGui, QtCore
import sys
import collections
from QDictView import QDictView
from QDictModel import QDictModel  
from QDictTreeWidget import QDictTreeWidget
import json
import types

       
    
class QDictBrowser(QtGui.QWidget):

    h_idx_name = 0
    h_idx_value = 1

    def __init__(self, parent=None, dc= None):
        QtGui.QWidget.__init__(self, parent, )
        
        l = QtGui.QVBoxLayout(self)
        
#===============================================================================
#        self._treeView = QDictView(self)
#        self._treeModel = QDictModel(self)
#        if dc:
#            self._treeModel.load(dc)
#        self._treeView.setModel(self._treeModel)
# 
#        l.addWidget(self._treeView)
#        self.setLayout(l)
#===============================================================================
                
        self._tree = QDictTreeWidget(self)
               
        
        l.addWidget(self._tree)
        self.setLayout(l)
        
        if dc:
            self._tree.load(dc)
    
    
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    from orion.tools import norm_json
    dd = norm_json.load('test_tree.json')
    #dd = norm_json.load(r'D:\orion\projects\iar\stm_direct_surgut\resources\dscr\var_dscr.json')

    
    window = QtGui.QMainWindow()
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    
    #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
    qdict = QDictBrowser(window, dd)
    window.setCentralWidget(qdict)
    window.show()
    
    sys.exit(app.exec_())
    