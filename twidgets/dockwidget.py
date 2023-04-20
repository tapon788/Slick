from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class TdockToolbar(QDockWidget):

    def __init__(self,*args,**kwargs):
        super(TdockToolbar, self).__init__(*args, **kwargs)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self._titlebarwidget = self.titleBarWidget()
        self.setTitleBarWidget(QWidget(self))
        self.dockLocationChanged.connect(self.aligntoolbar)

        #self.setMinimumSize = 300
        #self.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea | Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        dock_height = self.height()
        doc_width = self.width()
        print (doc_width,dock_height)
        if self.isFloating():
            self.setFloating(False)
            self.setFeatures(QDockWidget.NoDockWidgetFeatures)
            self.setTitleBarWidget(QWidget(self))
        else:


            self.setFloating(True)
            self.setTitleBarWidget(self._titlebarwidget)
            self.setFeatures(QDockWidget.AllDockWidgetFeatures)
            if self.widget().__class__.__name__ == 'Ttoolbar':
                if self.widget().orientation() == Qt.Horizontal:
                    self.resize(480, dock_height)

                else:
                    self.resize(doc_width, 480)


    def aligntoolbar(self,area):
        if self.widget().__class__.__name__ == 'Ttoolbar':
            toolbar = self.widget()
            if area == Qt.TopDockWidgetArea or area == Qt.BottomToolBarArea:
                toolbar.setOrientation(Qt.Horizontal)
            if area == Qt.LeftDockWidgetArea or area == Qt.RightDockWidgetArea:
                toolbar.setOrientation(Qt.Vertical)
            self.setTitleBarWidget(QWidget(self))


class TdockWidget(QDockWidget):

    def __init__(self,*args,**kwargs):
        super(TdockWidget, self).__init__(*args, **kwargs)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self._titlebarwidget = self.titleBarWidget()
        self.setTitleBarWidget(QWidget(self))


    def mouseDoubleClickEvent(self, *args, **kwargs):
        dock_height = self.height()
        doc_width = self.width()
        print(doc_width, dock_height)
        if self.isFloating():
            self.setFloating(False)
            self.setFeatures(QDockWidget.NoDockWidgetFeatures)
            self.setTitleBarWidget(QWidget(self))
        else:

            self.setFloating(True)
            self.setTitleBarWidget(self._titlebarwidget)
            self.setFeatures(QDockWidget.AllDockWidgetFeatures)
            if self.widget().__class__.__name__ == 'Ttoolbar':
                if self.widget().orientation() == Qt.Horizontal:
                    self.resize(doc_width, dock_height)

                else:
                    self.resize(doc_width, dock_height)