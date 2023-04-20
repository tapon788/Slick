from PyQt5.QtWidgets import *


class Ttreeview(QTreeView):
    def __init__(self,*args,**kwargs):
        super(Ttreeview,self).__init__(*args,**kwargs)
        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        #qss_file = open("style\\style.qss").read()

        styleshett = """
                QTreeView::branch:has-siblings:!adjoins-item {
        border-image: url(resources/img/treeview/vline.png) 0;
        }

        QTreeView::branch:has-siblings:adjoins-item {
            border-image: url(resources/img/treeview/branch-more.png) 0;
        }

        QTreeView::branch:!has-children:!has-siblings:adjoins-item {
            border-image: url(resources/img/treeview/branch-end.png) 0;
        }

        QTreeView::branch:has-children:!has-siblings:closed,
        QTreeView::branch:closed:has-children:has-siblings {
                border-image: none;
                image: url(resources/img/treeview/plus.png);
        }

        QTreeView::branch:open:has-children:!has-siblings,
        QTreeView::branch:open:has-children:has-siblings  {
                border-image: none;
                image: url(resources/img/treeview/down.png);
        }
        """


        self.setStyleSheet(styleshett)
        # self.setAlternatingRowColors(True)
        #self.setAllColumnsShowFocus(True)
        #self.setFont(QFont('Courier'))
        #self.setAnimated(True)


class TtreeviewCompare(QTreeView):
    def __init__(self,*args,**kwargs):
        super(TtreeviewCompare,self).__init__(*args,**kwargs)
        header = self.header()
        #qss_file = open("style\\style.qss").read()

        styleshett = """
                QTreeView::branch:has-siblings:!adjoins-item {
        border-image: url(resources/img/treeview/vline.png) 0;
        }

        QTreeView::branch:has-siblings:adjoins-item {
            border-image: url(resources/img/treeview/branch-more.png) 0;
        }

        QTreeView::branch:!has-children:!has-siblings:adjoins-item {
            border-image: url(resources/img/treeview/branch-end.png) 0;
        }

        QTreeView::branch:has-children:!has-siblings:closed,
        QTreeView::branch:closed:has-children:has-siblings {
                border-image: none;
                image: url(resources/img/treeview/plus.png);
        }

        QTreeView::branch:open:has-children:!has-siblings,
        QTreeView::branch:open:has-children:has-siblings  {
                border-image: none;
                image: url(resources/img/treeview/down.png);
        }
        """


        self.setStyleSheet(styleshett)
        # self.setAlternatingRowColors(True)
        #self.setAllColumnsShowFocus(True)
        #self.setFont(QFont('Courier'))
        #self.setAnimated(True)


