from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *



from twidgets.treeview import *
import sys, os


class MyAction(QAction):
    def __init__(self, shortcut, *args, **kwargs):
        super(QAction,self).__init__(*args, **kwargs)
        tip = args[1]
        self.setToolTip(tip)
        self.setStatusTip(tip)
        #self.setCheckable(True)
        self.setShortcut(QKeySequence(shortcut))


class SettingTable(QWidget):
    def __init__(self,*args,**kwargs):
        super(SettingTable,self).__init__(*args,**kwargs)

        # Read csv file for configuraton data
        # (tuple) self.connections =  (list)header, (list)(dict)connections
        self.connections =  self.read_config_file()
        self.connection_dictionary_list = self.connections[0]
        self.header = self.connections[1]
        #Initialize table with 7 colums
        self.table = QTableWidget(1,7,self)

        #Set table cells size according to the content inside
        '''
        h = self.table.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.ResizeToContents)
        '''

        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("background-color: #AFFFAF")

        #Automatic table resize depending on contents inside
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        #Set headers in the table
        font = QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)

        for i,header in enumerate(self.header):
            item = QTableWidgetItem()
            item.setText(header)
            item.setFont(font)
            self.table.setHorizontalHeaderItem(i,item)

        #Set data in the table
        row = -1
        col = -1
        

        for d in self.connection_dictionary_list:
            
            row+=1
            col = -1
            #Inserts a new row for new data
            self.table.insertRow(self.table.rowCount())
            for key,val in d.items():
                col+=1
                item = QTableWidgetItem(val)
                self.table.setItem(row,col,item)
        
        #Root Vertical layout to contain table and buttons
        layout = QVBoxLayout(self)

        btn_container = QWidget()
        #btn_container.setStyleSheet("background-color: #FF00FF")

        btn_layout = QHBoxLayout(btn_container)



        btn_add = QPushButton("Add")
        btn_layout.addWidget(btn_add)

        btn_add.clicked.connect(self.add_row)


        self.btn_save = QPushButton('Save')
        self.btn_save.setIcon(QIcon('2g.png'))
        self.btn_save.setIconSize(QSize(50, 50))
        btn_layout.addWidget(self.btn_save)
        #btn_save.clicked.connect(self.save_config)

        btn_export_config = QPushButton('Export')
        btn_layout.addWidget(btn_export_config)
        btn_export_config.clicked.connect(self.export_config)


        # Table added to root vertical layout
        layout.addWidget(self.table)
        # Horizontal Button layout added to root vertical layout
        layout.addWidget(btn_container)

      



    #Slot for add button click
    def add_row(self):
        self.table.insertRow(self.table.rowCount())

    def export_config(self):
        pass

    #Slot for save button click
    # def save_config(self):
    #     fp = open(os.getcwd()+'\\config\\config.csv',"w+")
    #     csv_line = str()
    #     for h in self.connections[1]:
    #         csv_line += h+','
    #     fp.write(csv_line[:-1]+'\n')
    #     for row in range(self.table.rowCount()):
    #         csv_line = str()
    #         for col in range(self.table.columnCount()):
    #             item = self.table.item(row,col)
    #             try:
    #                 csv_line += item.text()+','
    #             except AttributeError:
    #                 csv_line += ','
    #         if csv_line:
    #             #print(csv_line)
    #             fp.write(csv_line[:-1]+'\n')
    #     fp.close()

    # Function to read csv file and return connection tuple
    def read_config_file(self):

        try:
            fp = open(os.getcwd()+'\\resources\\config\\config.csv','r')
        except FileNotFoundError:
            print (os.getcwd())
            print ("File not Found")
        header = []
        data = fp.readlines()
        for line in data[0].split(','):
            header.append(line.strip())
        connection_dictionary_array = []
        for line in data[1:]:
            row_data = line.strip().split(',')
            #print (row_data)
            d = dict(zip(header,row_data))
            connection_dictionary_array.append(d)
            #print (d)
        fp.close()
        return (connection_dictionary_array,header)

    def get_details_from_name(self,name_list,connection_dict_list):
        filtered_dictionary_list = []
    
        for i in connection_dict_list:
    
            for key,val in i.items():
                
                if val in name_list:
                    filtered_dictionary_list.append(i)
        return filtered_dictionary_list


class SearchDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Search')

        font = QFont("Comic sans MS",10)



        self.searchEdit = QLineEdit()
        searchlabel = QLabel('Type and press [Enter]:')
        layout = QVBoxLayout()
        layout.addWidget(searchlabel)
        layout.addWidget(self.searchEdit)
        self.setFont(font)
        self.setLayout(layout)
        self.resize(400,50)


class MyTextEdit(QTextEdit):
    def __init__(self,*args,**kwargs):
        super(MyTextEdit,self).__init__(*args,**kwargs)

        self.cursor = self.textCursor()
        # self.format = QTextCharFormat()
        # self.format.setBackground(QBrush(QColor('yellow')))
        self.pos = 0
    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Control):
            self.searchDialog = SearchDialog(self)
            self.searchDialog.show()

            self.searchDialog.searchEdit.returnPressed.connect(lambda x=self.searchDialog.searchEdit.text():self.scrollToLine(self.searchDialog.searchEdit.text()))

            #searchDialog.searchEdit.returnPressed.connect(self.onSearch)
            pass

            #self.scrollToLine(text)

    def scrollToLine(self,text):
        searchText = text

        regex = QRegExp(searchText)

        fulltext = self.toPlainText()
        index = regex.indexIn(fulltext, self.pos)
      
        if (index == -1):
            self.pos = 0
            index = regex.indexIn(fulltext, self.pos)
            if (index == -1):
               

                QMessageBox(QMessageBox.Warning,
                                      "QMessageBox.warning()", "'"+searchText+"' Not found in this log!",
                                      QMessageBox.NoButton, self).exec()



        self.cursor.setPosition(index)
        for i in range(len(searchText)):
            self.cursor.movePosition(QTextCursor.NextCharacter, 1)
        # self.cursor.mergeCharFormat(self.format)
        self.setTextCursor(self.cursor)
        # self.tv.setFocus()
        self.pos = index + regex.matchedLength()


class LicenseReport(QWidget):
    def __init__(self,group,*args,**kwargs):
        super(LicenseReport,self).__init__(*args,**kwargs)
        
        #Central Widget
        sw1 = QWidget()
        hlayout1 = QHBoxLayout(sw1)

        # #Group-box
        self.nodeListGroupBox = QGroupBox(self)
        self.nodeListGroupBox.setTitle('Node List')

        # #vlayout
        self.vlayout = QVBoxLayout(self.nodeListGroupBox)
        
        # #Radio1
        st = SettingTable()
        connections = st.read_config_file()[0]
        node_list = []
        for d in connections:
            if d['Group'] == group:
                node_list.append(d['Name'])
        self.bsc_list = node_list
        self.x = []
        
        for n,bsc in enumerate(self.bsc_list):
            r = QCheckBox(self.nodeListGroupBox)
            r.setText(bsc)
            self.x.append(r)
            self.vlayout.addWidget(r)

        # #Group-box
        self.gbox2 = QGroupBox(self)
        self.gbox2.setTitle('Options')
        # #vlayout
        vlayout2 = QVBoxLayout(self.gbox2)

        # #Radio1
        self.r1 = QRadioButton(self.gbox2)
        self.r1.setText('Select All')
        vlayout2.addWidget(self.r1)
        self.r1.clicked.connect(self.check_all_cbox)
        self.r2 = QRadioButton(self.gbox2)
        self.r2.setText('Deselect All')
        vlayout2.addWidget(self.r2)
        self.r2.clicked.connect(self.uncheck_all_cbox)

        self.btn_run = QPushButton()
        self.btn_run.setText('Collect Log')

        self.btn_lic_parse = QPushButton()
        self.btn_lic_parse.setText('Parse Log')


        self.btn_open_dir = QPushButton()
        self.btn_open_dir.setText('Open')
        self.btn_open_dir.clicked.connect(self.open_dir)

        

        hlayout1.addWidget(self.nodeListGroupBox)
        hlayout1.addWidget(self.gbox2)
        hlayout1.addWidget(self.btn_run)
        hlayout1.addWidget(self.btn_lic_parse)
        hlayout1.addWidget(self.btn_open_dir)

        vlayout_container = QVBoxLayout(self)

        self.tv = MyTextEdit()
        font = QFont()
        font.setFamily("Courier")
        self.tv.setFont(font)
        # #self.tv.setStyleSheet('background-color:#000055;color:#FFFFFF;')

        self.progressbar = QProgressBar()
        self.progressbar.hide()
        self.current_node_label = QLabel(' ')

        vlayout_container.addWidget(sw1)
        vlayout_container.addWidget(self.tv)
        vlayout_container.addWidget(self.current_node_label)
        vlayout_container.addWidget(self.progressbar)
        
        #self.setCentralWidget(self)






    def check_all_cbox(self):
        for i in self.x:
            i.setChecked(True)

    def uncheck_all_cbox(self):
        for i in self.x:
            i.setChecked(False)

    def open_dir(self):
        os.startfile(os.getcwd()+'\\logs\\')

