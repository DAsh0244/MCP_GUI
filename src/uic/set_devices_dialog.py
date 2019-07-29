# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis\set_devices_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(340, 152)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.scan_button = QtWidgets.QPushButton(Dialog)
        self.scan_button.setObjectName("scan_button")
        self.verticalLayout.addWidget(self.scan_button)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.psu_addr_box = QtWidgets.QSpinBox(Dialog)
        self.psu_addr_box.setObjectName("psu_addr_box")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.psu_addr_box)
        self.scope_addr_box = QtWidgets.QSpinBox(Dialog)
        self.scope_addr_box.setObjectName("scope_addr_box")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.scope_addr_box)
        self.prologix_port_box = QtWidgets.QComboBox(Dialog)
        self.prologix_port_box.setObjectName("prologix_port_box")
        self.prologix_port_box.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.prologix_port_box)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.scan_button.setText(_translate("Dialog", "Scan Devices"))
        self.label.setText(_translate("Dialog", "Prologix Port"))
        self.label_2.setText(_translate("Dialog", "Power Supply Address"))
        self.label_3.setText(_translate("Dialog", "Scope Address"))
        # self.prologix_port_box.setItemText(0, _translate("Dialog", "Scan for Devices"))

