# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SAPLogon.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(265, 263)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("thread_16xLG.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.user_lineEdit = QtGui.QLineEdit(Dialog)
        self.user_lineEdit.setGeometry(QtCore.QRect(100, 10, 131, 20))
        self.user_lineEdit.setMouseTracking(True)
        self.user_lineEdit.setAutoFillBackground(False)
        self.user_lineEdit.setObjectName(_fromUtf8("user_lineEdit"))
        self.user_label = QtGui.QLabel(Dialog)
        self.user_label.setGeometry(QtCore.QRect(10, 10, 46, 13))
        self.user_label.setObjectName(_fromUtf8("user_label"))
        self.password_label = QtGui.QLabel(Dialog)
        self.password_label.setGeometry(QtCore.QRect(10, 40, 46, 13))
        self.password_label.setObjectName(_fromUtf8("password_label"))
        self.password_lineEdit = QtGui.QLineEdit(Dialog)
        self.password_lineEdit.setGeometry(QtCore.QRect(100, 40, 131, 20))
        self.password_lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.password_lineEdit.setObjectName(_fromUtf8("password_lineEdit"))
        self.langu_label = QtGui.QLabel(Dialog)
        self.langu_label.setGeometry(QtCore.QRect(10, 130, 46, 13))
        self.langu_label.setObjectName(_fromUtf8("langu_label"))
        self.langu_lineEdit = QtGui.QLineEdit(Dialog)
        self.langu_lineEdit.setGeometry(QtCore.QRect(100, 130, 41, 20))
        self.langu_lineEdit.setObjectName(_fromUtf8("langu_lineEdit"))
        self.msgserver_label = QtGui.QLabel(Dialog)
        self.msgserver_label.setGeometry(QtCore.QRect(10, 190, 81, 16))
        self.msgserver_label.setObjectName(_fromUtf8("msgserver_label"))
        self.msg_server_lineEdit = QtGui.QLineEdit(Dialog)
        self.msg_server_lineEdit.setGeometry(QtCore.QRect(100, 190, 131, 20))
        self.msg_server_lineEdit.setObjectName(_fromUtf8("msg_server_lineEdit"))
        self.sysid_label = QtGui.QLabel(Dialog)
        self.sysid_label.setGeometry(QtCore.QRect(10, 70, 46, 13))
        self.sysid_label.setObjectName(_fromUtf8("sysid_label"))
        self.system_lineEdit = QtGui.QLineEdit(Dialog)
        self.system_lineEdit.setGeometry(QtCore.QRect(100, 70, 41, 20))
        self.system_lineEdit.setObjectName(_fromUtf8("system_lineEdit"))
        self.group_lineEdit = QtGui.QLineEdit(Dialog)
        self.group_lineEdit.setGeometry(QtCore.QRect(100, 160, 131, 20))
        self.group_lineEdit.setObjectName(_fromUtf8("group_lineEdit"))
        self.group_label = QtGui.QLabel(Dialog)
        self.group_label.setGeometry(QtCore.QRect(10, 160, 46, 13))
        self.group_label.setObjectName(_fromUtf8("group_label"))
        self.cancel_pushButton = QtGui.QPushButton(Dialog)
        self.cancel_pushButton.setGeometry(QtCore.QRect(180, 220, 51, 23))
        self.cancel_pushButton.setObjectName(_fromUtf8("cancel_pushButton"))
        self.OK_pushButton = QtGui.QPushButton(Dialog)
        self.OK_pushButton.setGeometry(QtCore.QRect(120, 220, 51, 23))
        self.OK_pushButton.setObjectName(_fromUtf8("OK_pushButton"))
        self.client_label = QtGui.QLabel(Dialog)
        self.client_label.setGeometry(QtCore.QRect(10, 100, 46, 13))
        self.client_label.setObjectName(_fromUtf8("client_label"))
        self.client_lineEdit = QtGui.QLineEdit(Dialog)
        self.client_lineEdit.setGeometry(QtCore.QRect(100, 100, 41, 20))
        self.client_lineEdit.setObjectName(_fromUtf8("client_lineEdit"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.user_lineEdit, self.password_lineEdit)
        Dialog.setTabOrder(self.password_lineEdit, self.system_lineEdit)
        Dialog.setTabOrder(self.system_lineEdit, self.client_lineEdit)
        Dialog.setTabOrder(self.client_lineEdit, self.langu_lineEdit)
        Dialog.setTabOrder(self.langu_lineEdit, self.group_lineEdit)
        Dialog.setTabOrder(self.group_lineEdit, self.msg_server_lineEdit)
        Dialog.setTabOrder(self.msg_server_lineEdit, self.OK_pushButton)
        Dialog.setTabOrder(self.OK_pushButton, self.cancel_pushButton)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "SAP Logon", None))
        self.user_label.setText(_translate("Dialog", "User", None))
        self.password_label.setText(_translate("Dialog", "Password", None))
        self.langu_label.setText(_translate("Dialog", "Language", None))
        self.langu_lineEdit.setText(_translate("Dialog", "EN", None))
        self.msgserver_label.setText(_translate("Dialog", "Message Server", None))
        self.msg_server_lineEdit.setText(_translate("Dialog", "emsg1w.erp.kodak.com", None))
        self.sysid_label.setText(_translate("Dialog", "System", None))
        self.system_lineEdit.setText(_translate("Dialog", "G1W", None))
        self.group_lineEdit.setText(_translate("Dialog", "ALL", None))
        self.group_label.setText(_translate("Dialog", "Group", None))
        self.cancel_pushButton.setText(_translate("Dialog", "Cancel", None))
        self.OK_pushButton.setText(_translate("Dialog", "OK", None))
        self.client_label.setText(_translate("Dialog", "Client", None))
        self.client_lineEdit.setText(_translate("Dialog", "023", None))

