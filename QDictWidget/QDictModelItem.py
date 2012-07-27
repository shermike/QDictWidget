'''
Created on 26.07.2012

@author: M.Sherstennikov
'''
import collections

class QDictModelItem(object):
    
    def __init__(self, name=None, dat=None, parent=None):
        self.name = name
        self._data = dat
        self.parent = parent
        self.children = []
        
    @property
    def index(self):
        if self.parent:
            return self.parent.children.index(self)
    
    def dump(self, indent=0):
        print(' '*indent + str(self))
        for i in self.children:
            try:
                i.dump(indent+2)
            except AttributeError as e:
                print("'%s': %s" % (i, str(e)))
                
    def to_dict(self, dc=None):
        if dc is None:
            dc = collections.OrderedDict()
        data = None
        if isinstance(self.data, dict):
            data = collections.OrderedDict()
        elif isinstance(self.data, list):
            data = []
        else:
            data = self._data
            
        # ignore root node
        if self.name is not None:
            if isinstance(dc, dict):
                dc[self.name] = data
            elif isinstance(dc, list):
                dc.append(data)
        for i in self.children:
            try:
                i.to_dict(data)
            except AttributeError as e:
                print("'%s': %s" % (i, str(e)))
        return data
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if self._data is not None:
            if isinstance(self._data, bool):
                assert value in ('True', 'False'), "Invalid value for bool type" 
                self._data = True if value == 'True' else False
            else:
                self._data = type(self._data)(value)
        else:
            self._data = value
    
    @property
    def data_str(self):
        if isinstance(self.data, dict) or isinstance(self.data, list):
            return None
        return str(self.data)
    
    def add_child(self, child, name):
        if isinstance(self._data, dict):
            pass
    
    def __str__(self):
        value = self.data
        if isinstance(self.data, dict):
            value = 'dict'
        elif isinstance(self.data, list):
            value = 'list'
        return "%s : %s" % (self.name, value)
