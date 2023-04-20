from PyQt5.QtWidgets import *
from twidgets.tableview import *

class TtableDBWidget(QWidget):
    def __init__(self ,*args ,**kwargs):
        super(TtableDBWidget, self).__init__(*args, **kwargs)

        '''Set Main Layout'''
        mainlayout = QVBoxLayout()

        '''Set Top horizontal Layout'''
        toplayout = QHBoxLayout()
        mainlayout.addLayout(toplayout)
        self.setLayout(mainlayout)
        toplayout.setContentsMargins(0, 0, 0, 0)
        mainlayout.setContentsMargins(0, 0, 0, 0)

        ''' Top Layout Widgets '''
        ''' Table onTableSearch field '''
        self.search_table = QLineEdit()
        self.search_table.setPlaceholderText('Search in the table ...')

        ''' Sql query field '''
        self.sql_query_field = QLineEdit()
        self.sql_query_field.setPlaceholderText('Write SQL query ...')

        ''' Table choose combobox '''
        self.combo_choose_table  = QComboBox()

        ''' Buttons to export table and database '''
        self.btn_export_table = QPushButton('Export Table')
        self.btn_export_db = QPushButton('Export DB')

        ''' Table '''
        self.table = Ttableview()
        self.table.verticalHeader().setDefaultSectionSize(5)
        self.table.horizontalHeader().setDefaultSectionSize(100)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        '''to enable sorting'''
        self.table.setSortingEnabled(True)

        ''' DB Status Label '''
        self.status_label = QLabel('Here goes the status level')
        hlayout = QHBoxLayout()
        hs = QSpacerItem(10 ,10 ,QSizePolicy.Expanding)
        hlayout.addItem(hs)
        hlayout.addWidget(self.status_label)
        ''' Adding widgets to toplayout '''
        toplayout.addWidget(self.combo_choose_table)
        toplayout.addWidget(self.btn_export_table)
        toplayout.addWidget(self.btn_export_db)
        toplayout.addWidget(self.sql_query_field)
        ''' Adding widgets to main layout '''
        mainlayout.addWidget(self.search_table)
        mainlayout.addWidget(self.table)
        mainlayout.addLayout(hlayout)

        ''' Few layout design commands not used '''
        # layout.addStretch()
        # self.setStyleSheet('border:2px solid red;background-color:grey')
        # layout.setSpacing(0)
        # self.setStyleSheet('border:2px solid pink')

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):

        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()