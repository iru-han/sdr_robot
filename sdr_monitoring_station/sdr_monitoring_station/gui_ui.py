# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QStackedWidget, QTabWidget, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(775, 558)
        Form.setStyleSheet(u"QWidget#Form {\n"
"    background-color: #151b24;\n"
"    color: #eafcff;\n"
"    font-family: \"Malgun Gothic\";\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"QWidget#page, QWidget#page_2, QWidget#page_3 {\n"
"    background-color: #1a212c;\n"
"    border: 1px solid #2c3947;\n"
"    border-radius: 24px;\n"
"}\n"
"\n"
"QStackedWidget#stackedWidget {\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #eafcff;\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"QLabel#label_page, QLabel#label_page_2, QLabel#label_page_3 {\n"
"    color: #8ffcff;\n"
"    font-size: 18pt;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLabel#battery_label {\n"
"    background-color: #222b37;\n"
"    color: #ffd24d;\n"
"    border: 2px solid #7fffd4;\n"
"    border-radius: 16px;\n"
"    padding-left: 14px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QGroupBox {\n"
"    background-color: #212a35;\n"
"    border: 2px solid #9adf22;\n"
"    border-radius: 18px;\n"
"    margin-top: 12px;\n"
""
                        "    color: #8ffcff;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 14px;\n"
"    padding: 0 8px 0 8px;\n"
"    color: #ffb020;\n"
"}\n"
"\n"
"QGroupBox#groupBox_page,\n"
"QGroupBox#groupBox_page_2,\n"
"QGroupBox#groupBox_page_3 {\n"
"    background-color: #212a35;\n"
"    border: 2px solid #7fffd4;\n"
"    border-radius: 18px;\n"
"}\n"
"\n"
"QGroupBox#groupBox_btns {\n"
"    background-color: #1c2430;\n"
"    border: 2px solid #8ffcff;\n"
"    border-radius: 24px;\n"
"    color: #ffb020;\n"
"    font-size: 11pt;\n"
"}\n"
"\n"
"QGroupBox#groupBox_go,\n"
"QGroupBox#groupBox_stop,\n"
"QGroupBox#groupBox_right,\n"
"QGroupBox#groupBox_left,\n"
"QGroupBox#groupBox_back,\n"
"QGroupBox#groupBox_face {\n"
"    background-color: #232d3a;\n"
"    border: 2px solid #ffb020;\n"
"    border-radius: 18px;\n"
"}\n"
"\n"
"QGroupBox#groupBox_go:hover,\n"
"QGroupBox#groupBox_stop:hover,\n"
"QGroupBox#groupBox_right:hover,\n"
"QGroupBox#groupBox_left:hover,\n"
"QGroup"
                        "Box#groupBox_back:hover {\n"
"    background-color: #293544;\n"
"    border: 2px solid #8ffcff;\n"
"}\n"
"\n"
"QListWidget {\n"
"    background-color: #202934;\n"
"    color: #eafcff;\n"
"    border: 2px solid #8ffcff;\n"
"    border-radius: 18px;\n"
"    padding: 8px;\n"
"    outline: none;\n"
"}\n"
"\n"
"QListWidget::item {\n"
"    background-color: #263240;\n"
"    border: 1px solid #3a495b;\n"
"    border-radius: 10px;\n"
"    padding: 8px 10px;\n"
"    margin: 4px 0px;\n"
"}\n"
"\n"
"QListWidget::item:hover {\n"
"    border: 1px solid #9adf22;\n"
"    background-color: #2b3848;\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    background-color: #314154;\n"
"    border: 1px solid #ffb020;\n"
"    color: #8ffcff;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #263240;\n"
"    color: #eafcff;\n"
"    border: 2px solid #8ffcff;\n"
"    border-radius: 16px;\n"
"    padding: 6px 12px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2d3b4c;\n"
"    border: 2px s"
                        "olid #ffb020;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1a222c;\n"
"}\n"
"\n"
"QPushButton#btn_pre,\n"
"QPushButton#btn_next,\n"
"QPushButton#btn_pre_2,\n"
"QPushButton#btn_next_2,\n"
"QPushButton#btn_pre_3,\n"
"QPushButton#btn_next_3 {\n"
"    background-color: #25313d;\n"
"    border: 2px solid #9adf22;\n"
"    color: #8ffcff;\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"QPushButton#btn_pre:hover,\n"
"QPushButton#btn_next:hover,\n"
"QPushButton#btn_pre_2:hover,\n"
"QPushButton#btn_next_2:hover,\n"
"QPushButton#btn_pre_3:hover,\n"
"QPushButton#btn_next_3:hover {\n"
"    border: 2px solid #ffb020;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QPushButton#btn_go,\n"
"QPushButton#btn_stop,\n"
"QPushButton#btn_right,\n"
"QPushButton#btn_left,\n"
"QPushButton#btn_back {\n"
"    background-color: #263240;\n"
"    border: 2px solid #9adf22;\n"
"    border-radius: 18px;\n"
"    color: #ffb020;\n"
"    font-size: 22pt;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton#btn_face {\n"
"    background-color:"
                        " #263240;\n"
"    border: 2px solid #9adf22;\n"
"    border-radius: 18px;\n"
"    color: #ffb020;\n"
"    font-size: 10pt;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton#btn_go:hover,\n"
"QPushButton#btn_stop:hover,\n"
"QPushButton#btn_right:hover,\n"
"QPushButton#btn_left:hover,\n"
"QPushButton#btn_back:hover,\n"
"QPushButton#btn_face:hover {\n"
"    border: 2px solid #8ffcff;\n"
"    color: #8ffcff;\n"
"    background-color: #304051;\n"
"}\n"
"\n"
"QPushButton#btn_go:pressed,\n"
"QPushButton#btn_stop:pressed,\n"
"QPushButton#btn_right:pressed,\n"
"QPushButton#btn_left:pressed,\n"
"QPushButton#btn_back:pressed,\n"
"QPushButton#btn_face:pressed {\n"
"    background-color: #1b2530;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 2px solid #8ffcff;\n"
"    background-color: #202934;\n"
"    border-radius: 18px;\n"
"    top: -1px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background-color: #263240;\n"
"    color: #8ffcff;\n"
"    border: 2px solid #9adf22;\n"
"    border-top-left-radius: 12px;\n"
"    border"
                        "-top-right-radius: 12px;\n"
"    padding: 8px 18px;\n"
"    margin-right: 4px;\n"
"    min-width: 90px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: #304051;\n"
"    color: #ffffff;\n"
"    border: 2px solid #ffb020;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background-color: #2d3b4c;\n"
"}\n"
"QLineEdit {\n"
"    background-color: #263240;\n"
"    color: #eafcff;\n"
"    border: 2px solid #8ffcff;\n"
"    border-radius: 30px;\n"
"    padding: 6px 12px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"")
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 0, 771, 551))
        self.stackedWidget.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.Face_listWidget = QListWidget(self.page)
        self.Face_listWidget.setObjectName(u"Face_listWidget")
        self.Face_listWidget.setGeometry(QRect(540, 180, 221, 261))
        self.battery_label = QLabel(self.page)
        self.battery_label.setObjectName(u"battery_label")
        self.battery_label.setGeometry(QRect(520, 20, 231, 42))
        self.battery_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.groupBox_page = QGroupBox(self.page)
        self.groupBox_page.setObjectName(u"groupBox_page")
        self.groupBox_page.setGeometry(QRect(205, 440, 320, 58))
        self.label_page = QLabel(self.groupBox_page)
        self.label_page.setObjectName(u"label_page")
        self.label_page.setGeometry(QRect(110, 7, 100, 42))
        self.label_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_pre = QPushButton(self.groupBox_page)
        self.btn_pre.setObjectName(u"btn_pre")
        self.btn_pre.setGeometry(QRect(10, 8, 95, 40))
        self.btn_next = QPushButton(self.groupBox_page)
        self.btn_next.setObjectName(u"btn_next")
        self.btn_next.setGeometry(QRect(215, 8, 95, 40))
        self.groupBox_face = QGroupBox(self.page)
        self.groupBox_face.setObjectName(u"groupBox_face")
        self.groupBox_face.setGeometry(QRect(530, 80, 241, 91))
        self.Face_lineEdit = QLineEdit(self.groupBox_face)
        self.Face_lineEdit.setObjectName(u"Face_lineEdit")
        self.Face_lineEdit.setGeometry(QRect(10, 30, 141, 41))
        self.btn_face = QPushButton(self.groupBox_face)
        self.btn_face.setObjectName(u"btn_face")
        self.btn_face.setGeometry(QRect(160, 20, 71, 51))
        self.face_label = QLabel(self.page)
        self.face_label.setObjectName(u"face_label")
        self.face_label.setGeometry(QRect(270, 60, 211, 331))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.tabWidget = QTabWidget(self.page_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(88, 36, 575, 360))
        self.tabWidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.groupBox_page_2 = QGroupBox(self.page_2)
        self.groupBox_page_2.setObjectName(u"groupBox_page_2")
        self.groupBox_page_2.setGeometry(QRect(205, 440, 320, 58))
        self.label_page_2 = QLabel(self.groupBox_page_2)
        self.label_page_2.setObjectName(u"label_page_2")
        self.label_page_2.setGeometry(QRect(110, 7, 100, 42))
        self.label_page_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_pre_2 = QPushButton(self.groupBox_page_2)
        self.btn_pre_2.setObjectName(u"btn_pre_2")
        self.btn_pre_2.setGeometry(QRect(10, 8, 95, 40))
        self.btn_next_2 = QPushButton(self.groupBox_page_2)
        self.btn_next_2.setObjectName(u"btn_next_2")
        self.btn_next_2.setGeometry(QRect(215, 8, 95, 40))
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.groupBox_btns = QGroupBox(self.page_3)
        self.groupBox_btns.setObjectName(u"groupBox_btns")
        self.groupBox_btns.setGeometry(QRect(410, 60, 300, 345))
        self.groupBox_go = QGroupBox(self.groupBox_btns)
        self.groupBox_go.setObjectName(u"groupBox_go")
        self.groupBox_go.setGeometry(QRect(100, 20, 100, 100))
        self.btn_go = QPushButton(self.groupBox_go)
        self.btn_go.setObjectName(u"btn_go")
        self.btn_go.setGeometry(QRect(8, 8, 84, 84))
        self.label_go = QLabel(self.groupBox_go)
        self.label_go.setObjectName(u"label_go")
        self.label_go.setGeometry(QRect(0, 0, 1, 1))
        self.groupBox_left = QGroupBox(self.groupBox_btns)
        self.groupBox_left.setObjectName(u"groupBox_left")
        self.groupBox_left.setGeometry(QRect(0, 122, 100, 100))
        self.btn_left = QPushButton(self.groupBox_left)
        self.btn_left.setObjectName(u"btn_left")
        self.btn_left.setGeometry(QRect(8, 8, 84, 84))
        self.label_left = QLabel(self.groupBox_left)
        self.label_left.setObjectName(u"label_left")
        self.label_left.setGeometry(QRect(0, 0, 1, 1))
        self.groupBox_stop = QGroupBox(self.groupBox_btns)
        self.groupBox_stop.setObjectName(u"groupBox_stop")
        self.groupBox_stop.setGeometry(QRect(100, 122, 100, 100))
        self.btn_stop = QPushButton(self.groupBox_stop)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(8, 8, 84, 84))
        self.label_stop = QLabel(self.groupBox_stop)
        self.label_stop.setObjectName(u"label_stop")
        self.label_stop.setGeometry(QRect(0, 0, 1, 1))
        self.groupBox_right = QGroupBox(self.groupBox_btns)
        self.groupBox_right.setObjectName(u"groupBox_right")
        self.groupBox_right.setGeometry(QRect(200, 122, 100, 100))
        self.btn_right = QPushButton(self.groupBox_right)
        self.btn_right.setObjectName(u"btn_right")
        self.btn_right.setGeometry(QRect(8, 8, 84, 84))
        self.label_right = QLabel(self.groupBox_right)
        self.label_right.setObjectName(u"label_right")
        self.label_right.setGeometry(QRect(0, 0, 1, 1))
        self.groupBox_back = QGroupBox(self.groupBox_btns)
        self.groupBox_back.setObjectName(u"groupBox_back")
        self.groupBox_back.setGeometry(QRect(100, 224, 100, 100))
        self.btn_back = QPushButton(self.groupBox_back)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setGeometry(QRect(8, 8, 84, 84))
        self.label_back = QLabel(self.groupBox_back)
        self.label_back.setObjectName(u"label_back")
        self.label_back.setGeometry(QRect(0, 0, 1, 1))
        self.groupBox_page_3 = QGroupBox(self.page_3)
        self.groupBox_page_3.setObjectName(u"groupBox_page_3")
        self.groupBox_page_3.setGeometry(QRect(205, 430, 320, 58))
        self.label_page_3 = QLabel(self.groupBox_page_3)
        self.label_page_3.setObjectName(u"label_page_3")
        self.label_page_3.setGeometry(QRect(110, 7, 100, 42))
        self.label_page_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_pre_3 = QPushButton(self.groupBox_page_3)
        self.btn_pre_3.setObjectName(u"btn_pre_3")
        self.btn_pre_3.setGeometry(QRect(10, 8, 95, 40))
        self.btn_next_3 = QPushButton(self.groupBox_page_3)
        self.btn_next_3.setObjectName(u"btn_next_3")
        self.btn_next_3.setGeometry(QRect(215, 8, 95, 40))
        self.listWidget = QListWidget(self.page_3)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(40, 60, 221, 338))
        self.listWidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.stackedWidget.addWidget(self.page_3)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.battery_label.setText(QCoreApplication.translate("Form", u"\ubc30\ud130\ub9ac \uc794\ub7c9 :", None))
        self.groupBox_page.setTitle("")
        self.label_page.setText(QCoreApplication.translate("Form", u"1page", None))
        self.btn_pre.setText(QCoreApplication.translate("Form", u"PREV", None))
        self.btn_next.setText(QCoreApplication.translate("Form", u"NEXT", None))
        self.groupBox_face.setTitle("")
        self.Face_lineEdit.setText("")
        self.btn_face.setText(QCoreApplication.translate("Form", u"\ud655\uc778", None))
        self.face_label.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"STATUS", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"CONTROL", None))
        self.groupBox_page_2.setTitle("")
        self.label_page_2.setText(QCoreApplication.translate("Form", u"2page", None))
        self.btn_pre_2.setText(QCoreApplication.translate("Form", u"PREV", None))
        self.btn_next_2.setText(QCoreApplication.translate("Form", u"NEXT", None))
        self.groupBox_btns.setTitle(QCoreApplication.translate("Form", u"CONTROL PANEL", None))
        self.groupBox_go.setTitle("")
        self.btn_go.setText(QCoreApplication.translate("Form", u"\u2191", None))
        self.label_go.setText("")
        self.groupBox_left.setTitle("")
        self.btn_left.setText(QCoreApplication.translate("Form", u"\u2190", None))
        self.label_left.setText("")
        self.groupBox_stop.setTitle("")
        self.btn_stop.setText(QCoreApplication.translate("Form", u"\u25a0", None))
        self.label_stop.setText("")
        self.groupBox_right.setTitle("")
        self.btn_right.setText(QCoreApplication.translate("Form", u"\u2192", None))
        self.label_right.setText("")
        self.groupBox_back.setTitle("")
        self.btn_back.setText(QCoreApplication.translate("Form", u"\u2193", None))
        self.label_back.setText("")
        self.groupBox_page_3.setTitle("")
        self.label_page_3.setText(QCoreApplication.translate("Form", u"3page", None))
        self.btn_pre_3.setText(QCoreApplication.translate("Form", u"PREV", None))
        self.btn_next_3.setText(QCoreApplication.translate("Form", u"NEXT", None))
    # retranslateUi

