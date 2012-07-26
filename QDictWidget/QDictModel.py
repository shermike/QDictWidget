'''
Created on 25.07.2012

@author: M.Sherstennikov
'''
from PySide import QtCore
import functools
import sip
sip.setapi('QVariant', 2)

def print_res(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print("%s -> %s" % (func.__name__, str(res)))
        return res
    return wrapper
              

class QDictModelItem:
    
    def __init__(self, name=None, data=None, parent=None):
        self.name = name
        self.data = data
        self.parent = parent
        self.children = []
    
    def dump(self, indent=0):
        print(' '*indent + str(self))
        for i in self.children:
            try:
                i.dump(indent+2)
            except AttributeError as e:
                print("'%s': %s" % (i, str(e)))
                
    def to_dict(self, parent=None):
        if not parent:
            parent = {}
        if self.children:
            parent[self.name] = {}
        else:
            return
        for i in self.children:
            try:
                i.to_dict(parent[self.name])
            except AttributeError as e:
                print("'%s': %s" % (i, str(e)))
        return parent
    
    @property
    def data_str(self):
        if isinstance(self.data, dict) or isinstance(self.data, list):
            return None
        return str(self.data)
    
    def __str__(self):
        value = self.data
        if isinstance(self.data, dict):
            value = 'dict'
        elif isinstance(self.data, list):
            value = 'list'
        return "%s : %s" % (self.name, value)

class QDictModel(QtCore.QAbstractItemModel):

    header = [ 'Name', 'Value']

    def __init__(self):
        QtCore.QAbstractItemModel.__init__(self)
        
        self._dict = None
        
    def load_item(self, name, data, parent=None):
        item = QDictModelItem(None)
        item.name = name
        item.data = data
        item.parent = parent
        
        if isinstance(data, dict):
            for n, v in data.items():
                it = self.load_item(n, v, item)
                if it:
                    it.index = len(item.children)
                    item.children.append(it)
                    
        if isinstance(data, list):
            for i, v in enumerate(data):
                it = self.load_item(str(i), v, item)
                if it:
                    it.index = len(item.children)
                    item.children.append(it)
                    
        return item
        
    def load(self, data):
        assert isinstance(data, dict), "QDictModel can not load not dictionary data"
        self._dict = data
        self.root = self.load_item('Root', data)
        self.root.dump()
        
    def rowCount(self, parent):
        pitem = None
        if parent.isValid():
            pitem = parent.internalPointer()
        else:
            pitem = self.root
        if pitem:
            return len(pitem.children) 
        return 0
    
    def columnCount(self, parent):
        return 2
    
    def data(self, index, role):
        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return None
        
        if not index.isValid():
            return None
        
        item = index.internalPointer()
        
        if index.column() == 0:
            return item.name
        elif index.column() == 1:
            return item.data_str
        
    def index(self, row, column, parent):
        #print(inspect.stack()[0][3])
        if parent.isValid():
            pitem = parent.internalPointer()
        else:
            pitem = self.root
        return self.createIndex(row, column, pitem.children[row])
    
    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        
        item = index.internalPointer()
        
        par = item.parent
        
        if not par or par == self.root:
            return QtCore.QModelIndex()
        
        return self.createIndex(par.index, 0, par)
    
    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEditable  
    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        return self.header[section]
    
    def supportedDragActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction