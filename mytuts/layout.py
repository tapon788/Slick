'''
BASICS:
We need one QMainWindow and inside this one Widget as central widget.
each layout contains Qwidgets as block to achieve the layout. If we
need a vertical layout, then add a VBoxLayout and then add Qwidgets to 
that layout.

One layout stands/inflates on top of a parent widget and contains multiple child 
Widgets

'''

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,QLabel,
    QApplication,
    QVBoxLayout,
    QHBoxLayout)

from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.setWindowTitle('Slick1.04.22')
        self.setGeometry(
            QApplication.desktop().availableGeometry().x()+50,
            QApplication.desktop().availableGeometry().y()+100,
            QApplication.desktop().availableGeometry().width()-100,
            QApplication.desktop().availableGeometry().height()-150,
        )

        # Define widgets and layouts
        self.main_central_widget = QWidget()
        self.main_central_widget.setStyleSheet('border:2px solid red;background-color:orange;')
        
        #Vertical layout
        self.main_vlayout = QVBoxLayout()
        self.vwidget1 = QLabel('Vertical-1')
        self.vwidget1.setStyleSheet('border:2px solid red;background-color:white;')

        self.vwidget2 = QLabel('Vertical-2')
        self.vwidget2.setStyleSheet('border:2px solid red;background-color:blue;')

        self.main_vlayout.addWidget(self.vwidget1)
        self.main_vlayout.addWidget(self.vwidget2)

        #Horizontal Layout
        self.hlayout = QHBoxLayout()
        self.hwidget1 = QLabel("Horizontal-1")
        self.hwidget1.setStyleSheet('border:2px solid red;background-color:green;')
        self.hwidget2 = QLabel("Horizontal-2")
        self.hwidget2.setStyleSheet('border:2px solid red;background-color:white;')
        self.hlayout.addWidget(self.hwidget1)
        self.hlayout.addWidget(self.hwidget2)
        self.vwidget1.setLayout(self.hlayout)

        self.main_central_widget.setLayout(self.main_vlayout)
        self.setCentralWidget(self.main_central_widget)



if __name__ == '__main__':
    import sys,os

    app = QApplication(sys.argv)
    app_icon = QIcon(os.getcwd()+'\\resources\\img\\icons\\slick.svg')
    app.setWindowIcon(app_icon)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())