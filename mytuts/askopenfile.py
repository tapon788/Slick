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
    QWidget,QLabel,QPushButton,QFileDialog,QLineEdit,
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
        self.openfilespath = str()
        # Define widgets and layouts
        self.main_central_widget = QWidget()
        
        
        #Vertical layout
        self.main_vlayout = QHBoxLayout()
        # self.vwidget1 = QLabel('Vertical-1')
        # self.vwidget1.setStyleSheet('border:2px solid red;background-color:white;')

        self.editbox=QLineEdit()
        self.btn = QPushButton("Click me")
        self.btn.setFixedWidth(100)
        self.btn.clicked.connect(self.onBtnLicParseClicked)

        self.main_vlayout.addWidget(self.editbox)
        self.main_vlayout.addWidget(self.btn)
        
        self.main_central_widget.setLayout(self.main_vlayout)
        self.setCentralWidget(self.main_central_widget)
        
        self.main_vlayout.setSpacing(0)
        self.btn.setFixedHeight(35)
        self.editbox.setFixedHeight(33)
    
    def onBtnLicParseClicked(self, s):

        filename = QFileDialog.getOpenFileName(self, "Open File", "C:\\","All Files (*)")
        self.editbox.setText(filename[0])
        

if __name__ == '__main__':
    import sys,os

    app = QApplication(sys.argv)
    app_icon = QIcon(os.getcwd()+'\\resources\\img\\icons\\slick.svg')
    app.setWindowIcon(app_icon)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())