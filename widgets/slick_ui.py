'''
Library Imports:
Basic packages contains default python packages
Slick packages contains custom packaged created for this project
Unused imports hash-out may be used later
'''

__author__ = 'Tapon Paul'

# Python basic libraries
import sys, os,time

# Slick package imports
from Slick import *

'''unused imports'''
# from Slick.widgets.ui_bsc_license_report import LicenseReport
# from Slick.widgets.ui_settings import SettingTable
from Slick.worker.qrunnables import MyWorker,WorkerSignals
from Slick.ssh.ssh_script import SlickSSH
import prettytable
# import qdarkstyle
import xlsxwriter
from Slick.licpareser.logParser import ParseLog
from Slick.licpareser.licenseModel import lic_info,ucap


class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.setWindowTitle('Slick1.04.22')


        ''' Setting geometry to set window size and position with
            respect to the monitor '''

        self.setGeometry(
            QApplication.desktop().availableGeometry().x(),
            QApplication.desktop().availableGeometry().y(),
            QApplication.desktop().availableGeometry().width(),
            QApplication.desktop().availableGeometry().height()-50,
        )

        # Define widgets and layouts
        mainCentralWidget = QWidget()
        mainVlayout = QVBoxLayout()
        middleHlayout = QHBoxLayout()
        container_middleHlayout = QWidget()
        container_middleHlayout.setLayout(middleHlayout)
        #container_middleHlayout.setStyleSheet('border:2px solid green;background-color:orange;')

        leftwing = Tleftwing()

        self.rightwing = TrightWing()

        middleHlayout.addWidget(leftwing)
        middleHlayout.addWidget(self.rightwing)
        mainVlayout.addWidget(container_middleHlayout)

        #mainVlayout.setContentsMargins(0,0,0,0)
        middleHlayout.setSpacing(0)
        middleHlayout.setContentsMargins(0,0,0,0)

        #rightVlayout.setContentsMargins(0, 0, 0, 0)
        mainCentralWidget.setLayout(mainVlayout)

        # Add a toolbar
        self.toolbar = Ttoolbar("My Toolbar")
        mainVlayout.addWidget(self.toolbar)
        self.addToolBar(self.toolbar)

        # Dock-up toolbar
        self.dock = TdockToolbar('Toolbar', mainCentralWidget)
        self.dock.setWidget(self.toolbar)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock)

        # Dockup leftwing

        self.dock_lw = TdockWidget('Leftwing',mainCentralWidget)
        self.dock_lw.setWidget(leftwing)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dock_lw)


        #Dockup rightwing

        # self.dock_rw = TdockWidget('RightWing',mainCentralWidget)
        #
        # self.dock_rw.setWidget(rightwing)
        # self.addDockWidget(Qt.RightDockWidgetArea,self.dock_rw)
        #
        # '''Add status bar'''
        # self.setStatusBar(QStatusBar(self))

        # Central mainCentralWidget
        mainVlayout.setContentsMargins(0,0,0,0)
        self.setCentralWidget(mainCentralWidget)
        #mainCentralWidget.setStyleSheet('background-image:url("../resources/bg.jpg");opacity:0.5;')

        #Toolbar members and Action button clicks

        button_action_home = MyAction('Ctrl+b', QIcon(os.getcwd()+'\\resources\\img\\icons\\home.svg'),'Home',self)
        self.toolbar.addAction(button_action_home)
        button_action_home.triggered.connect(lambda x='btn_home':self.onMyButtonActionClicked('btn_home'))
        self.toolbar.addSeparator()


        button_action_lic_report_bsc = MyAction('Ctrl+b',QIcon(os.getcwd()+'\\resources\\img\\icons\\2g.svg'),'BSC License Report',self)
        self.toolbar.addAction(button_action_lic_report_bsc)
        button_action_lic_report_bsc.triggered.connect(lambda x='btn_bsc_lic_report':self.onMyButtonActionClicked('btn_bsc_lic_report'))
        self.toolbar.addSeparator()

        button_action_lic_report_rnc = MyAction('Ctrl+r',QIcon(os.getcwd()+'\\resources\\img\\icons\\3g.svg'),'RNC License Report',self)
        self.toolbar.addAction(button_action_lic_report_rnc)
        button_action_lic_report_rnc.triggered.connect(lambda x='btn_rnc_lic_report': self.onMyButtonActionClicked('btn_rnc_lic_report'))
        self.toolbar.addSeparator()

        button_action_ping_report_rnc = MyAction('Ctrl+p',QIcon(os.getcwd()+'\\resources\\img\\icons\\ping.svg'),'RNC Ping Report',self)
        self.toolbar.addAction(button_action_ping_report_rnc)
        button_action_ping_report_rnc.triggered.connect(lambda x='btn_bsc_ping_report': self.onMyButtonActionClicked('btn_bsc_ping_report'))
        self.toolbar.addSeparator()

        button_action_sla_report = MyAction('Ctrl+s',QIcon(os.getcwd()+'\\resources\\img\\icons\\report.svg'),'Banglalink RAN SLA',self)
        self.toolbar.addAction(button_action_sla_report)
        button_action_sla_report.triggered.connect(lambda x='btn_sla_report': self.onMyButtonActionClicked('btn_sla_report'))
        self.toolbar.addSeparator()

        button_action_settings = MyAction('Alt+s',QIcon(os.getcwd()+'\\resources\\img\\icons\\settings.svg'),'Settings',self)
        self.toolbar.addAction(button_action_settings)
        button_action_settings.triggered.connect(lambda x='btn_settings': self.onMyButtonActionClicked('btn_settings'))
        self.toolbar.addSeparator()

        button_action_log = MyAction('Alt+s',QIcon(os.getcwd()+'\\resources\\img\\icons\\log.svg'),'Log',self)
        self.toolbar.addAction(button_action_log)
        button_action_log.triggered.connect(lambda x='btn_log': self.onMyButtonActionClicked('btn_log'))


        # Add the menu bar
        menu = self.menuBar()
        menu.setNativeMenuBar(False) # Disable global menubar on mac

        file_menu = menu.addMenu('Reports')
        file_menu.addAction(button_action_home)
        file_menu.addAction(button_action_lic_report_bsc)
        file_menu.addAction(button_action_lic_report_rnc)
        file_menu.addSeparator()
        file_menu.addAction(button_action_ping_report_rnc)
        file_menu.addSeparator()
        file_menu.addAction(button_action_sla_report)

        file_menu = menu.addMenu('Settings')
        file_menu.addAction(button_action_settings)

        #BTN Clicks
        
        self.rightwing.settingsUI.btn_save.clicked.connect(self.onBtnSaveSettingClicked)
        self.rightwing.licenseReportUIBsc.btn_run.clicked.connect(lambda x='BSC':self.onBtnLicReportClicked('BSC'))
        self.rightwing.licenseReportUIBsc.btn_lic_parse.clicked.connect(lambda x='BSC':self.onBtnLicParseClicked('BSC'))




        #variable initialize
        #ThreadPoool
        self.threadpool = QThreadPool()

        #
        self.get_connection_info = []

        #
        self.openfilespath = str()



        '''
        widget-code separation starts here

                        LEFT WING

        '''

        '''Get Tree Model like data from sqlite database'''

        self.search_tree = leftwing.search_tree
        self.search_tree.textChanged.connect(self.onTreeSearch)

        self.dbcon = ConnectDB(os.getcwd()+'\\..\\db\\sran.sqlite')
        rn_bsc = self.dbcon.getnodes('BSC','bcf')
        rn_rnc = self.dbcon.getnodes('RNC','wbts')
        rn_mrbts = self.dbcon.getnodes('MRBTS')

        self.tree_bsc = leftwing.tree_bsc
        model_bsc = Ttreemodel(rn_bsc)
        self.proxy_model_bsc = FilterProxyModel()
        self.proxy_model_bsc.setSourceModel(model_bsc)
        self.tree_bsc.setModel(self.proxy_model_bsc)

        self.tree_rnc = leftwing.tree_rnc
        model_rnc = Ttreemodel(rn_rnc)
        self.proxy_model_rnc = FilterProxyModel()
        self.proxy_model_rnc.setSourceModel(model_rnc)
        self.tree_rnc.setModel(self.proxy_model_rnc)

        self.tree_mrbts = leftwing.tree_mrbts
        model_mrbts = Ttreemodel(rn_mrbts)
        self.proxy_model_mrbts = FilterProxyModel()
        self.proxy_model_mrbts.setSourceModel(model_mrbts)
        self.tree_mrbts.setModel(self.proxy_model_mrbts)

        ''' Tree MRBTS Context Menu '''
        self.tree_mrbts.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_mrbts.customContextMenuRequested.connect(lambda x: self.openMenu(x,self.tree_mrbts.currentIndex()))


        '''

                        RIGHT WING

        '''

        self.search_table = self.rightwing.tableViewDatabase.search_table
        self.sql_query_field = self.rightwing.tableViewDatabase.sql_query_field
        self.combo_choose_table = self.rightwing.tableViewDatabase.combo_choose_table
        self.btn_export_table = self.rightwing.tableViewDatabase.btn_export_table
        self.btn_export_db = self.rightwing.tableViewDatabase.btn_export_db
        self.table = self.rightwing.tableViewDatabase.table


        self.search_table.textChanged.connect(self.search)
        self.sql_query_field.returnPressed.connect(
            lambda x=self.sql_query_field.text(): self.creatableonquery(self.sql_query_field.text()))

        ''' Load combobox items using sqlite database table's name '''
        self.db_tables = []
        #self.dbcon = ConnectDB(os.getcwd() + '\\..\\db\\sran.sqlite')
        combo_itmes = self.dbcon.getDataFromQuery('SELECT name FROM sqlite_master '
                                             'WHERE type="table" ORDER BY name;')[0]

        [self.db_tables.append(i[0]) for i in combo_itmes]
        self.combo_choose_table.addItems(self.db_tables)
        self.combo_choose_table.currentIndexChanged.connect(self.changemodel)

        ''' Load rightwing's table with data from a table '''
        data = self.dbcon.getdata('name,mrbts,btsname,plmn', 'mrbts', None)
        print(data)
        if data[1]:
            self.table_header = data[1]
            self.model = Ttablemodel(data[0], self.table_header)
            self.table_proxy_model = QSortFilterProxyModel()
            self.table_proxy_model.setSourceModel(self.model)
            self.table_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
            self.table.setModel(self.table_proxy_model)
            '''to add items into filtering if newly added'''
            self.table_proxy_model.dynamicSortFilter()
            '''to filter from all columns'''
            self.table_proxy_model.setFilterKeyColumn(-1)
        else:
            print(data[0])




    '''
    SLOTS for all SIGNALS emitted from components of MainWindow class
    '''
    def onTreeSearch(self, s):
        self.proxy_model_bsc.setFilterRegExp(s)
        self.proxy_model_rnc.setFilterRegExp(s)
        self.proxy_model_mrbts.setFilterRegExp(s)

    ''' Context Menu '''
    def openMenu(self, position, proxyindex):
        indexes = self.tree_mrbts.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        menu = QMenu()
        if level == 0:
            a = menu.addAction(self.tr("Connect BSC"))
            a.triggered.connect(lambda x: self.connectTosbts(self.tree_mrbts.model().data(proxyindex)))
        elif level == 1:
            menu.addAction(self.tr("Edit object/container"))
            menu.addAction(self.tr("Lock BCF"))
            menu.addAction(self.tr("Unlock BCF"))
            menu.addAction(self.tr("Reset BCF"))
            menu.addAction(self.tr("Get BCF"))

        elif level == 2:
            menu.addAction(self.tr("Edit object"))

        menu.exec_(self.tree_mrbts.viewport().mapToGlobal(position))

    ''' Slot for context Menu fired Signal '''
    def connectTosbts(self, info):
        self.dbcon = ConnectDB(os.getcwd()+'\\..\\db\\sran.sqlite')
        data = self.dbcon.getdata('ip','sranvlan','userlabel="oam" and mrbts='+info.split('-')[-1])[0][0]

    ''' Right Wing Signals '''
    def changemodel(self, comboindex):
        tablename = self.db_tables[comboindex]
        self.combo_choose_table.currentIndex()
        data = self.dbcon.getdata('*', tablename, None)
        self.cmodel(data)
        self.sql_query_field.selectAll()

    def search(self,s):
        print (s)
        self.table_proxy_model.setFilterRegExp(s)

    def creatableonquery(self,q):
        if q:
            if q.upper() == "SHOW TABLES;":
                q = "SELECT name FROM sqlite_master WHERE type=\"table\" ORDER BY name;"
            elif q.upper().find("DESC") >= 0 and q.upper().find(";") >= 0:
                t = q.split(';')[0].split(' ')[-1].strip()
                q = 'pragma table_info("'+t+'");'
            data = self.dbcon.getDataFromQuery(q)
            self.cmodel(data)
        else:
            pass

    def cmodel(self,data):
        if data is None:
            data = ([], "Empty")
        if data[1]:
            header = data[1]
            self.model = Ttablemodel(data[0], header)
            self.table_proxy_model.setSourceModel(self.model)
            self.table.setModel(self.table_proxy_model)
        else:
            error = data[0]
            error_message = 'Not a correct SQL statement!\n' + error
            self.warning("SQL Error", error_message)

    def warning(self,text,title):
        QMessageBox.critical(self,title,text)




    ''' Action button slots to switch widgets on rightwing '''
    def onMyButtonActionClicked(self, s):
        if s == 'btn_home':
            self.rightwing.licenseReportUIBsc.setVisible(False)
            self.rightwing.licenseReportUIRnc.setVisible(False)
            self.rightwing.tableViewDatabase.setVisible(True)
            self.rightwing.settingsUI.setVisible(False)
        if s == 'btn_bsc_lic_report':
            self.rightwing.licenseReportUIBsc.setVisible(True)
            self.rightwing.licenseReportUIRnc.setVisible(False)
            self.rightwing.tableViewDatabase.setVisible(False)
            self.rightwing.settingsUI.setVisible(False)
        if s == 'btn_rnc_lic_report':
            self.rightwing.licenseReportUIBsc.setVisible(False)
            self.rightwing.licenseReportUIRnc.setVisible(True)
            self.rightwing.tableViewDatabase.setVisible(False)
            self.rightwing.settingsUI.setVisible(False)
        if s == 'btn_settings':
            self.rightwing.settingsUI.setVisible(True)
            self.rightwing.licenseReportUIBsc.setVisible(False)
            self.rightwing.licenseReportUIRnc.setVisible(False)
            self.rightwing.tableViewDatabase.setVisible(False)
        if s == 'btn_log':
            QFileDialog.getOpenFileName('C:\\')

    def onBtnSaveSettingClicked(self):
        self.connections = self.settigs_widget.read_config_file()
        new_entries = []

        fp_prev = open(os.getcwd() + '\\config\\config.csv', "r")
        table_prev = fp_prev.readlines()
        fp = open(os.getcwd() + '\\config\\config.csv', "w+")
        csv_line = str()
        for h in self.connections[1]:
            csv_line += h + ','
        fp.write(csv_line[:-1] + '\n')
        for row in range(self.settigs_widget.table.rowCount()):
            csv_line = str()
            for col in range(self.settigs_widget.table.columnCount()):
                item = self.settigs_widget.table.item(row, col)
                try:
                    csv_line += item.text() + ','
                except AttributeError:
                    csv_line += ','
            if csv_line:
                if '' in csv_line[:-1].split(','):
                    continue
                if csv_line[:-1] + '\n' not in table_prev:
                    new_entries.append(dict(zip(self.connections[1], csv_line[:-1].split(','))))
                fp.write(csv_line[:-1] + '\n')
        fp.close()

        fp_prev.close()

        for d in new_entries:
            if d['Group'] == 'BSC':
                r = QCheckBox(self.rightwing.licenseReportUIBsc.gbox)
                r.setText(d['Name'])
                self.rightwing.licenseReportUIBsc.x.append(r)
                self.rightwing.licenseReportUIBsc.vlayout.addWidget(r)

            if d['Group'] == 'RNC':
                r = QCheckBox(self.rightwing.licenseReportUIRnc.gbox)
                r.setText(d['Name'])
                self.rightwing.licenseReportUIRnc.x.append(r)
                self.rightwing.licenseReportUIRnc.vlayout.addWidget(r)


    # Collect Log button slot on license report ui
    def onBtnLicReportClicked(self, s):
        self.connections = self.rightwing.settingsUI.read_config_file()
            
        get_connection_info = []

        if s == 'BSC':
            self.rightwing.licenseReportUIBsc.progressbar.show()
            #self.rightwing.licenseReportUIBsc.progressbar.show()
            print('#' * 50)
            for i in self.rightwing.licenseReportUIBsc.x:
                print(i)
                if i.isChecked():
                    get_connection_info.append(i.text())

            connection_info_details = self.rightwing.settingsUI.get_details_from_name(get_connection_info, self.connections[0])

            # ssh = SlickSSH(connection_info_details, '\r', ['ZW7I:LIC,FULL;',
            #                                                'ZW7I:FEA,FULL:FSTATE=ON;',
            #                                                'ZW7I:FEA,FULL:FSTATE=OFF;',
            #                                                'ZW7I:UCAP,FULL;'])

            ssh = SlickSSH(connection_info_details,'\r', ['cd virtualenvironment/scraping/bin/',
                                                     'source activate',
                                                     'cd corona',
                                                     'scrapy crawl corona'])

            worker = MyWorker(ssh.execute_cmd)#,self.rightwing.licenseReportUIBsc.tv)
            worker.signals.update.connect(self.update_tv)
            worker.signals.progress.connect(self.progress)
            worker.signals.finished.connect(self.finish)
            worker.signals.error.connect(self.error)
            self.threadpool.start(worker)

        if s == 'RNC':
            self.rightwing.licenseReportUIRnc.progressbar.show()
            for i in self.rightwing.licenseReportUIRnc.x:
                if i.isChecked():
                    get_connection_info.append(i.text())
            connection_info_details = self.settigs_widget.get_details_from_name(get_connection_info, self.connections[0])
            ssh2 = SlickSSH(connection_info_details, '\n', ['fsclish -c "show license all"'])
            rnc_worker = MyWorker(ssh2.execute_cmd, self.rightwing.licenseReportUIRnc.tv)
            rnc_worker.signals.update.connect(self.update_tv2)
            rnc_worker.signals.progress.connect(self.progress2)
            self.threadpool.start(rnc_worker)


    ###############################################################
    #                                                             #
    #                       SIGNAL SLOTS                          #
    #                                                             #
    ###############################################################

    # Signal Slot for update (BSC license report widget)
    def update_tv(self, s):
        # self.rightwing.licenseReportUIBsc.current_node_label.setText(s)
        self.rightwing.licenseReportUIBsc.tv.append(s)
        pass


    # Signal Slot for progressbar ui (BSC license report widget)
    def progress(self, s):
        self.rightwing.licenseReportUIBsc.progressbar.setValue(s)


    # Signal Slot for finish (BSC license report widget)
    def finish(self):
        self.rightwing.licenseReportUIBsc.current_node_label.setText("Finished")


    # Signal Slot for error (BSC license report widget)
    def error(self, s):
        for i in s:
            self.rightwing.licenseReportUIBsc.tv.append(str(i).replace('\n', '\n\n'))
        self.rightwing.licenseReportUIBsc.progressbar.hide()
        self.rightwing.licenseReportUIBsc.current_node_label.hide()
        self.rightwing.licenseReportUIBsc.tv.setStyleSheet("color:red")


    # Signal Slot for update (RNC license report widget)
    def update_tv2(self, s):
        self.rightwing.licenseReportUIRnc.current_node_label.setText(s)
        pass


    # Signal Slot for progressbar ui (RNC license report widget)
    def progress2(self, s):
        self.rightwing.licenseReportUIRnc.progressbar.setValue(s)


    # Signal Slot for finish (BSC license report widget)
    def finish2(self):
        self.rightwing.licenseReportUIRnc.current_node_label.setText("Finished")


    # Signal Slot for error (BSC license report widget)
    def error2(self, s):
        for i in s:
            self.rightwing.licenseReportUIRnc.tv.append(str(i).replace('\n', '\n\n'))
        self.rightwing.licenseReportUIRnc.progressbar.hide()
        self.rightwing.licenseReportUIRnc.current_node_label.hide()
        self.rightwing.licenseReportUIRnc.tv.setStyleSheet("color:red")


    # Signal Slot for progressbar ui (BSC license report widget on Parsing)
    def progress3(self, s):
        self.rightwing.licenseReportUIBsc.progressbar.setValue(s)


    def license_parser(self, update, progress):
        pt = prettytable.PrettyTable()

        update.emit('*' * 5 + 'License Parsing Started ' + time.strftime("%A %X %D") + '*' * 5)
        # update.emit('-' * 5 +'License Parsing Started '+time.strftime("%D")+'-' * 5  )
        wb = xlsxwriter.Workbook(os.getcwd() + '\\output\\lic_report.xlsx')

        ############################### LIC FULL ############################################

        keys = list(self.input_files_dict)

        if 'lic_bsc_log' in keys:

            # screen.append('Parsing '+self.input_files_dict['lic_bsc_log']+'\n')

            fp = open(self.input_files_dict['lic_bsc_log'], 'r')
            log = fp.readlines()
            fp.close()
            # screen.append('Working with License Full\n')
            # print('-' * 80 + ' LP BSC PLOG')
            inst_parse_log = ParseLog()

            collectedlog = inst_parse_log.grep(log, 'ZW7I:LIC', '<W7_>', '----------------------------------------------',
                                               'ZW7I:LIC', 'mcBSC')
            specific_info = ['CONTROLLER NAME', 'CONTROLLER CNUM', 'CUSTOMER ID', 'LICENCE CODE', 'LICENCE NAME',
                             'LICENCE FILE NAME', 'LICENCE CAPACITY', 'CUSTOMER NAME']
            object_array = []

            # screen.append('Writing license info in execel sheet : BSC LIC\n')

            ws = wb.add_worksheet('BSC LIC')
            row = 0
            for spinfo in specific_info:
                ws.write(row, specific_info.index(spinfo), spinfo)

            pt.field_names = ['Controller', 'Code', 'Name', 'File', 'Capacity']

            for array in collectedlog:

                inst_lic_info = lic_info(specific_info)
                # print (inst_lic_info.match)
                # pt.field_names = inst_lic_info.match
                col = -1
                for i in array:
                    for spinfo in specific_info:
                        if i.find(spinfo) >= 0:
                            inst_lic_info.value[inst_lic_info.match.index(spinfo)] = i.split(':')[-1].replace('.',
                                                                                                              '').strip()
                row += 1
                # print(inst_lic_info.value)
                pt.add_row([inst_lic_info.value[0], inst_lic_info.value[3], inst_lic_info.value[4], inst_lic_info.value[5],
                            inst_lic_info.value[6]])
                for d in inst_lic_info.value:
                    col += 1
                    ws.write(row, col, d)
            update.emit(str(pt))
            progress.emit(10)

            # -----------------------------------------------------------------------------------------------------------------

            ############################### BSC FEA ############################################
            # screen.append('Working with FEA ON and OFF\n')
            inst_parse_log = ParseLog()
            collectedlog = inst_parse_log.grep(log, 'ZW7I:FEA', '<W7_>', '----------------------------------------------',
                                               'ZW7I:FEA', 'mcBSC')

            specific_info = ['CONTROLLER NAME', 'CONTROLLER CNUM', 'FEATURE CODE', 'FEATURE NAME', 'FEATURE STATE']
            object_array = []
            # screen.append('Writing license info in execel sheet : BSC FEA\n')
            ws = wb.add_worksheet('BSC FEA')
            row = 0
            for spinfo in specific_info:
                ws.write(row, specific_info.index(spinfo), spinfo)

            for array in collectedlog:
                inst_lic_info = lic_info(specific_info)
                col = -1
                for i in array:
                    for spinfo in specific_info:
                        if i.find(spinfo) >= 0:
                            inst_lic_info.value[inst_lic_info.match.index(spinfo)] = i.split(':')[-1].replace('.', '')
                row += 1

                for d in inst_lic_info.value:
                    col += 1
                    ws.write(row, col, d)
            progress.emit(40)
            ############################### BSC UCAP ############################################
            # screen.append('Working with UCAP\n')
            inst_parse_log = ParseLog()
            collectedlog = inst_parse_log.grep_ucap(log)

            object_array = []

            for array in collectedlog:

                inst_ucap = ucap()

                for i in array:
                    if i.find('CONTROLLER NAME:') >= 0:
                        inst_ucap.bsc_name = i.split(':')[-1].replace('.', '')
                    if i.find('CONTROLLER CNUM:') >= 0:
                        inst_ucap.bsc_cnum = i.split(':')[-1].replace('.', '')

                    inst_ucap.feature_code = i.split('          ')[0].strip()
                    inst_ucap.capacity_usage = i.split('          ')[-1].strip()

                object_array.append(inst_ucap)
            # screen.append('Writing license info in execel sheet : BSC UCAP\n')
            ws = wb.add_worksheet('BSC UCAP')
            ws.write(0, 0, 'CONTROLLER NAME')
            ws.write(0, 1, 'CONTROLLER CNUM')
            ws.write(0, 2, 'FEATURE CODE')
            ws.write(0, 3, 'USED CAPACITY')

            row = 0
            for i in object_array:
                row += 1
                ws.write(row, 0, i.bsc_name)
                ws.write(row, 1, i.bsc_cnum)
                ws.write(row, 2, i.feature_code)
                ws.write(row, 3, i.capacity_usage)
            progress.emit(70)
        # -----------------------------------------------------------------------------------------------------------------
        ############################### RNC LIC ############################################

        if 'lic_rnc_log' in keys:
            # screen.append('Working with License ALL\n')
            fp = open(self.input_files_dict['lic_rnc_log'], 'r')
            log = fp.readlines()
            fp.close()
            inst_parse_log_rnc = ParseLog()
            collectedlog = inst_parse_log_rnc.grep(log, '@RNC-', 'The total number of licenses ',
                                                   '------------------------------------------------------------------',
                                                   '@RNC-',
                                                   '@RNC-')

            specific_info = ['RNC ID', 'License Code', 'License Name', 'Allowed Capacity', 'License Serial Number',
                             'License Start Time', 'License End Time',
                             'Order ID', 'Customer ID', 'Customer Name', 'Feature Code', 'Feature Name', 'License State',
                             'License State']
            object_array = []
            # screen.append('Writing license info in execel sheet : RNC LIC\n')
            ws = wb.add_worksheet('RNC LIC')
            row = 0
            for spinfo in specific_info:
                ws.write(row, specific_info.index(spinfo), spinfo)

            for array in collectedlog:
                inst_lic_info = lic_info(specific_info)
                col = -1
                for i in array:
                    # print(i)
                    for spinfo in specific_info:
                        if i.find(spinfo) >= 0:
                            # print(i)
                            inst_lic_info.value[inst_lic_info.match.index(spinfo)] = ''.join(i.split(':')[1:]).replace('.',
                                                                                                                       '').strip()
                row += 1
                for d in inst_lic_info.value:
                    col += 1
                    ws.write(row, col, d)
        wb.close()
        progress.emit(100)

        # screen.append('Check output at '+os.getcwd()+'\\output\\lic_report.xlsx')
        # input(
        #     '\n\t\tLicense Parsing Done\n\t\tCheck output at [' + os.getcwd() + '\\out\\lic_report.xlsx] \n\t\tPress [ENTER] to exit')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    #app.setStyleSheet(qdarkstyle.load_stylesheet())
    window.show()
    app.exec_()