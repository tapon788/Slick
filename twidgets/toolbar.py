from PyQt5.QtWidgets import *


class Ttoolbar(QToolBar):
    def __init__(self,*args,**kwargs):
        super(Ttoolbar,self).__init__(*args,**kwargs)
        #self.setIconSize(QSize(25,25))