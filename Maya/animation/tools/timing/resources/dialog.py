# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K:/.core/dev/tapp/Tapp/Maya/animation\tools\timing\resources\dialog.ui'
#
# Created: Mon Aug 15 18:32:33 2016
#      by: Qt UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(513, 115)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 115))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.bake_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.bake_checkBox.setObjectName("bake_checkBox")
        self.horizontalLayout_3.addWidget(self.bake_checkBox)
        self.forwardOnly_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.forwardOnly_checkBox.setObjectName("forwardOnly_checkBox")
        self.horizontalLayout_3.addWidget(self.forwardOnly_checkBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.accurracy_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.accurracy_doubleSpinBox.setObjectName("accurracy_doubleSpinBox")
        self.horizontalLayout.addWidget(self.accurracy_doubleSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.storeAnimation_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.storeAnimation_pushButton.setMinimumSize(QtCore.QSize(100, 40))
        self.storeAnimation_pushButton.setObjectName("storeAnimation_pushButton")
        self.horizontalLayout_2.addWidget(self.storeAnimation_pushButton)
        self.restoreAnimation_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.restoreAnimation_pushButton.setMinimumSize(QtCore.QSize(100, 40))
        self.restoreAnimation_pushButton.setObjectName("restoreAnimation_pushButton")
        self.horizontalLayout_2.addWidget(self.restoreAnimation_pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout_5.addWidget(self.horizontalSlider)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Timing Tool"))
        self.bake_checkBox.setText(_translate("MainWindow", "Bake"))
        self.forwardOnly_checkBox.setText(_translate("MainWindow", "Forward-only"))
        self.label.setText(_translate("MainWindow", "Accuracy:"))
        self.storeAnimation_pushButton.setText(_translate("MainWindow", "Store Animation"))
        self.restoreAnimation_pushButton.setText(_translate("MainWindow", "Restore Animation"))

