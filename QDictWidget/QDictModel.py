'''
Created on 25.07.2012

@author: M.Sherstennikov
'''
from PySide import QtCore
import functools
import json
from QDictModelItem import QDictModelItem

def print_res(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print("%s -> %s" % (func.__name__, str(res)))
        return res
    return wrapper

def iterate(data):
    if isinstance(data, dict):
        for n, v in data.items():
            yield n, v
                
    if isinstance(data, list):
        for i, v in enumerate(data):
            yield str(i), v

class QDictModel(QtCore.QAbstractItemModel):

    HEADER_NAME = 'Name'
    HEADER_VALUE = 'Value'

    header = [ HEADER_NAME, HEADER_VALUE]
    
    def __init__(self):
        QtCore.QAbstractItemModel.__init__(self)
        
        self._dict = None
        
    def load_item(self, name, data, parent=None):
        item = QDictModelItem(None)
        item.name = name
        if isinstance(data, dict):
            item.data = {}
        elif isinstance(data, list):
            item.data = []
        else:
            item.data = data
        item.parent = parent
        
        for n, v in iterate(data):
            it = self.load_item(n, v, item)
            if it:
                #it.index = len(item.children)
                item.children.append(it)
        
        #=======================================================================
        # if isinstance(data, dict):
        #    for n, v in data.items():
        #        it = self.load_item(n, v, item)
        #        if it:
        #            it.index = len(item.children)
        #            item.children.append(it)
        #            
        # if isinstance(data, list):
        #    for i, v in enumerate(data):
        #        it = self.load_item(str(i), v, item)
        #        if it:
        #            it.index = len(item.children)
        #            item.children.append(it)
        #=======================================================================
        return item
    
    def load_idx(self, name, data, parent=None):
        pitem = parent.internalPointer()
        
        if name:
            item = QDictModelItem(None)
            item.name = name
            item.parent = pitem
            
            if isinstance(data, dict):
                item.data = {}
            elif isinstance(data, list):
                item.data = []
            else:
                item.data = data
                return item
        else:
            item = pitem
        
        self.beginInsertRows(parent, self.rowCount(parent), len(data))
        
        self.insertRows(self.rowCount(parent), len(data), parent)
                
        self.endInsertRows()
        
        for n, v in iterate(data):
            idx = self.index(row, 0, parent)
            it = self.load_idx(n, v, item)
            if it:
                item.children.append(it)

        return item
        
    def load(self, data):
        assert isinstance(data, dict), "QDictModel can not load not dictionary data"
        self.root = self.load_item(None, data)
        #d = self.root.to_dict()
        #print(d)
        #self.root.dump()
        
    def save(self, fname, fmt='json'):
        d = self.root.to_dict()
        data = None
        if fmt == 'json':
            data = json.dumps(d, indent=2, encoding='ascii')
            
        assert data, "Unknown save format: %s" % str(fmt) 
        with open(fname, "w") as f:
            f.write(data)
        
    def insertRows(self, row, count, parent):
        if not parent.isValid():
            return False
        
        item = parent.internalPointer()
        print "%s : insert %d rows at %d" % (item.name, count, row)
#        for i in range(count):
#            it = QDictModelItem("asd", 8, item)
#            item.children.append(it)
            
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
        return len(self.header)
    
    def data(self, index, role):
        if not index.isValid():
            return None
        if role == QtCore.Qt.UserRole:
            return index.internalPointer()
        
        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return None
        
        item = index.internalPointer()
        
        if index.column() == self.header.index(self.HEADER_NAME):
            return item.name
        elif index.column() == self.header.index(self.HEADER_VALUE):
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
    
    def setData(self, index, value, role):
        if not index.isValid():
            return False
        item = index.internalPointer()
        if role == QtCore.Qt.EditRole:
            try:
                if index.column() == self.header.index(self.HEADER_NAME):
                    item.name = value
                elif index.column() == self.header.index(self.HEADER_VALUE):
                    item.data = value
            except:
                return False
            return True
        elif role == QtCore.Qt.UserRole:
#            self.beginInsertRows(index, self.rowCount(index)-1, len(value))
#            self.insertRows(self.rowCount(index), len(value), index)
#            self.endInsertRows()
#            
#            parent = QDictModelItem()
#            n = next(value.iterkeys())
#            parent.name = n 
#            it = self.load_idx(n, value, index)
#            item.children.append(it)
            
            self.load_idx(None, value, index)
            
#            for n, v in iterate(value):
#                it = self.load_idx(n, v, index)
#                if it:
#                    item.children.append(it)
                    
            start_idx = self.index(self.rowCount(index)-1, 0, index)
            
            
            end_idx = self.index(self.rowCount(index)-1, 0, index)
            b = self.emit( QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"), start_idx, end_idx )
            b = self.emit( QtCore.SIGNAL("layoutChanged()") )
            
            print(b)