# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auto_grid_comp_dialog_base.ui'
#
# Created: Thu Nov 10 10:56:45 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AutoGridCompDialogBase(object):
    def setupUi(self, AutoGridCompDialogBase):
        AutoGridCompDialogBase.setObjectName(_fromUtf8("AutoGridCompDialogBase"))
        AutoGridCompDialogBase.resize(400, 300)
        self.button_box = QtGui.QDialogButtonBox(AutoGridCompDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))

        self.retranslateUi(AutoGridCompDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), AutoGridCompDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), AutoGridCompDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(AutoGridCompDialogBase)

    def retranslateUi(self, AutoGridCompDialogBase):
        AutoGridCompDialogBase.setWindowTitle(_translate("AutoGridCompDialogBase", "AutoGridComp", None))

