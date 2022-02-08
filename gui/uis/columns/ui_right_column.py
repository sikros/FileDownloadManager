# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *


class Ui_RightColumn(object):
    def setupUi(self, RightColumn):
        if not RightColumn.objectName():
            RightColumn.setObjectName(u"RightColumn")
        RightColumn.resize(240, 600)
        self.main_pages_layout = QVBoxLayout(RightColumn)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.menus = QStackedWidget(RightColumn)
        self.menus.setObjectName(u"menus")
        self.menu_1 = QWidget()
        self.menu_1.setObjectName(u"menu_1")
        self.verticalLayout = QVBoxLayout(self.menu_1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)


        self.label_1 = QLabel(self.menu_1)
        self.label_1.setObjectName(u"label_1")
        font = QFont()
        font.setPointSize(16)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet(u"font-size: 16pt")
        self.label_1.setAlignment(Qt.AlignHCenter|Qt.AlignBottom)

        self.verticalLayout.addWidget(self.label_1)

        self.label_2 = QLabel(self.menu_1)
        self.label_2.setObjectName(u"label_2")
        font_2 = QFont()
        font_2.setPointSize(8)
        self.label_2.setFont(font_2)
        self.label_2.setStyleSheet(u"font-size: 8pt")
        self.label_2.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.menu_1)
        self.label_3.setObjectName(u"label_3")
        font_3 = QFont()
        font_3.setPointSize(10)
        self.label_3.setFont(font_3)
        self.label_3.setStyleSheet(u"font-size: 10pt")
        self.label_3.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.label_3.setOpenExternalLinks(True)
        self.verticalLayout.addWidget(self.label_3)

        
        self.label_4 = QLabel(self.menu_1)
        self.label_4.setObjectName(u"label_3")
        font_4 = QFont()
        font_4.setPointSize(10)
        self.label_4.setFont(font_4)
        self.label_4.setStyleSheet(u"font-size: 10pt")
        self.label_4.setAlignment(Qt.AlignHCenter|Qt.AlignBottom)
        self.label_4.setOpenExternalLinks(True)
        self.verticalLayout.addWidget(self.label_4)

        
        self.menus.addWidget(self.menu_1)
        self.main_pages_layout.addWidget(self.menus)

        self.retranslateUi(RightColumn)
        self.menus.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(RightColumn)
    # setupUi

    def retranslateUi(self, RightColumn):
        RightColumn.setWindowTitle(QCoreApplication.translate("RightColumn", u"Form", None))
        self.label_1.setText(QCoreApplication.translate("RightColumn", u"网盘分享资源下载", None))
        self.label_2.setText(QCoreApplication.translate("RightColumn", u"Version: 1.0", None))
        
        self.label_3.setText(QCoreApplication.translate("RightColumn", u"""
        <a style='color:Gainsboro;text-decoration:none' href='https://www.xcjkwl.com/'>Web site</a> | 
        <a style='color:Gainsboro;text-decoration:none' href='https://www.github.com/sikros'>Git repo</a><br>""", None))

        self.label_4.setText(QCoreApplication.translate("RightColumn", u"""Presented by <a style='color:Gainsboro;text-decoration:none' href='https://kim.xcjkwl.com/'>Kim</a>
        <br><br>
        UI Design by <a style='color:Gainsboro;text-decoration:none' href='https://github.com/Wanderson-Magalhaes/PyOneDark_Qt_Widgets_Modern_GUI'>Wanderson Magalhaes</a>
        """,None))
    # retranslateUi

