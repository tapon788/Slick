from PyQt5.QtCore import *
from PyQt5.QtGui import *


''' This is the node class for leftwing treeview '''


class Node(object):
    def __init__(self, name, plmn, parent=None):
        self._name = name
        self._parent = parent
        self._child = []
        self._plmn = plmn


        # self._plmnInfo = plmnInfo

        if parent is not None:
            parent.addChild(self)


    def addChild(self,child):
        self._child.append(child)


    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self,row):
        return self._child[row]

    def childCount(self):
        return len(self._child)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._child.index(self)


    def insertChild(self, position, child):
        if position < 0 or position > len(self._child):
            return False

        self._child.insert(position, child)
        child._parent = self
        return True

    def plmnInfo(self):
        # if self._plmn is not None:
        #     return '/'.join(self._plmn.split('/')[1:])
        return self._plmn


''' This is the node class for details treeview '''


class DetailNode(Node):
    def __init__(self,name,plmn,properties,adminstate, parent=None):
        super(DetailNode,self).__init__(name,plmn,parent)
        self._properties = properties
        self._adminstate = adminstate

    def getProperties(self):
        return self._properties

    def getAdminstate(self):
        return self._adminstate


''' This is the base tree model  '''


class Ttreemodel(QAbstractItemModel):
    def __init__(self,rootnode,parent=None):
        super(Ttreemodel,self).__init__(parent)
        self._rootnode = rootnode
        self._customchildlist = []

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            parentnode = parent.internalPointer()
        else:
            parentnode = self._rootnode

        return parentnode.childCount()

    def columnCount(self, parent=None, *args, **kwargs):
        return 2

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == Qt.DisplayRole:
            if p_int == 0:
                return self._rootnode.name()

            if p_int == 1:
                return 'PLMN'

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled

    def data(self, index, role=None):
        if not index.isValid():
            return None
        parentnode = index.internalPointer()
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return parentnode.name()
            elif index.column() == 1:
                return parentnode.plmnInfo()

        # if role == Qt.DecorationRole:
        #     plmn = parentnode.plmnInfo()
        #     if plmn.split('/')[-1].find('BTS')>=0:
        #         return QIcon(os.getcwd()+'\\resources\\img\\icons\\2g.svg')

    def parent(self, index=None):

        parentnode = index.internalPointer()

        parent = parentnode.parent()

        if parent == self._rootnode:
            return QModelIndex()
        else:
            return self.createIndex(parent.row(), 0, parent)

    def index(self, p_int, p_int_1, parent=None, *args, **kwargs):

        parentnode = self.getNode(parent)
        # if index.isValid():
        #     parentnode = index.internalPointer()
        # else:
        #     parentnode = self._rootnode

        childnode = parentnode.child(p_int)

        if childnode:
            return self.createIndex(p_int,p_int_1,childnode)
        else:
            return QModelIndex()


    def mimeData(self, index):
        
        node = index[1].data() # to drag plmn info not item itself
        mimedata = QMimeData()
        mimedata.setText(node)
        return mimedata



    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._rootnode


''' Thid is inherited from custom Ttreemodel for detail tree view '''


class TSingleTreeModel(Ttreemodel):
    def __init__(self, rootnode, parent=None):
        super(TSingleTreeModel, self).__init__(rootnode, parent=None)

    def data(self, index, role=None):
        if not index.isValid():
            return None
        parentnode = index.internalPointer()
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return parentnode.name()
            elif index.column() == 1:
                return parentnode.plmnInfo()

        # if role == Qt.SizeHintRole:
        #     return QSize(200, 45)

        if role == Qt.DecorationRole:
            if index.column() == 0:
                if parentnode.getAdminstate() == '3':
                    return QColor('red')



class TparameterTreeModel(Ttreemodel):
    def __init__(self,root_node,parent=None):
        super(TparameterTreeModel,self).__init__(root_node,parent)


    def columnCount(self, parent=None, *args, **kwargs):
        return 2


    def data(self, index, role=None):
        if not index.isValid():
            return None
        parentnode = index.internalPointer()
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return parentnode.name()
            elif index.column() == 1:
                return parentnode.plmnInfo()

''' This custom model also filters children  in response to onTableSearch '''


class TfilterProxyModel(QSortFilterProxyModel):
    def __index__(self):
        super(TfilterProxyModel, self).__index__(self)

    def filterAcceptsRow(self, p_int, QModelIndex):
        res = super(TfilterProxyModel, self).filterAcceptsRow(p_int, QModelIndex)
        idx = self.sourceModel().index(p_int, 0, QModelIndex)

        if self.sourceModel().hasChildren(idx):
            num_items = self.sourceModel().rowCount(idx)
            for i in range(num_items):
                res = res or self.filterAcceptsRow(i, idx)

        return res


''' This is the base table model '''


class Ttablemodel(QAbstractTableModel):
    def __init__(self, data, header, parent=None, *args, **kwargs):
        super(Ttablemodel,self).__init__(*args,**kwargs)
        self._data = data
        self._header = header

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        if self._data:
            return len(self._data[0])
        else:
            return 0

    def data(self, index, role=None):
        if role == Qt.EditRole:
            return self._data[index.row()][index.column()]

        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self._data[row][col]
            # if value:
            #     return value.upper()
            return value

    def flags(self, QModelIndex):
        return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def headerData(self, section, Qt_Orientation, role=None):
        if role == Qt.DisplayRole:
            if Qt_Orientation == Qt.Horizontal:
                return self._header[section]
            
            if Qt_Orientation == Qt.Vertical:
                return str(section+1)

            else:
                return None

    # def setData(self, index, value, role = Qt.EditRole):
    #     if role == Qt.EditRole:
    #         row = index.row()
    #         col = index.column()
    #         print(value,row,col,self._data[row][col])
    #         self._data[row][col] = value

    #         self.dataChanged.emit(index,index)
    #         return True
    #     else:
    #         return False

    def getheader(self):
        return self._header



class TtablemodelCompare(Ttablemodel):
    def __init__(self, *args, **kwargs):
        super(TtablemodelCompare, self).__init__(*args,**kwargs)

    def data(self, index, role=None):

        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self._data[row][col]
            if value:
                return value
