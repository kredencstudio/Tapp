# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K:/.core/dev/tapp/Tapp/Maya/animation\tools\resetAttributes\resources\dialog.ui'
#
# Created: Mon Aug 15 18:32:32 2016
#      by: Qt UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(201, 116)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.line_23 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_23.sizePolicy().hasHeightForWidth())
        self.line_23.setSizePolicy(sizePolicy)
        self.line_23.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
        self.horizontalLayout_2.addWidget(self.line_23)
        self.character_fkik_label = QtWidgets.QLabel(self.centralwidget)
        self.character_fkik_label.setObjectName("character_fkik_label")
        self.horizontalLayout_2.addWidget(self.character_fkik_label)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.translation_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.translation_checkBox.setChecked(True)
        self.translation_checkBox.setObjectName("translation_checkBox")
        self.gridLayout.addWidget(self.translation_checkBox, 0, 0, 1, 1)
        self.rotation_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.rotation_checkBox.setChecked(True)
        self.rotation_checkBox.setObjectName("rotation_checkBox")
        self.gridLayout.addWidget(self.rotation_checkBox, 0, 1, 1, 1)
        self.scale_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.scale_checkBox.setChecked(True)
        self.scale_checkBox.setObjectName("scale_checkBox")
        self.gridLayout.addWidget(self.scale_checkBox, 1, 0, 1, 1)
        self.extraAttributes_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.extraAttributes_checkBox.setChecked(True)
        self.extraAttributes_checkBox.setObjectName("extraAttributes_checkBox")
        self.gridLayout.addWidget(self.extraAttributes_checkBox, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Reset Attributes"))
        self.character_fkik_label.setText(_translate("MainWindow", "Reset Attributes"))
        self.pushButton.setText(_translate("MainWindow", "Reset Selection"))
        self.translation_checkBox.setText(_translate("MainWindow", "Translation"))
        self.rotation_checkBox.setText(_translate("MainWindow", "Rotation"))
        self.scale_checkBox.setText(_translate("MainWindow", "Scale"))
        self.extraAttributes_checkBox.setText(_translate("MainWindow", "Extra Attributes"))

