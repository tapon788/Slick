from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QKeySequence



class MyAction(QAction):
    def __init__(self,shortcut,*args,**kwargs):
        super(QAction,self).__init__(*args,**kwargs)
        tip = args[1]
        self.setToolTip(tip)
        self.setStatusTip(tip)
        #self.setCheckable(True)
        self.setShortcut(QKeySequence(shortcut))
