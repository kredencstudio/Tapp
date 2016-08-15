# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K:/.core/dev/tapp/Tapp/Maya/lighting\region\resources\region.ui'
#
# Created: Mon Aug 15 18:32:33 2016
#      by: Qt UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(392, 259)
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.renderlayer_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.renderlayer_listWidget.setObjectName("renderlayer_listWidget")
        self.horizontalLayout.addWidget(self.renderlayer_listWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.refresh_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_pushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.refresh_pushButton.setObjectName("refresh_pushButton")
        self.verticalLayout.addWidget(self.refresh_pushButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.getPreviewRegion_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.getPreviewRegion_pushButton.setObjectName("getPreviewRegion_pushButton")
        self.verticalLayout.addWidget(self.getPreviewRegion_pushButton)
        self.getObjectRegion_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.getObjectRegion_pushButton.setObjectName("getObjectRegion_pushButton")
        self.verticalLayout.addWidget(self.getObjectRegion_pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.connectPreview_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectPreview_pushButton.setObjectName("connectPreview_pushButton")
        self.verticalLayout.addWidget(self.connectPreview_pushButton)
        self.disconnectPreview_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.disconnectPreview_pushButton.setObjectName("disconnectPreview_pushButton")
        self.verticalLayout.addWidget(self.disconnectPreview_pushButton)
        self.connectArnold_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectArnold_pushButton.setObjectName("connectArnold_pushButton")
        self.verticalLayout.addWidget(self.connectArnold_pushButton)
        self.disconnectArnold_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.disconnectArnold_pushButton.setObjectName("disconnectArnold_pushButton")
        self.verticalLayout.addWidget(self.disconnectArnold_pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Region Render"))
        self.refresh_pushButton.setText(_translate("MainWindow", "Refresh"))
        self.getPreviewRegion_pushButton.setText(_translate("MainWindow", "Get Preview Region"))
        self.getObjectRegion_pushButton.setText(_translate("MainWindow", "Get Object Region"))
        self.connectPreview_pushButton.setText(_translate("MainWindow", "Connect Preview"))
        self.disconnectPreview_pushButton.setText(_translate("MainWindow", "Disconnect Preview"))
        self.connectArnold_pushButton.setText(_translate("MainWindow", "Connect Arnold"))
        self.disconnectArnold_pushButton.setText(_translate("MainWindow", "Disconnect Arnold"))

