__author__ = 'Tapon Paul'

'''
Library Imports:
Basic packages contains default python packages
Slick packages contains custom packaged created for this project
Unused imports hash-out may be used later
'''

# Python basic libraries
import time
from PyQt5.QtCore import *


# Slick package imports

''' import from Slick package '''

#import deputy.os_utility as myhelper
from deputy import os_utility as myhelper

from twidgets.wings import *

#from twidgets.wings import *
from twidgets.components import *
from twidgets.toolbar import *
from twidgets.dockwidget import *

from tdbopeations.dbops import *

from worker.qrunnables import MyWorker, ParseWorker

from ssh.ssh_script import SlickSSH
from poko.parser_script import Prepare

from planmaker.planmaker_script import ReadInput

from Audit.DBO import DBCheckSqlite
from Audit.read_xl_input import Read_XL
from Audit.XL import MakeExcelFile


from licpareser.logParser import ParseLog
from licpareser.licenseModel import lic_info,ucap

from tests import comp

import prettytable
import qdarkstyle
import xlsxwriter
from itertools import cycle

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.setWindowTitle('Skimping RAN 0.0')
        ''' Setting geometry to set window size and position with
            respect to the monitor '''

        self.setGeometry(
            QApplication.desktop().availableGeometry().x()+50,
            QApplication.desktop().availableGeometry().y()+100,
            QApplication.desktop().availableGeometry().width()-100,
            QApplication.desktop().availableGeometry().height()-150,
        )

        #self.dbcon = ConnectDB(os.getcwd()+'\\resources\\db\\nokia.db')
        self.dbcon = ConnectDB(os.getcwd()+'\\resources\\db\\parsed_sbts.sqlite')
        

        # Define widgets and layouts
        self.main_widget = QWidget()
        #self.main_widget.setStyleSheet('border:2px solid red;')
        self.main_vlayout = QVBoxLayout()
        self.wings_hlayout = QHBoxLayout()
        self.container_wings = QWidget()
        #self.main_widget.setStyleSheet('border:2px solid green;background-color:orange;')
        self.container_wings.setLayout(self.wings_hlayout)
        #self.container_wings.setStyleSheet('border:2px solid green;background-color:orange;')
        self.main_vlayout.addWidget(self.container_wings)
        self.wings_hlayout.setSpacing(0)
        self.wings_hlayout.setContentsMargins(0, 0, 0, 0)
        self.setupUI()

        ''' Add status bar '''
        self.setStatusBar(QStatusBar(self))
        self.main_vlayout.setContentsMargins(0,0,0,0)
        self.setCentralWidget(self.main_widget)
        #self.main_widget.setStyleSheet('background-image:url("bg.jpg");')

        self.openfilespath = str()
        # ThreadPoool
        self.threadpool = QThreadPool()

    def setupUI(self):
        self.main_widget.setLayout(self.main_vlayout)
        self.setupToolbar()
        self.setupMainMenu()
        self.setupLeftwing(self.dbcon)
        self.setupRightwing(self.dbcon)


    def reloadUI(self,db_filename):
        self.rightwing.close()
        self.dock.close()
        self.dock_lw.close()
        self.leftwing.close()
        self.setupToolbar()
        self.setupLeftwing(ConnectDB(db_filename))
        self.setupRightwing(ConnectDB(db_filename))
        

    def setupToolbar(self):

        # Add a toolbar
        self.toolbar = Ttoolbar("My Toolbar")
        self.main_vlayout.addWidget(self.toolbar)
        
        self.addToolBar(self.toolbar)


        #Toolbar members and Action button clicks

        self.button_action_home = MyAction('Ctrl+b', QIcon(os.getcwd()+'\\resources\\img\\icons\\home.svg'),'Home',self)
        self.toolbar.addAction(self.button_action_home)
        self.button_action_home.triggered.connect(lambda x='btn_home':self.onMyButtonActionClicked('btn_home'))
        self.toolbar.addSeparator()

        # self.button_action_nodedetails = MyAction('Ctrl+n', QIcon(os.getcwd()+'\\resources\\img\\icons\\details.svg'),'Node Detail',self)
        # self.toolbar.addAction(self.button_action_nodedetails)
        # self.button_action_nodedetails.triggered.connect(lambda x='node_details':self.onMyButtonActionClicked('node_details'))
        # self.toolbar.addSeparator()

        self.button_action_lic_report_bsc = MyAction('Ctrl+b',QIcon(os.getcwd()+'\\resources\\img\\icons\\2g.svg'),'BSC License Report',self)
        self.toolbar.addAction(self.button_action_lic_report_bsc)
        self.button_action_lic_report_bsc.triggered.connect(lambda x='btn_bsc_lic_report':self.onMyButtonActionClicked('btn_bsc_lic_report'))
        self.toolbar.addSeparator()

        self.button_action_lic_report_rnc = MyAction('Ctrl+r',QIcon(os.getcwd()+'\\resources\\img\\icons\\3g.svg'),'RNC License Report',self)
        self.toolbar.addAction(self.button_action_lic_report_rnc)
        self.button_action_lic_report_rnc.triggered.connect(lambda x='btn_rnc_lic_report': self.onMyButtonActionClicked('btn_rnc_lic_report'))
        self.toolbar.addSeparator()

        self.button_action_parse = MyAction('Alt+p',QIcon(os.getcwd()+'\\resources\\img\\icons\\orange.svg'),'Parse XML CM Data',self)
        self.toolbar.addAction(self.button_action_parse)
        self.button_action_parse.triggered.connect(lambda x='btn_parse': self.onMyButtonActionClicked('btn_parse'))
        self.toolbar.addSeparator()

        self.button_action_reload_ui = MyAction('Alt+s',QIcon(os.getcwd()+'\\resources\\img\\icons\\reload.svg'),'Reload UI',self)
        self.toolbar.addAction(self.button_action_reload_ui)
        self.button_action_reload_ui.triggered.connect(lambda x='btn_reload': self.onMyButtonActionClicked('btn_reload'))
        self.toolbar.addSeparator()

        self.button_xmlplan = MyAction('Alt+x',QIcon(os.getcwd()+'\\resources\\img\\icons\\xml.svg'),'XML Plan maker',self)
        self.toolbar.addAction(self.button_xmlplan)
        self.button_xmlplan.triggered.connect(lambda x='btn_xmlplan': self.onMyButtonActionClicked('btn_xmlplan'))
        self.toolbar.addSeparator()
   
        self.button_parameteraudit = MyAction('Alt+a',QIcon(os.getcwd()+'\\resources\\img\\icons\\audit.svg'),'Parameter Audit',self)
        self.toolbar.addAction(self.button_parameteraudit)
        self.button_parameteraudit.triggered.connect(lambda x='btn_audit': self.onMyButtonActionClicked('btn_audit'))
        self.toolbar.addSeparator()

        self.button_action_settings = MyAction('Alt+s',QIcon(os.getcwd()+'\\resources\\img\\icons\\settings.svg'),'Settings',self)
        self.toolbar.addAction(self.button_action_settings)
        self.button_action_settings.triggered.connect(lambda x='btn_settings': self.onMyButtonActionClicked('btn_settings'))
        self.toolbar.addSeparator()



        self.button_action_qr = MyAction('Alt+x',QIcon(os.getcwd()+'\\resources\\img\\icons\\qr.svg'),'Generate QR code',self)
        self.toolbar.addAction(self.button_action_qr)
        self.button_action_qr.triggered.connect(lambda x='btn_qr': self.onMyButtonActionClicked('btn_qr'))
        self.toolbar.addSeparator()





        # self.button_action_compare = MyAction('Alt+s',QIcon(os.getcwd()+'\\resources\\img\\icons\\compare.svg'),'Log',self)
        # self.toolbar.addAction(self.button_action_compare)
        # self.button_action_compare.triggered.connect(lambda x='btn_compare': self.onMyButtonActionClicked('btn_compare'))


        # self.button_action_ping_report_rnc = MyAction('Ctrl+p',QIcon(os.getcwd()+'\\resources\\img\\icons\\ping.svg'),'RNC Ping Report',self)
        # self.toolbar.addAction(self.button_action_ping_report_rnc)
        # self.button_action_ping_report_rnc.triggered.connect(lambda x='btn_bsc_ping_report': self.onMyButtonActionClicked('btn_bsc_ping_report'))
        # self.toolbar.addSeparator()

        # self.button_action_sla_report = MyAction('Ctrl+s',QIcon(os.getcwd()+'\\resources\\img\\icons\\report.svg'),'Banglalink RAN SLA',self)
        # self.toolbar.addAction(self.button_action_sla_report)
        # self.button_action_sla_report.triggered.connect(lambda x='btn_sla_report': self.onMyButtonActionClicked('btn_sla_report'))
        # self.toolbar.addSeparator()


        # self.button_action_log = MyAction('Alt+s',QIcon(os.getcwd()+'\\resources\\img\\icons\\log.svg'),'Log',self)
        # self.toolbar.addAction(self.button_action_log)
        # self.button_action_log.triggered.connect(lambda x='btn_log': self.onMyButtonActionClicked('btn_log'))


        # Dock-up toolbar
        self.dock = TdockToolbar('Toolbar', self.main_widget)
        self.dock.setWidget(self.toolbar)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock)

    def setupMainMenu(self):
        # Add the menu bar
        menu = self.menuBar()
        menu.setNativeMenuBar(False) # Disable global menubar on mac

        file_menu = menu.addMenu('Menu')
        file_menu.addAction(self.button_action_home)
        file_menu.addAction(self.button_action_lic_report_bsc)
        file_menu.addAction(self.button_action_lic_report_rnc)
        file_menu.addSeparator()
        # file_menu.addAction(self.button_action_ping_report_rnc)
        # file_menu.addSeparator()
        # file_menu.addAction(self.button_action_sla_report)

        # file_menu = menu.addMenu('Settings')
        file_menu.addAction(self.button_action_settings)

    def setupLeftwing(self,db_info):
        self.dbcon = db_info 
        '''
        This (self.dbcon = db_info) is needed since some signalling uses self.db as 
        source of data. During reload of database self.db will not be updated accroding to db_info argument.
        '''
        self.leftwing = Tleftwing()
        self.wings_hlayout.addWidget(self.leftwing)
        

        rn_bsc = db_info.getnodes('BSC','bcf')
        rn_rnc = db_info.getnodes('RNC','wbts')
        rn_mrbts = db_info.getnodes('MRBTS', 'lnbts')

        self.tree_bsc = self.leftwing.tree_bsc
        self.model_bsc = Ttreemodel(rn_bsc)
        self.proxy_model_bsc = TfilterProxyModel()
        self.proxy_model_bsc.setSourceModel(self.model_bsc)
        self.tree_bsc.setModel(self.proxy_model_bsc)
        self.tree_bsc.clicked.connect(lambda x: self.onTreeClicked(x, self.tree_bsc.model()))

        self.tree_rnc = self.leftwing.tree_rnc
        self.model_rnc = Ttreemodel(rn_rnc)
        self.proxy_model_rnc = TfilterProxyModel()
        self.proxy_model_rnc.setSourceModel(self.model_rnc)
        self.tree_rnc.setModel(self.proxy_model_rnc)
        self.tree_rnc.clicked.connect(lambda x: self.onTreeClicked(x, self.tree_rnc.model()))

        self.tree_mrbts = self.leftwing.tree_mrbts
        #self.tree_mrbts.setStyleSheet('background-image:url("vline.png");')
        self.model_mrbts = Ttreemodel(rn_mrbts)
        self.proxy_model_mrbts = QSortFilterProxyModel()
        self.proxy_model_mrbts.setSourceModel(self.model_mrbts)
        self.tree_mrbts.setModel(self.proxy_model_mrbts)

        self.tree_mrbts.clicked.connect(lambda x: self.onTreeClicked(x, self.tree_mrbts.model()))

        ''' Tree MRBTS Context Menu '''
        self.tree_mrbts.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_mrbts.customContextMenuRequested.connect(lambda x: self.onTreeRightClickMenu(x, self.tree_mrbts.currentIndex()))

        self.search_tree = self.leftwing.search_tree
        self.search_tree.textChanged.connect(self.onTreeSearch)
        
        # Dockup self.leftwing

        self.dock_lw = TdockWidget('Leftwing', self.main_widget)
        self.dock_lw.setWidget(self.leftwing)
        #print(self.dock_lw.width(),self.dock_lw.height())
        #self.dock_lw.setMinimumSize(300)
        
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_lw)

    def setupRightwing(self,db_info):
        self.dbcon = db_info
        self.rightwing = TrightWing()
        self.rightwing.setContentsMargins(10,10,10,10)
        self.wings_hlayout.addWidget(self.rightwing)
        """ Table Database View """
        self.search_table = self.rightwing.tableViewDatabase.search_table
        self.search_table.setDragEnabled(True)
        self.sql_query_field = self.rightwing.tableViewDatabase.sql_query_field
        self.combo_choose_table = self.rightwing.tableViewDatabase.combo_choose_table
        self.btn_export_table = self.rightwing.tableViewDatabase.btn_export_table
        self.btn_export_table.clicked.connect(self.export_table)
        self.btn_export_db = self.rightwing.tableViewDatabase.btn_export_db
        self.btn_export_db.clicked.connect(self.rotate_table)

        self.table = self.rightwing.tableViewDatabase.table

        self.nodeDetails = self.rightwing.nodeDetialsUI

        self.search_table.textChanged.connect(self.onTableSearch)
        self.sql_query_field.returnPressed.connect(
            lambda x=self.sql_query_field.text(): self.onExecuteSQL(self.sql_query_field.text()))

        ''' Load combobox items using sqlite database table's name '''
        self.db_tables = []
        # self.dbcon = ConnectDB(os.getcwd() + '\\..\\db\\sran.sqlite')
        combo_itmes = db_info.getDataFromQuery('SELECT name FROM sqlite_master '
                                             'WHERE type="table" ORDER BY name;')[0]

        [self.db_tables.append(i[0]) for i in combo_itmes]
        self.combo_choose_table.addItems(self.db_tables)
        self.combo_choose_table.currentIndexChanged.connect(self.onComboItemSelected)

        ''' Load rightwing's table with data from a table '''
        data = db_info.getdata('name,mrbts,btsname,plmn', 'mrbts', None)
        #print(data)
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
            #self.table_proxy_model.setFilterKeyColumn(-1)

        self.compare_button = self.rightwing.nodeDetialsUI.compare_widget.btn_compare   #compareUI.btn_compare
        self.compare_button_cycle = cycle(['off','on'])
        self.compare_button.clicked.connect(self.onCompareButtonClicked)

        # BTN Clicks

        self.rightwing.settingsUI.btn_save.clicked.connect(self.onBtnSaveSettingClicked)
        self.rightwing.licenseReportUIBsc.btn_run.clicked.connect(lambda x='BSC': self.onBtnLicReportClicked('BSC'))
        self.rightwing.licenseReportUIBsc.btn_lic_parse.clicked.connect(lambda x='BSC': self.onBtnLicParseClicked('BSC'))

        self.rightwing.licenseReportUIRnc.btn_run.clicked.connect(lambda x='RNC': self.onBtnLicReportClicked('RNC'))
        self.rightwing.licenseReportUIRnc.btn_lic_parse.clicked.connect(lambda x='RNC': self.onBtnLicParseClicked('RNC'))


        self.rightwing.tableViewDatabase.status_label.setText(str(self.table.model().rowCount())+' X '+str(self.table.model().columnCount())+' Table     ')
        
        self.rightwing.parseUI.btn_file_open.clicked.connect(lambda x='browse': self.onBtnFileBrowseClicked('browse'))
        self.rightwing.parseUI.btn_run.clicked.connect(lambda x='parse': self.onBtnFileBrowseClicked('parse'))
        
        self.rightwing.parseUI.c1.clicked.connect(self.onMultiParseChecked)


        self.rightwing.xmlplanMaker.btn_file_open.clicked.connect(lambda x='browsePlan': self.onBtnFileBrowseClicked('browsePlan'))
        self.rightwing.xmlplanMaker.btn_run.clicked.connect(lambda x='make_plan': self.onBtnFileBrowseClicked('make_plan'))
        
        
        self.rightwing.parameterAudit.btn_file_open.clicked.connect(lambda  x='browseAuditProfile': self.onBtnFileBrowseClicked('browseAuditProfile'))
        self.rightwing.parameterAudit.btn_run.clicked.connect(lambda x="audit": self.onBtnFileBrowseClicked('audit'))

        # Dockup rightwing

        # self.dock_rw = TdockWidget('RightWing',self.main_widget)
        
        # self.dock_rw.setWidget(self.rightwing)
        # self.addDockWidget(Qt.RightDockWidgetArea,self.dock_rw)

    '''
    SLOTS for all SIGNALS emitted from components of MainWindow class
    '''

    def rotate_table(self):
        pass
    
    def export_table(self):
        st = time.ctime()
        #self.table.
        import pandas as pd

        excel_file_name = self.setSaveFileName()


        model = self.table.model()
        headers = []
        # for(int i = 0; i < myTableView->model()->columnCount(); i++)
        # {
        #     headers.append(myTableView->model()->headerData(i, Qt::Horizontal).toString());
        # }

        for i in range(model.columnCount()):
            headers.append(str(model.headerData(i,Qt.Horizontal)))

        data = list()
        #data.append(headers)
        cnt = 0
        for row in range(model.rowCount()):
            data.append([])
            cnt+=1
            for column in range(model.columnCount()):
                index = model.index(row, column)
                # We suppose data are strings
                data[row].append(model.data(index))

        df1 = pd.DataFrame(data,columns=headers)
        df1.to_excel(excel_file_name,sheet_name='Sheet_name_1')
        # cnt = 0
        # wb = xlsxwriter.Workbook(excel_file_name)
        # ws = wb.add_worksheet('SlickData')
        # for row in data:
        #     cnt+=1
        #     print(cnt)
        #     for d in row:
        #         ws.write(data.index(row),row.index(d),d)
        # wb.close()
        #print(str(st)+'\n'+str(time.ctime()))
        QMessageBox.information(self,
                "Slick Info", "Voila! Exported Successfully!")

    def setSaveFileName(self):
        options = QFileDialog.Options()
        # if not self.native.isChecked():
        #     options |= QFileDialog.DontUseNativeDialog
        fileName, filtr = QFileDialog.getSaveFileName(self,
                "QFileDialog.getSaveFileName()",'',
                "Text Files (*.xlsx)", "", options)
        if fileName:
            return fileName

    def onCompareButtonClicked(self, s):
        self.table_info = tuple()
        btn_state = next(self.compare_button_cycle)
        name1 = self.rightwing.nodeDetialsUI.compare_widget.labelA.text() #compareUI.labelA.text()
        name2 = self.rightwing.nodeDetialsUI.compare_widget.labelB.text() #compareUI.labelB.text()

        cbox_match = self.rightwing.nodeDetialsUI.compare_widget.cbox_match #compareUI.cbox_match
        cbox_unmatch = self.rightwing.nodeDetialsUI.compare_widget.cbox_unmatch #compareUI.cbox_unmatch
        cbox_all = self.rightwing.nodeDetialsUI.compare_widget.cbox_all #compareUI.cbox_all



        if btn_state == 'on':
            self.rightwing.nodeDetialsUI.compare_widget.search_comp_table.setVisible(False)
            self.rightwing.nodeDetialsUI.compare_widget.btn_refresh.setVisible(True)
            self.rightwing.nodeDetialsUI.compare_widget.compare_slayout.setCurrentIndex(0)
            self.rightwing.nodeDetialsUI.compare_widget.btn_compare.setText('Compare')
        else:
            self.rightwing.nodeDetialsUI.compare_widget.search_comp_table.setVisible(True)
            self.rightwing.nodeDetialsUI.compare_widget.btn_refresh.setVisible(False)
            self.rightwing.nodeDetialsUI.compare_widget.btn_compare.setText('Back')
            self.cmp_table = self.rightwing.nodeDetialsUI.compare_widget.comp_table
            #print(name1,name2)
            table_name1 = name1.split('/')[-1].split('-')[0]
            table_name2 = name2.split('/')[-1].split('-')[0]
            if table_name1 == table_name2 :
                table_info = comp.compare(table_name1, name1, name2)
                header =  table_info[0]
                table_data = table_info[1]+table_info[2]
                cbox_all.setChecked(True)
                compare_table_model = TtablemodelCompare(table_data, header)
                self.comp_table_proxy_model = QSortFilterProxyModel()
                self.comp_table_proxy_model.setSourceModel(compare_table_model)
                self.comp_table_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
                self.cmp_table.setModel(self.comp_table_proxy_model)
                self.comp_table_proxy_model.setFilterKeyColumn(-1)



                cbox_match.clicked.connect(lambda x: self.onCompareCheckBoxChecked('matched',table_info[1],header))
                cbox_unmatch.clicked.connect(lambda x: self.onCompareCheckBoxChecked('unmatched',table_info[2],header))
                cbox_all.clicked.connect(lambda x: self.onCompareCheckBoxChecked('all',table_data,header))
                self.rightwing.nodeDetialsUI.compare_widget.search_comp_table.textChanged.connect(self.search_comp_table)
            else:
                pass
                #print("Invalid Compare")
            self.rightwing.nodeDetialsUI.compare_widget.compare_slayout.setCurrentIndex(1)

        # self.rightwing.compareUI.lable_vs.setText('Compare')
        # hlayout = self.rightwing.compareUI.labelA.layout()

    def search_comp_table(self, s):
        #print(s)
        self.comp_table_proxy_model.setFilterRegExp(s)

    def onCompareCheckBoxChecked(self, cbox, data, header):
        #print(cbox)
        #print(data)
        model = TtablemodelCompare(data, header)
        self.comp_table_proxy_model = QSortFilterProxyModel()
        self.comp_table_proxy_model.setSourceModel(model)
        self.comp_table_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.cmp_table.setModel(self.comp_table_proxy_model)
        self.comp_table_proxy_model.setFilterKeyColumn(-1)

    def onTreeSearch(self, s):
        self.proxy_model_bsc.setFilterRegExp(s)
        self.proxy_model_rnc.setFilterRegExp(s)
        self.proxy_model_mrbts.setFilterRegExp(s)


    def onTreeClicked(self, index, model):
        print ("#"*100)
        sourceindex = model.mapToSource(index)
        self.nodeDetails.proxy_model_parameter.setSourceModel(None)
        plmn = sourceindex.internalPointer().plmnInfo()
        data = self.dbcon.getproperties(plmn)
        table = self.rightwing.nodeDetialsUI.parameterTree
        proxy_model = self.rightwing.nodeDetialsUI.proxy_model_parameter
        parameterRoot = Node('Parameter','p')
        for key,val in data.items():

            Node(key,val.upper() if val is not None else val, parameterRoot)

        model = TparameterTreeModel(parameterRoot)
        proxy_model.setSourceModel(model)
        table.setModel(proxy_model)


        rn = self.dbcon.getnodesAll(plmn)
        if rn:
            self.nodeDetails.treeHierarchyModel = TSingleTreeModel(rn)
            self.nodeDetails.prxy = QSortFilterProxyModel()
            self.nodeDetails.prxy.setSourceModel(self.nodeDetails.treeHierarchyModel)
            self.nodeDetails.moTree.setModel(self.nodeDetails.prxy)
            self.nodeDetails.moTree.expandAll()
            #self.nodeDetails.slayout.addWidget(self.nodeDetails.moTree)
            #self.nodeDetails.treecontainer.setStyleSheet('')
            self.nodeDetails.moTree.clicked.connect(self.nodeDetails.getNodeParameters)
        else:
            #self.nodeDetails.treecontainer.setStyleSheet('')
            self.nodeDetails.prxy.setSourceModel(None)

        self.rightwing.layout.setCurrentIndex(3)

    ''' Context Menu '''
    def onTreeRightClickMenu(self, position, proxyindex):

        indexes = self.tree_mrbts.selectedIndexes()
        source_index = self.proxy_model_mrbts.mapToSource(proxyindex)

        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        menu = QMenu()
        if level == 0:
            a = menu.addAction(self.tr("Connect SBTS"))
            a.triggered.connect(lambda x: self.onMenuItemSelected('connect', source_index))
            b = menu.addAction(self.tr('Get Details'))
            b.triggered.connect(lambda x: self.onMenuItemSelected('detail', source_index))
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

    def onMenuItemSelected(self, selected, source_index):

        if selected == 'connect':
            # self.dbcon = ConnectDB(os.getcwd()+'\\..\\db\\sran.sqlite')
            # data = self.dbcon.getdata('ip','sranvlan','userlabel="oam" and mrbts='+info.split('-')[-1])[0][0]
            # print(info)
            pass

        elif selected == 'detail':
            self.nodeDetails.proxy_model_parameter.setSourceModel(None)
            plmn = source_index.internalPointer().plmnInfo()
            rn = self.dbcon.getnodesAll(plmn)
            # self.proxy_model_parameter.setSourceModel(None)
            # droppedText = event.mimeData().text().strip()
            # self.dbcon = ConnectDB(os.getcwd() + '\\resources\\db\\sran.sqlite')

            if rn:
                self.nodeDetails.treeHierarchyModel = Ttreemodel(rn)
                self.nodeDetails.prxy = QSortFilterProxyModel()
                self.nodeDetails.prxy.setSourceModel(self.nodeDetails.treeHierarchyModel)
                self.nodeDetails.moTree.setModel(self.nodeDetails.prxy)
                self.nodeDetails.moTree.expandAll()
                self.nodeDetails.slayout.addWidget(self.nodeDetails.moTree)
                self.nodeDetails.treecontainer.setStyleSheet('')
                self.nodeDetails.moTree.clicked.connect(self.nodeDetails.getNodeParameters)
            else:
                self.nodeDetails.treecontainer.setStyleSheet('')
                self.nodeDetails.proxy_model_parameter.setSourceModel(None)

            self.rightwing.layout.setCurrentIndex(3)

    ''' Right Wing Signals '''
    def onComboItemSelected(self, comboindex):
        tablename = self.db_tables[comboindex]
        self.combo_choose_table.currentIndex()
        data = self.dbcon.getdata('*', tablename, None)
        self.cmodel(data)
        #self.table.resizeColumnsToContents()
        self.sql_query_field.selectAll()

        self.rightwing.tableViewDatabase.status_label.setText(str(self.table.model().rowCount())+' X '+str(self.table.model().columnCount())+' Table     ')

    def onTableSearch(self, s):
        self.table_proxy_model.setFilterRegExp(s)
        self.rightwing.tableViewDatabase.status_label.setText(str(self.table.model().rowCount())+' X '+str(self.table.model().columnCount())+' Table     ')

    def onExecuteSQL(self, q):
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
        self.rightwing.tableViewDatabase.status_label.setText(str(self.table.model().rowCount())+' X '+str(self.table.model().columnCount())+' Table     ')

    def warning(self, text, title):
        QMessageBox.critical(self, title, text)

    def onMultiParseChecked(self,s):

        if s:
            self.rightwing.parseUI.edit_raw_xml_db_dir.setEnabled(True)
            self.rightwing.parseUI.edit_raw_xml_db_pattrn.setEnabled(True)

        else:
            self.rightwing.parseUI.edit_raw_xml_db_dir.setEnabled(False)
            self.rightwing.parseUI.edit_raw_xml_db_pattrn.setEnabled(False)

    ''' Action button slots to switch widgets on rightwing '''

    def onMyButtonActionClicked(self, s):
        if s == 'btn_home':
            self.rightwing.layout.setCurrentIndex(0)
            # self.rightwing.licenseReportUIBsc.setVisible(False)
            # self.rightwing.licenseReportUIRnc.setVisible(False)
            # self.rightwing.tableViewDatabase.setVisible(True)
            # self.rightwing.settingsUI.setVisible(False)
        if s == 'btn_bsc_lic_report':
            self.rightwing.layout.setCurrentIndex(1)
            # self.rightwing.licenseReportUIBsc.setVisible(True)
            # self.rightwing.licenseReportUIRnc.setVisible(False)
            # self.rightwing.tableViewDatabase.setVisible(False)
            # self.rightwing.settingsUI.setVisible(False)
        if s == 'btn_rnc_lic_report':
            self.rightwing.layout.setCurrentIndex(2)
            # self.rightwing.licenseReportUIBsc.setVisible(False)
            # self.rightwing.licenseReportUIRnc.setVisible(True)
            # self.rightwing.tableViewDatabase.setVisible(False)
            # self.rightwing.settingsUI.setVisible(False)

        if s == 'node_details':
            self.rightwing.layout.setCurrentIndex(3)


        if s == 'btn_settings':
            self.rightwing.layout.setCurrentIndex(4)
            # self.rightwing.settingsUI.setVisible(True)
            # self.rightwing.licenseReportUIBsc.setVisible(False)
            # self.rightwing.licenseReportUIRnc.setVisible(False)
            # self.rightwing.tableViewDatabase.setVisible(False)


        if s == 'btn_parse':
            self.rightwing.layout.setCurrentIndex(7)

        if s == 'btn_xmlplan':
            self.rightwing.layout.setCurrentIndex(8)

        if s == 'btn_audit':
            self.rightwing.layout.setCurrentIndex(9)

        if s == 'btn_reload':
            print("Reload clicked")
            db_filename = QFileDialog.getOpenFileName(self, "Browse Sqlite database", os.getcwd(),"All Files (*)")
            print(db_filename)
            if db_filename[0]:
                try:
                    self.reloadUI(db_filename[0])
                except TypeError:
                    pass
            else:
                print('O la la! Nothing Selected!')
        if s == 'btn_compare':
            self.rightwing.layout.setCurrentIndex(5)

        if s == 'btn_qr':
            self.rightwing.layout.setCurrentIndex(6)

        if s == 'btn_log':
            QFileDialog.getOpenFileName('C:\\')

    def onBtnSaveSettingClicked(self):
        self.connections = self.rightwing.settingsUI.read_config_file()
        new_entries = []
        fp_prev = open(os.getcwd() + '\\resources\\config\\config.csv', "r")
        table_prev = fp_prev.readlines()
        fp = open(os.getcwd() + '\\resources\\config\\config.csv', "w+")
        csv_line = str()
        for h in self.connections[1]:
            csv_line += h + ','
        fp.write(csv_line[:-1] + '\n')
        for row in range(self.rightwing.settingsUI.table.rowCount()):
            csv_line = str()
            for col in range(self.rightwing.settingsUI.table.columnCount()):
                item = self.rightwing.settingsUI.table.item(row, col)
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
                r = QCheckBox(self.rightwing.licenseReportUIBsc.nodeListGroupBox)
                r.setText(d['Name'])
                self.rightwing.licenseReportUIBsc.x.append(r)
                self.rightwing.licenseReportUIBsc.vlayout.addWidget(r)

            if d['Group'] == 'RNC':
                r = QCheckBox(self.rightwing.licenseReportUIRnc.nodeListGroupBox)
                r.setText(d['Name'])
                self.rightwing.licenseReportUIRnc.x.append(r)
                self.rightwing.licenseReportUIRnc.vlayout.addWidget(r)

        QMessageBox.information(self,'Settings Table','Saved!')

    # Collect Log button slot on license report ui
    def onBtnLicReportClicked(self, s):
        self.connections = self.rightwing.settingsUI.read_config_file()

        get_connection_info = []

        if s == 'BSC':
            self.rightwing.licenseReportUIBsc.progressbar.show()
            #self.rightwing.licenseReportUIBsc.progressbar.show()

            for i in self.rightwing.licenseReportUIBsc.x:

                if i.isChecked():
                    get_connection_info.append(i.text())

            connection_info_details = self.rightwing.settingsUI.get_details_from_name(get_connection_info, self.connections[0])

            ssh = SlickSSH(connection_info_details, '\r', ['ZW7I:LIC,FULL;',
                                                           'ZW7I:FEA,FULL:FSTATE=ON;',
                                                           'ZW7I:FEA,FULL:FSTATE=OFF;',
                                                           'ZW7I:UCAP,FULL;'])

            # ssh = SlickSSH(connection_info_details,'\r', ['cd virtualenvironment/py3env/bin/',
            #                                               'cd xmlparser',
            #                                               'ls -ltr'
            #                                          ])

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
            connection_info_details = self.rightwing.settingsUI.get_details_from_name(get_connection_info, self.connections[0])
            ssh2 = SlickSSH(connection_info_details, '\n', ['fsclish -c "show license all"'])
            #ssh2 = SlickSSH(connection_info_details, '\n', ['pwd','ls -ltr'])
            rnc_worker = MyWorker(ssh2.execute_cmd,) #self.rightwing.licenseReportUIRnc.tv)
            rnc_worker.signals.update.connect(self.update_tv2)
            rnc_worker.signals.progress.connect(self.progress2)
            self.threadpool.start(rnc_worker)

    # Parse license button slot on license report ui
    def onBtnLicParseClicked(self, s):
        # print ('-'*80+' Enter Click')

        if s == 'BSC':
            self.rightwing.licenseReportUIBsc.progressbar.show()
        if s == 'RNC':
            self.rightwing.licenseReportUIRnc.progressbar.show()
        # print('-' * 80 + ' Show Progressbar')
        options = QFileDialog.Options()
        files, filtr = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", self.openfilespath,
                                                    "All Files (*);;Text Files (*.txt)", "", options)
        self.input_files_dict = {}
        # print('-' * 80 + ' Open Diag')
        if files:
            for f in files:
                if (f.split('/')[-1]).lower().find('bsc') >= 0:
                    self.input_files_dict['lic_bsc_log'] = f
                if (f.split('/')[-1]).lower().find('rnc') >= 0:
                    self.input_files_dict['lic_rnc_log'] = f

        if self.input_files_dict:
            if s == 'BSC':
                lic_parse_worker = MyWorker(self.license_parser)
                lic_parse_worker.signals.update.connect(self.update_tv)
                lic_parse_worker.signals.progress.connect(self.progress)
                lic_parse_worker.signals.finished.connect(self.finish)
                # print('-' * 80 + ' Thread done')
                # lic_parse_worker.signals.error.connect(self.error)
            if s == 'RNC':
                lic_parse_worker = MyWorker(self.license_parser)
                lic_parse_worker.signals.update.connect(self.update_tv2)
                lic_parse_worker.signals.progress.connect(self.progress2)
                lic_parse_worker.signals.finished.connect(self.finish2)
                # lic_parse_worker.signals.error.connect(self.error2)
            self.threadpool.start(lic_parse_worker)
            # print('-' * 80 + ' TP Start')

    def onBtnFileBrowseClicked(self,s):
        if s == 'browse':
            self.filename = QFileDialog.getOpenFileName(self, "Open File", "C:\\","All Files (*)")
            self.rightwing.parseUI.lineEdit_file_open.setText(self.filename[0])
            self.rightwing.parseUI.btn_run.setEnabled(True)
            self.rightwing.parseUI.edit_base_dir.setText(os.path.dirname(self.filename[0]))

        if s == 'browsePlan':
            self.inputfilename = QFileDialog.getOpenFileName(self, "Open File", "C:\\","All Files (*)")
            self.rightwing.xmlplanMaker.lineEdit_file_open.setText(self.inputfilename[0])
            self.rightwing.xmlplanMaker.btn_run.setEnabled(True)
            #self.rightwing.xmlplanMaker.edit_base_dir.setText(os.path.dirname(self.filename[0]))

        if s == 'browseAuditProfile':
            self.inputAudit = QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "All Files (*)")
            self.rightwing.parameterAudit.lineEdit_file_open.setText(self.inputAudit[0])
            self.rightwing.parameterAudit.btn_run.setEnabled(True)
            print('Kindly do the audit '+self.inputAudit[0])

        if s == 'audit':
            objectname = 'Parameter'

            input = Read_XL(self.rightwing.parameterAudit.lineEdit_file_open.text().strip(), objectname)
            input_data = input.read_excel()[1]
            parametername = []
            plannedvalue = []
            objectname = []
            print (input_data)
            for i in input_data:
                objectname.append(i[0])
                parametername.append(i[1])
                if str(i[-1]):
                    if len(str(i[-1]).split('.')) > 2:
                        plannedvalue.append(str(i[-1]))
                    else:
                        plannedvalue.append(str(i[-1]).split('.')[0])
            print (objectname)
            print (parametername)
            print (plannedvalue)
            objectDictionary = {}

            for i in objectname:
                if i not in objectDictionary.keys():
                    p = []
                    v = []
                    index = 0
                    for j in objectname:
                        if j==i:
                            p.append(parametername[index])
                            v.append(plannedvalue[index])
                        index+=1
                    objectDictionary[i] = dict(zip(p, v))



            #dbOpeartions = DBCheck('10.10.9.150','tapon','tapon12345','huawei')
            dbOpeartions = DBCheckSqlite(r'C:\Python36\Scripts\python3env\Scripts\MyQt5\Slick\resources\db\parsed_sbts.sqlite')

           

            abc = MakeExcelFile( '/'.join(self.rightwing.parameterAudit.lineEdit_file_open.text().strip().split('/')[:-1])+'/audit.xlsx')

            for key,val in objectDictionary.items():
                dbfeedback = dbOpeartions.get_result(key, val)
                abc.createsheet(key,dbfeedback)

            abc.close()


        if s ==  'parse':
            self.rightwing.parseUI.progressbar.hide()
            self.rightwing.parseUI.progress_label.hide()
            base_path = self.rightwing.parseUI.edit_base_dir.text()
            abs_path = self.rightwing.parseUI.edit_abs_path.text()
            mobj = self.rightwing.parseUI.edit_mo_name.text()
            size = int(self.rightwing.parseUI.edit_mo_chunk_size.text())
            src = self.filename[0].split('/')[-1]
            db_name = self.rightwing.parseUI.edit_db_name.text()
            mo_list_filter = self.rightwing.parseUI.edit_mo_class.toPlainText().strip().split(',')
            is_dir_parse = self.rightwing.parseUI.c1.isChecked()
            raw_xml_db_dir = self.rightwing.parseUI.edit_raw_xml_db_dir.text()
            prepare = Prepare(base_path,abs_path,src,mobj,size,mo_list_filter,db_name,is_dir_parse,raw_xml_db_dir)

            xml_parse_worker = ParseWorker(prepare.xml_mo_chunker)
            xml_parse_worker.signals.update.connect(self.update_output)
            xml_parse_worker.signals.progress.connect(self.update_pg)
            xml_parse_worker.signals.finished.connect(self.unhide_pg)
            self.threadpool.start(xml_parse_worker)

        if s== 'make_plan':
            print('Plan need to create ')
            inp = ReadInput(self.inputfilename,1)
            input_info = inp.get_param_names()
            self.rightwing.xmlplanMaker.lbl_xml_inputobjects.setText("ManagedObjects: "+str(input_info[0][0])+" | Parameters: "+str(input_info[1][0])+" | Total: "+str(len(input_info[1])))
            xmlplan_worker = ParseWorker(inp.create_plan)
            xmlplan_worker.signals.update.connect(self.update_xmlplan_output)
            self.threadpool.start(xmlplan_worker)



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

    def update_output(self,s):
        self.rightwing.parseUI.output.setText(s)

    def update_xmlplan_output(self,s):
        self.rightwing.xmlplanMaker.output.setText(s)

    def update_pg(self,s):
        self.rightwing.parseUI.progressbar.setValue(s)

    def unhide_pg(self):
        self.rightwing.parseUI.progressbar.show()
        self.rightwing.parseUI.progress_label.show()

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
        self.rightwing.licenseReportUIRnc.tv.append(s)
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
    # import pyqtcss
    import os
    import sys
    # pyqtcss.available_styles()
    # ['classic', 'dark_blue', 'dark_orange']

    # style_string = pyqtcss.get_style('classic')
    #print(os.getcwd())
    
    app = QApplication(sys.argv)
    app_icon = QIcon(os.getcwd()+'\\resources\\img\\icons\\slick.svg')
    app.setWindowIcon(app_icon)


    window = MainWindow()
    style = """
    QWidget{
    font-family:Consolas,Courier;
    }
    """
    #app.setStyleSheet(qdarkstyle.load_stylesheet())
    # app.setStyleSheet(style_string)
    #app.setStyleSheet(style)
    #app.setStyleSheet(qss_file)
    window.show()
    sys.exit(app.exec_())