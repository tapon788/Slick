import sys
from PyQt5.QtCore import Qt, QMimeData, QLocale
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QTreeView


class SceneTreeModel(QStandardItemModel):
    def mimeData(self, indexes):
        print(indexes)
        name = indexes[0].data()
        print('called mimeData on ' + name)
        mimedata = QMimeData()
        mimedata.setText(name)
        return mimedata

    # def supportedDropActions(self):
    #     return Qt.MoveAction
    #
    # def canDropMimeData(self, data, action, row, column, parent):
    #     print('can drop called on')
    #     print(parent.data())
    #     return True
    #
    # def dropMimeData(self, data, action, row, column, parent):
    #     parent_name = parent.data()
    #     node_name = data.text()
    #     print("Dropped {} onto {}".format(node_name, parent_name))
    #     return True


def give_model():
    model = SceneTreeModel()
    # create a tree item
    item1 = QStandardItem('item1')
    item2 = QStandardItem('item2')
    item3 = QStandardItem('item3')

    model.invisibleRootItem().appendRow(item1)
    item1.appendRow(item2)
    model.invisibleRootItem().appendRow(item3)

    return model


class UI_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(UI_MainWindow, self).__init__(parent)
        Left = 250
        Top = 100
        Width = 250
        Height = 300
        self.setGeometry(Left, Top, Width, Height)
        self.setWindowTitle("MainWindow")
        self.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.treeView = QTreeView(self)
        self.treeView.setRootIsDecorated(False)
        self.treeView.setObjectName("treeView")
        self.treeView.header().setVisible(False)

        self.setCentralWidget(self.treeView)

        self.treeView.setModel(give_model())
        self.treeView.setDragDropMode(QAbstractItemView.InternalMove)
        self.treeView.expandAll()


if __name__ == '__main__':
    MainAppThread = QApplication([])

    MainWindow = UI_MainWindow()
    MainWindow.show()

    sys.exit(MainAppThread.exec_())
