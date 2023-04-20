from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class Ttableview(QTableView):
    def __init__(self,*args,**kwargs):
        super(Ttableview,self).__init__(*args,**kwargs)
        self.setCornerButtonEnabled(True)
        #
        # h = self.horizontalHeader()
        # h.setSectionResizeMode(QHeaderView.ResizeToContents)
        #self.setAcceptDrops(True)
        #self.horizontalHeader().setStretchLastSection(True)
        #self.resizeColumnsToContents()
        #self.resizeRowsToContents()
        #header.setSectionResizeMode(QHeaderView.ResizeToContents)

    def dragEnterEvent(self, e):
      
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, event):
        droppedText = event.mimeData().text()
        self.setText(droppedText)
        print(droppedText+' Done :-)')

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_C:
            model = self.model()
            header = model.sourceModel().getheader()
            print('ctrl+c pressed')

            selection = self.selectionModel()
            indexes = selection.selectedIndexes()
            data = str()
            header_index = []
            headerlist = []
            #try:
            previous = indexes[0].row()
            for i in indexes:
                if i.column() not in header_index:
                    header_index.append(i.column())
                    headerlist.append(header[i.column()])
                if i.row() == previous:
                    data += '\t'
                else:
                    data += '\n'
                previous = i.row()
                d = model.data(i)
                if not d:
                    d = str()
                data += d
            



            headerstring = '\t'.join(headerlist)+'\n'
        
            QApplication.clipboard().setText(headerstring+data[1:])
            # except:
            #     QApplication.clipboard().setText('')



class TtableviewCompare(Ttableview):
    def __init__(self,*args,**kwargs):
        super(TtableviewCompare,self).__init__(*args,**kwargs)
        #self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeColumnsToContents()
        self.setAlternatingRowColors(True)

        # To resize row height
        verticalHeader = self.verticalHeader()
        verticalHeader.setSectionResizeMode(QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(16)


        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)



        tablestyles = """
        font-size:14px;
        """
        headerstyles =  """
        font-weight:bold;
        """
        self.horizontalHeader().setStyleSheet(headerstyles)
        self.setStyleSheet(tablestyles)
