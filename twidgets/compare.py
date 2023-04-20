from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from tdbopeations.dbops import *
from twidgets.treeview import *
from twidgets.tableview import *
import os



class my_label1(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(my_label1, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        styleshett = """
        font-size:24px;
        text-align:center;
        color: green;
        background-color:#EEFFEE;
        """
        self.dbcon = ConnectDB(os.getcwd() + '\\resources\\db\\parsed_sbts.sqlite')
        self.setStyleSheet(styleshett)

    def dragEnterEvent(self, event):
        stylesheet = """
        border: 2px solid #DCDCDC;
        color: green;
        background-color:#DCFFDC;
        """
        self.setStyleSheet(stylesheet)
        if event.mimeData().hasFormat("text/plain"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        dropped_data = event.mimeData().text()
        # self.setText(event.mimeData().text())
        table = self.parent().parent().parent().comp_tableA
        proxy_model = self.parent().parent().parent().proxy_model_parameter1
        slayout = self.parentWidget().layout()
        slayout.setCurrentIndex(1)
        d = self.dbcon.getproperties(dropped_data)

        parameterRoot = Node('Parameter', 'p')
        for key, val in d.items():
            Node(key, val.upper() if val is not None else val, parameterRoot)

        model_left = TparameterTreeModel(parameterRoot)
        proxy_model.setSourceModel(model_left)
        table.setModel(proxy_model)
        self.setText(dropped_data)


class my_label2(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(my_label2, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        styleshett = """
        font-size:24px;
        text-align:center;
        color: green;
        background-color:#EEEEFF;
        """
        self.dbcon = ConnectDB(os.getcwd() + '\\resources\\db\\parsed_sbts.sqlite')
        self.setStyleSheet(styleshett)

    def dragEnterEvent(self, event):
        styleshett = """
        border: 2px solid #DCDCDC;
        color: green;
        background-color:#DCDCFF;
        """
        self.setStyleSheet(styleshett)
        if event.mimeData().hasFormat("text/plain"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # print()
        dropped_data = event.mimeData().text()
        table = self.parent().parent().parent().comp_tableB
        proxy_model = self.parent().parent().parent().proxy_model_parameter2
        slayout = self.parentWidget().layout()
        slayout.setCurrentIndex(1)
        d = self.dbcon.getproperties(dropped_data)
        parameterRoot = Node('Parameter', 'p')
        for key, val in d.items():
            Node(key, val.upper() if val is not None else val, parameterRoot)

        model_left = TparameterTreeModel(parameterRoot)
        proxy_model.setSourceModel(model_left)
        table.setModel(proxy_model)
        self.setText(dropped_data)

    def dragLeaveEvent(self, event):
        styleshett = """
        border: none;
        color: green;
        background-color:#EEEEFF;
        """
        self.setStyleSheet(styleshett)


class CompareWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(CompareWidget, self).__init__(*args, **kwargs)

        '''Set Main Layout'''

        parentLayout = QVBoxLayout()
        self.setLayout(parentLayout)
        compare_label = QLabel('Comparison A/B')
        compare_label.setAlignment(Qt.AlignCenter)
        parentLayout.addWidget(compare_label)

        self.compare_slayout = QStackedLayout()
        self.a_b_container = QWidget()
        a_b_compare_layout = QHBoxLayout()
        vs_layout = QVBoxLayout()

        self.slayout_left = QStackedLayout()
        self.compare_left = QFrame()
        self.compare_left.setLayout(self.slayout_left)

        self.labelA = my_label1('A')
        self.comp_tableA = TtreeviewCompare()
        self.proxy_model_parameter1 = QSortFilterProxyModel()
        self.slayout_left.addWidget(self.labelA)
        self.slayout_left.addWidget(self.comp_tableA)
        self.slayout_left.setCurrentIndex(0)
        self.lable_vs = QLabel('VS')
        vs_layout.addWidget(self.lable_vs)

        self.slayout_right = QStackedLayout()
        self.compare_right = QFrame()
        self.compare_right.setLayout(self.slayout_right)
        self.labelB = my_label2('B')
        self.comp_tableB = TtreeviewCompare()
        self.proxy_model_parameter2 = QSortFilterProxyModel()
        self.slayout_right.addWidget(self.labelB)
        self.slayout_right.addWidget(self.comp_tableB)
        self.slayout_right.setCurrentIndex(0)

        a_b_compare_layout.addWidget(self.compare_left)
        a_b_compare_layout.addLayout(vs_layout)
        a_b_compare_layout.addWidget(self.compare_right)

        self.a_b_container.setLayout(a_b_compare_layout)

        self.a_b_result_container = QWidget()
        a_b_result_layout = QVBoxLayout()
        self.comp_table = TtableviewCompare()

        bottom_hlayout = QHBoxLayout()
        self.cbox_match = QRadioButton('Match')
        self.cbox_unmatch = QRadioButton('Discord')
        self.cbox_all = QRadioButton('All')
        bottom_hlayout.addWidget(self.cbox_match)
        bottom_hlayout.addWidget(self.cbox_unmatch)
        bottom_hlayout.addWidget(self.cbox_all)
        a_b_result_layout.addWidget(self.comp_table)
        a_b_result_layout.addLayout(bottom_hlayout)
        self.a_b_result_container.setLayout(a_b_result_layout)

        btnCompare = QHBoxLayout()
        hs = QSpacerItem(10, 10, QSizePolicy.Expanding)
        self.btn_compare = QPushButton('Compare')
        self.btn_compare.setFixedWidth(100)
        btnCompare.addItem(hs)
        btnCompare.addWidget(self.btn_compare)

        refreshBtn = QHBoxLayout()
        hs2 = QSpacerItem(10, 10, QSizePolicy.Expanding)
        self.btn_refresh = QPushButton('Refresh')
        self.btn_refresh.setFixedWidth(100)
        refreshBtn.addWidget(self.btn_refresh)
        refreshBtn.addItem(hs2)

        self.btn_compare.setContentsMargins(0, 0, 0, 0)
        self.search_comp_table = QLineEdit()
        self.search_comp_table.setPlaceholderText('Search in compared table ...')
        parentLayout.addLayout(refreshBtn)
        parentLayout.addWidget(self.search_comp_table)

        self.search_comp_table.setVisible(False)
        parentLayout.addLayout(self.compare_slayout)
        parentLayout.addLayout(btnCompare)
        self.compare_slayout.setCurrentIndex(0)

        self.btn_refresh.clicked.connect(self.refresh)

        '''
        styles = """
        border:2px dotted blue;
        """
        #self.setStyleSheet(styles)
        '''

    def refresh(self, s):
        self.slayout_left.setCurrentIndex(0)
        self.slayout_right.setCurrentIndex(0)

