from models.models import *
from twidgets.components import MyTextEdit
from tdbopeations.dbops import *
from twidgets.components import *

from twidgets.treeview import *
from twidgets.compare import *
from twidgets.dbtable import *
from PyQt5.QtCore import *
import qrcode
import os, time
import hashlib




class ParseWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super(ParseWidget,self).__init__(*args,**kwargs)
        self.setContentsMargins(0,0,0,0)
        style = """
        QTextEdit{
        font-family:Consolas,Courier;
        color:#555500;
        }
        """
        mainLayout = QVBoxLayout()
        toplayout = QHBoxLayout()
        
        self.setLayout(mainLayout)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        parser_setting_gbox = QGroupBox(self)
        parser_setting_gbox.setTitle("Parser Settings")
        self.leftbox = QWidget()
        
   
        # self.rightbox = QWidget()
        # #self.rightbox.setStyleSheet('background-color:orange;')

        leftboxLayout = QVBoxLayout(parser_setting_gbox)
        
        
        # #self.leftbox.setLayout(leftboxLayout)
        
        # #leftboxLayout.setContentsMargins(0,0,0,0)

        
        # self.rightbox.setLayout(rightboxLayout)

        askOpenWidget = QWidget(parser_setting_gbox)
        askOpenLayout = QHBoxLayout()
        self.btn_file_open = QPushButton("Browse")
        self.lineEdit_file_open = QLineEdit()
        #self.lineEdit_file_open.setFixedHeight(32)
        self.btn_run = QPushButton("Run")
        self.btn_run.setEnabled(False)
        askOpenLayout.addWidget(self.lineEdit_file_open)
        askOpenLayout.addWidget(self.btn_file_open)
        askOpenLayout.addWidget(self.btn_run)
        askOpenLayout.setContentsMargins(0,0,0,0)
        #askOpenWidget.setContentsMargins(0,0,0,0)
        askOpenWidget.setLayout(askOpenLayout)
     
        

        parseSettingWidget = QWidget(parser_setting_gbox)
        parseSettingLayout = QGridLayout()
        parseSettingWidget.setLayout(parseSettingLayout)
        parseSettingLayout.setSpacing(20)

        label_mo_chunk_size = QLabel('MO Chunk Size')
        self.edit_mo_chunk_size = QLineEdit('100')
      

        label_mo_name = QLabel('MO Name')
        self.edit_mo_name = QLineEdit('managedObject')
       

        label_mo_class = QLabel('MO Classes')
        self.edit_mo_class = QTextEdit("BSC,BCF,BTS,TRX,LAPD,RNC,WBTS,WCEL,IPNB,MRBTS,LNBTS,LNCEL")
      


        label_abs_path = QLabel('Absolute Path')
        self.edit_abs_path = QLineEdit('ToBeParsed')
        

        label_base_dir = QLabel('Base Directory')
        self.edit_base_dir = QLineEdit(os.path.dirname(os.path.abspath(__file__)))



        label_db_name = QLabel('DB NAME PREFIX')
        self.edit_db_name = QLineEdit('parsed_')


        label_is_directory_parse = QLabel('Multi Parse')
        self.c1 = QCheckBox()
        self.c1.setText('True')

        label_raw_xml_db_dir = QLabel('Raw XML DB DIR')
        self.edit_raw_xml_db_dir = QLineEdit('RawDB')

        label_raw_xml_db_pattrn = QLabel('RAW XML DB pattern')
        self.edit_raw_xml_db_pattrn = QLineEdit('.xml.gz')


        label_is_zip_db = QLabel('IS ZIP DB?')
        combo_is_zip_db = QComboBox()

        label_is_weekly_backup = QLabel('IS WEEKLY BACKUP?')
        combo_is_weekly_backup = QComboBox()
       
        parseSettingLayout.addWidget(label_mo_chunk_size,1,0)
        parseSettingLayout.addWidget(self.edit_mo_chunk_size,1,1)

        parseSettingLayout.addWidget(label_mo_name,2,0)
        parseSettingLayout.addWidget(self.edit_mo_name,2,1)

        parseSettingLayout.addWidget(label_mo_class,3,0)
        parseSettingLayout.addWidget(self.edit_mo_class,3,1)

        parseSettingLayout.addWidget(label_db_name,4,0)
        parseSettingLayout.addWidget(self.edit_db_name,4,1)
        
        parseSettingLayout.addWidget(label_abs_path,5,0)
        parseSettingLayout.addWidget(self.edit_abs_path,5,1)


        parseSettingLayout.addWidget(label_base_dir,6,0)
        parseSettingLayout.addWidget(self.edit_base_dir,6,1)

        parseSettingLayout.addWidget(label_is_directory_parse,7,0)
        parseSettingLayout.addWidget(self.c1,7,1)

        parseSettingLayout.addWidget(label_raw_xml_db_dir,8,0)
        parseSettingLayout.addWidget(self.edit_raw_xml_db_dir,8,1)

        parseSettingLayout.addWidget(label_raw_xml_db_pattrn,9,0)
        parseSettingLayout.addWidget(self.edit_raw_xml_db_pattrn,9,1)

        parseSettingLayout.addWidget(label_is_zip_db,10,0)
        parseSettingLayout.addWidget(combo_is_zip_db,10,1)

        parseSettingLayout.addWidget(label_is_weekly_backup,11,0)
        parseSettingLayout.addWidget(combo_is_weekly_backup,11,1)

        self.edit_raw_xml_db_dir.setEnabled(False)
        self.edit_raw_xml_db_pattrn.setEnabled(False)

        
        # leftboxLayout.addWidget(parser_setting_gbox)
        leftboxLayout.addWidget(askOpenWidget)
        # leftboxLayout.addStretch(1)
        leftboxLayout.addWidget(parseSettingWidget)
        


        output_gbox = QGroupBox(self)
        output_gbox.setTitle('Output')
       
        rightboxLayout = QVBoxLayout(output_gbox)

        self.output = QTextEdit()
        rightboxLayout.setContentsMargins(0,0,0,0)
        rightboxLayout.addWidget(self.output)
        self.output.setStyleSheet("border:none;")
        
        progress_layout = QHBoxLayout()

        self.progress_label = QLabel('Progress')
        self.progressbar = QProgressBar()
        
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progressbar)
    
        rightboxLayout.addLayout(progress_layout)

        self.progressbar.hide()
        self.progress_label.hide()
        toplayout.addWidget(parser_setting_gbox)

        toplayout.addWidget(output_gbox)
        mainLayout.addLayout(toplayout)
        
class XMLPlanMaker(QWidget):
    def __init__(self,*args,**kwargs):
        super(XMLPlanMaker,self).__init__(*args,**kwargs)
        self.setContentsMargins(0,0,0,0)
    

        mainLayout = QVBoxLayout()
        toplayout = QVBoxLayout()
        
        self.setLayout(mainLayout)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        xmlplan_maker_gbox = QGroupBox(self)
        xmlplan_maker_gbox.setTitle("XML Plan Maker")
        self.leftbox = QWidget()

        leftboxLayout = QVBoxLayout(xmlplan_maker_gbox)
    
        askOpenWidget = QWidget(xmlplan_maker_gbox)
        askOpenLayout = QHBoxLayout()
        self.btn_file_open = QPushButton("Browse")
        self.lineEdit_file_open = QLineEdit()
        self.btn_run = QPushButton("Make Plan")
        self.btn_run.setEnabled(False)
        self.lbl_xml_inputobjects = QLabel()
        askOpenLayout.addWidget(self.lineEdit_file_open)
        askOpenLayout.addWidget(self.btn_file_open)
        askOpenLayout.addWidget(self.btn_run)
        askOpenLayout.setContentsMargins(0,0,0,0)
        askOpenWidget.setLayout(askOpenLayout)
        leftboxLayout.addWidget(askOpenWidget)
        leftboxLayout.addWidget(self.lbl_xml_inputobjects)
        output_gbox = QGroupBox(self)
        output_gbox.setTitle('Plan Output')
       
        rightboxLayout = QVBoxLayout(output_gbox)

        self.output = MyTextEdit()

        style = """
        QTextEdit{
        font-family:Consolas,Courier;
        color:#555500;
        }
        """

        self.output.setStyleSheet(style)
        #self.output.setAcceptRichText(True)
        rightboxLayout.setContentsMargins(0,0,0,0)
        rightboxLayout.addWidget(self.output)
        self.output.setStyleSheet("border:none;")
        
        progress_layout = QHBoxLayout()

        self.progress_label = QLabel('Progress')
        self.progressbar = QProgressBar()
        
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progressbar)
    
        rightboxLayout.addLayout(progress_layout)

        self.progressbar.hide()
        self.progress_label.hide()
        toplayout.addWidget(xmlplan_maker_gbox)

        toplayout.addWidget(output_gbox)
        mainLayout.addLayout(toplayout)

class ParameterAudit(QWidget):
    def __init__(self,*args,**kwargs):
        super(ParameterAudit,self).__init__(*args,**kwargs)

        self.setContentsMargins(0,0,0,0)
    

        mainLayout = QVBoxLayout()
        toplayout = QVBoxLayout()
        
        self.setLayout(mainLayout)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        xmlplan_maker_gbox = QGroupBox(self)
        xmlplan_maker_gbox.setTitle("Parameter Audit")
        self.leftbox = QWidget()

        leftboxLayout = QVBoxLayout(xmlplan_maker_gbox)
    
        askOpenWidget = QWidget(xmlplan_maker_gbox)
        askOpenLayout = QHBoxLayout()
        self.btn_file_open = QPushButton("Browse")
        self.lineEdit_file_open = QLineEdit()
        self.btn_run = QPushButton("Audit")
        self.btn_run.setEnabled(False)
        self.lbl_xml_inputobjects = QLabel()
        askOpenLayout.addWidget(self.lineEdit_file_open)
        askOpenLayout.addWidget(self.btn_file_open)
        askOpenLayout.addWidget(self.btn_run)
        askOpenLayout.setContentsMargins(0,0,0,0)
        askOpenWidget.setLayout(askOpenLayout)
        leftboxLayout.addWidget(askOpenWidget)
        leftboxLayout.addWidget(self.lbl_xml_inputobjects)
        output_gbox = QGroupBox(self)
        output_gbox.setTitle('Result')
       
        rightboxLayout = QVBoxLayout(output_gbox)

        self.output = MyTextEdit()
       


        style = """
        QTextEdit{
        font-family:Consolas,Courier;
        color:#555500;
        }
        """

        self.output.setStyleSheet(style)
        #self.output.setAcceptRichText(True)
        rightboxLayout.setContentsMargins(0,0,0,0)
        rightboxLayout.addWidget(self.output)
        self.output.setStyleSheet("border:none;")
        
        progress_layout = QHBoxLayout()

        self.progress_label = QLabel('Progress')
        self.progressbar = QProgressBar()
        
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progressbar)
    
        rightboxLayout.addLayout(progress_layout)

        self.progressbar.hide()
        self.progress_label.hide()
        toplayout.addWidget(xmlplan_maker_gbox)

        toplayout.addWidget(output_gbox)
        mainLayout.addLayout(toplayout)

class QRGeneratorWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super(QRGeneratorWidget, self).__init__(*args,**kwargs) 
        self.cusotomer = {'name':'Slick001', 'id':None}
        if not self.cusotomer['id']:
            data = os.popen('wmic baseboard get product,manufacturer,serialnumber').read()
            dlist = data.split('\n')
            dlist = list(filter(('').__ne__, dlist))
            lic_coded = hashlib.md5('-'.join(dlist[-1].split()).encode())
        else:
            lic_coded = hashlib.md5(self.cusotomer['id'].encode())
            
        self.lic_md5 = lic_coded.hexdigest()
        self.lic_md5 = self.lic_md5 * 3
        layout = QVBoxLayout()
        self.lic_lineedit = QLineEdit()
        self.lic_lineedit.setFixedWidth(450)
        self.label = QLabel()
        pixmap  = qrcode.make(self.lic_md5, image_factory=Image).pixmap()
        self.label.setPixmap(pixmap)
        layout.addWidget(self.lic_lineedit)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignCenter)
        
        self.setLayout(layout)
        
        styles = """
        border: 2px solid red;
        """
        self.setStyleSheet(styles)

        self.lic_lineedit.returnPressed.connect(lambda x=self.lic_lineedit.text(): self.setlic(self.lic_lineedit.text()))


    def setlic(self,in_md5):
        if in_md5 == self.cusotomer['id']:
            print('valid')
        else:
            print('invalid') 

class Image(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size):
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QImage(
            size, size, QImage.Format_RGB16)
        self._image.fill(Qt.white)

    def pixmap(self):
        return QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,Qt.black)

class Tleftwing(QWidget):
    def __init__(self,*args,**kwargs):
        super(Tleftwing, self).__init__(*args, **kwargs)

        #self.setStyleSheet('border: 1px solid green')
        '''Set Main Layout'''
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(10, 10, 10, 10)

        '''Tree onTableSearch field'''
        self.search_tree = QLineEdit()
        self.search_tree.setPlaceholderText('Search for a Node...')

        ''' BSC Tree'''
        self.tree_bsc = Ttreeview()
        # self.tree_bsc.setSelectionMode(self.tree_bsc.SingleSelection)
        self.tree_bsc.setDragDropMode(QAbstractItemView.InternalMove)
        # self.tree_bsc.setDragEnabled(True)
        # self.tree_bsc.setAcceptDrops(True)
        # self.tree_bsc.setDropIndicatorShown(True)

        ''' RNC Tree'''
        self.tree_rnc = Ttreeview()
        # self.tree_rnc.setSelectionMode(self.tree_rnc.SingleSelection)
        self.tree_rnc.setDragDropMode(QAbstractItemView.InternalMove)
        # self.tree_rnc.setDragEnabled(True)
        # self.tree_rnc.setAcceptDrops(True)
        # self.tree_rnc.setDropIndicatorShown(True)


        # sizePolicy = QSizePolicy(QSizePolicy.Expanding,
        #                          QSizePolicy.Expanding)
        #
        # self.tree_rnc.setSizePolicy(sizePolicy)


        ''' MRBTS Tree'''
        self.tree_mrbts = Ttreeview()
        # self.tree_mrbts.setSelectionMode(self.tree_mrbts.SingleSelection)
        self.tree_mrbts.setDragDropMode(QAbstractItemView.InternalMove)
        # self.tree_mrbts.setDragEnabled(True)
        # self.tree_mrbts.setAcceptDrops(True)
        # self.tree_mrbts.setDropIndicatorShown(True)

        ''' Adding all leftwing widgets to layout '''
        layout.addWidget(self.search_tree)
        layout.addWidget(self.tree_mrbts)
        layout.addWidget(self.tree_rnc)
        layout.addWidget(self.tree_bsc)

        ''' Few layout design commands not used '''
        # layout.addStretch()
        # self.setFixedWidth(200)
        # self.setStyleSheet('border:2px solid red;background-color:grey')
        # layout.setSpacing(0)
        # self.setStyleSheet('border-right:2px solid yellow')

class TrightWing(QWidget):
    def __init__(self,*args,**kwargs):
        super(TrightWing, self).__init__(*args, **kwargs)
        
        ''' Layout '''
        self.layout = QStackedLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        ''' Components '''
        self.licenseReportUIBsc = LicenseReport('BSC')
        self.licenseReportUIRnc = LicenseReport('RNC')
        self.tableViewDatabase = TtableDBWidget()
        self.settingsUI = SettingTable()
        self.nodeDetialsUI = TnodeDeatail()
        self.compareUI = CompareWidget()
        self.qrCodegen = QRGeneratorWidget()
        self.parseUI = ParseWidget()
        self.xmlplanMaker = XMLPlanMaker()
        self.parameterAudit = ParameterAudit()

        ''' Add components '''
        self.layout.addWidget(self.tableViewDatabase)
        self.layout.addWidget(self.licenseReportUIBsc)
        self.layout.addWidget(self.licenseReportUIRnc)
        self.layout.addWidget(self.nodeDetialsUI)
        self.layout.addWidget(self.settingsUI)
        self.layout.addWidget(self.compareUI)
        self.layout.addWidget(self.qrCodegen)
        self.layout.addWidget(self.parseUI)
        self.layout.addWidget(self.xmlplanMaker)
        self.layout.addWidget(self.parameterAudit)
        self.layout.setCurrentIndex(9)

class TnodeDeatail(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Main Layout """
        layout = QVBoxLayout()
        self.setLayout(layout)

        search_parameter = QLineEdit()
        search_parameter.setPlaceholderText('Search parameter')
        search_parameter.textChanged.connect(self.searchparameter)

        """ Center Layout """
        moDetailLayout = QHBoxLayout()

        self.parameterTree = Ttreeview()
        '''
        #self.description = QTextEdit()
        #self.treecontainer = DropLabel()
        #self.slayout = QStackedLayout()
        '''

        self.moTree = Ttreeview()
        self.moTree.setSelectionMode(self.moTree.SingleSelection)
        self.moTree.setDragDropMode(QAbstractItemView.InternalMove)
        self.moTree.setDragEnabled(True)
        self.moTree.setAcceptDrops(True)
        self.moTree.setDropIndicatorShown(True)

        self.proxy_model_parameter = QSortFilterProxyModel()
        self.prxy = QSortFilterProxyModel()

        '''
        #self.treecontainer.setLayout(self.slayout)
        #self.treecontainer.setMinimumWidth(500)
        #self.description.setReadOnly(True)

        # self.webEngineView = QWebEngineView()
        # initialUrl = 'http://qt.io'
        # self.webEngineView.load(QUrl(initialUrl))
        # self.webEngineView.page().titleChanged.connect(self.setWindowTitle)
        # self.webEngineView.page().urlChanged.connect(self.urlChanged)
        '''
        moDetailLayout.addWidget(self.moTree)
        moDetailLayout.addWidget(self.parameterTree)
        '''
        #moDetailLayout.addWidget(self.description)
        '''
        self.compare_widget = CompareWidget()

        '''
        a_b_container and container 2 of compare widget was previously on CompareWidget
        But this created a problem of poping up stacked layout during startup.
        To mitigate this issue they are added here.
        '''

        self.compare_widget.compare_slayout.addWidget(self.compare_widget.a_b_container)
        self.compare_widget.compare_slayout.addWidget(self.compare_widget.a_b_result_container)
        layout.addWidget(search_parameter)
        layout.addLayout(moDetailLayout)
        layout.addWidget(self.compare_widget)

    def searchparameter(self, s):
        self.proxy_model_parameter.setFilterRegExp(s)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()
        self.treecontainer.setStyleSheet('border:2px solid blue')

    def dragLeaveEvent(self, QDragLeaveEvent):
        self.treecontainer.setStyleSheet('')

    def dropEvent(self, event):
        self.proxy_model_parameter.setSourceModel(None)
        droppedText = event.mimeData().text().strip()
        self.dbcon = ConnectDB(os.getcwd() + '\\resources\\db\\parsed_sbts.sqlite')

        rn = self.dbcon.getnodesAll(droppedText)
        if rn:
            self.treeHierarchyModel = Ttreemodel(rn)

            self.prxy.setSourceModel(self.treeHierarchyModel)
            self.moTree.setModel(self.prxy)
            self.moTree.expandAll()
            self.slayout.addWidget(self.moTree)
            self.treecontainer.setStyleSheet('')
            self.moTree.clicked.connect(self.getNodeParameters)
        else:
            self.treecontainer.setStyleSheet('')
            self.proxy_model_parameter.setSourceModel(None)

    def getNodeParameters(self, index):
        sourceIndex = self.prxy.mapToSource(index)
        treeDataDict = sourceIndex.internalPointer().getProperties()
        print(treeDataDict)
        parameterRoot = Node('Parameter', 'p')
        for key, val in treeDataDict.items():
            Node(key, val.upper() if val is not None else val, parameterRoot)

        model = TparameterTreeModel(parameterRoot)
        self.proxy_model_parameter.setSourceModel(model)
        self.parameterTree.setModel(self.proxy_model_parameter)

# class DropLabel(QLabel):
#     def __init__(self, *args, **kwargs):
#         super(DropLabel, self).__init__(*args, **kwargs)
#         self.setAcceptDrops(True)

