import sys

from PyQt5.QtWidgets import QApplication, QTreeView

from Slick.tests.tjwakeham.node import Node
from Slick.tests.tjwakeham.model import FileSystemTreeModel


app = QApplication(sys.argv)

model = FileSystemTreeModel(Node('Filename'), path='c:/')


tree = QTreeView()
tree.setModel(model)

tree.show()

sys.exit(app.exec_())