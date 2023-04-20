from PyQt5.QtCore import QRunnable,QObject,pyqtSignal,pyqtSlot
from PyQt5.QtGui import QTextCursor
import sys,traceback

class WorkerSignals(QObject):
    update = pyqtSignal(str)
    progress = pyqtSignal(int)
    error = pyqtSignal(tuple)
    finished = pyqtSignal()


class MyWorker(QRunnable):
    def __init__(self,fn,*args,**kwargs):
        super(MyWorker,self).__init__(*args,**kwargs)

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.fn(self.signals.update,self.signals.progress,*self.args,**self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()




class ParseWorker(QRunnable):
    def __init__(self,fn,*args,**kwargs):
        super(ParseWorker,self).__init__(*args,**kwargs)

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.fn(self.signals.update,self.signals.progress,self.signals.finished,*self.args,**self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
