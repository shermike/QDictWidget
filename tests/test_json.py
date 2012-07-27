'''
Created on 25.07.2012

@author: M.Sherstennikov
'''
from QDictWidget import *
import sys


fname = 'test_tree.json'

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    from orion.tools import norm_json
    dd = norm_json.load(fname)
    #dd = norm_json.load(r'D:\orion\projects\iar\stm_direct_surgut\resources\dscr\var_dscr.json')

    window = QtGui.QMainWindow()
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    
    qdict = QDictWidget(window, dd)
    window.setCentralWidget(qdict)
    
    def save():
        qdict.save("D:/"+fname)#norm_json.save("D:/"+fname, dd)
    
    menuFile = window.menuBar().addMenu( "File" )
    menuFile.addAction( "Save", save)
    
    #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
    window.show()
    
    sys.exit(app.exec_())