# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SAPTableExtractor.ui'
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

class Ui_SAPTableExtractor(object):
    def setupUi(self, SAPTableExtractor):
        SAPTableExtractor.setObjectName(_fromUtf8("SAPTableExtractor"))
        SAPTableExtractor.resize(400, 691)
        SAPTableExtractor.setMinimumSize(QtCore.QSize(400, 600))
        SAPTableExtractor.setMaximumSize(QtCore.QSize(400, 700))
        SAPTableExtractor.setSizeGripEnabled(False)
        self.label = QtGui.QLabel(SAPTableExtractor)
        self.label.setGeometry(QtCore.QRect(10, 20, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.SAPTable_lineEdit = QtGui.QLineEdit(SAPTableExtractor)
        self.SAPTable_lineEdit.setGeometry(QtCore.QRect(80, 20, 301, 21))
        self.SAPTable_lineEdit.setObjectName(_fromUtf8("SAPTable_lineEdit"))
        self.Choose_pushButton = QtGui.QPushButton(SAPTableExtractor)
        self.Choose_pushButton.setGeometry(QtCore.QRect(10, 310, 91, 23))
        self.Choose_pushButton.setObjectName(_fromUtf8("Choose_pushButton"))
        self.Cancel_pushButton = QtGui.QPushButton(SAPTableExtractor)
        self.Cancel_pushButton.setGeometry(QtCore.QRect(290, 600, 91, 23))
        self.Cancel_pushButton.setObjectName(_fromUtf8("Cancel_pushButton"))
        self.label_2 = QtGui.QLabel(SAPTableExtractor)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 351, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.Extract_pushButton = QtGui.QPushButton(SAPTableExtractor)
        self.Extract_pushButton.setGeometry(QtCore.QRect(10, 600, 91, 23))
        self.Extract_pushButton.setObjectName(_fromUtf8("Extract_pushButton"))
        self.Field_listWidget = QtGui.QListWidget(SAPTableExtractor)
        self.Field_listWidget.setGeometry(QtCore.QRect(10, 110, 371, 192))
        self.Field_listWidget.setSelectionRectVisible(True)
        self.Field_listWidget.setObjectName(_fromUtf8("Field_listWidget"))
        self.Restriction_lineEdit = QtGui.QLineEdit(SAPTableExtractor)
        self.Restriction_lineEdit.setGeometry(QtCore.QRect(10, 360, 371, 20))
        self.Restriction_lineEdit.setObjectName(_fromUtf8("Restriction_lineEdit"))
        self.label_3 = QtGui.QLabel(SAPTableExtractor)
        self.label_3.setGeometry(QtCore.QRect(10, 340, 321, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.Append_checkBox = QtGui.QCheckBox(SAPTableExtractor)
        self.Append_checkBox.setGeometry(QtCore.QRect(10, 570, 161, 31))
        self.Append_checkBox.setObjectName(_fromUtf8("Append_checkBox"))
        self.maxRows_lineEdit = QtGui.QLineEdit(SAPTableExtractor)
        self.maxRows_lineEdit.setGeometry(QtCore.QRect(80, 50, 113, 20))
        self.maxRows_lineEdit.setObjectName(_fromUtf8("maxRows_lineEdit"))
        self.label_4 = QtGui.QLabel(SAPTableExtractor)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.DBName_lineEdit = QtGui.QLineEdit(SAPTableExtractor)
        self.DBName_lineEdit.setGeometry(QtCore.QRect(10, 500, 371, 20))
        self.DBName_lineEdit.setObjectName(_fromUtf8("DBName_lineEdit"))
        self.label_5 = QtGui.QLabel(SAPTableExtractor)
        self.label_5.setGeometry(QtCore.QRect(10, 480, 121, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(SAPTableExtractor)
        self.label_6.setGeometry(QtCore.QRect(10, 530, 111, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.DBTable_lineEdit = QtGui.QLineEdit(SAPTableExtractor)
        self.DBTable_lineEdit.setGeometry(QtCore.QRect(10, 550, 371, 20))
        self.DBTable_lineEdit.setObjectName(_fromUtf8("DBTable_lineEdit"))
        self.dbselect_pushButton = QtGui.QPushButton(SAPTableExtractor)
        self.dbselect_pushButton.setGeometry(QtCore.QRect(10, 450, 111, 23))
        self.dbselect_pushButton.setObjectName(_fromUtf8("dbselect_pushButton"))
        self.progressBar = QtGui.QProgressBar(SAPTableExtractor)
        self.progressBar.setGeometry(QtCore.QRect(10, 630, 371, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.message_label = QtGui.QLabel(SAPTableExtractor)
        self.message_label.setGeometry(QtCore.QRect(10, 660, 371, 16))
        self.message_label.setText(_fromUtf8(""))
        self.message_label.setObjectName(_fromUtf8("message_label"))
        self.Restriction_lineEdit1 = QtGui.QLineEdit(SAPTableExtractor)
        self.Restriction_lineEdit1.setGeometry(QtCore.QRect(10, 390, 371, 21))
        self.Restriction_lineEdit1.setObjectName(_fromUtf8("Restriction_lineEdit1"))
        self.Restriction_lineEdit2 = QtGui.QLineEdit(SAPTableExtractor)
        self.Restriction_lineEdit2.setGeometry(QtCore.QRect(10, 420, 371, 20))
        self.Restriction_lineEdit2.setObjectName(_fromUtf8("Restriction_lineEdit2"))

        self.retranslateUi(SAPTableExtractor)
        QtCore.QMetaObject.connectSlotsByName(SAPTableExtractor)
        SAPTableExtractor.setTabOrder(self.SAPTable_lineEdit, self.maxRows_lineEdit)
        SAPTableExtractor.setTabOrder(self.maxRows_lineEdit, self.Restriction_lineEdit)
        SAPTableExtractor.setTabOrder(self.Restriction_lineEdit, self.Restriction_lineEdit1)
        SAPTableExtractor.setTabOrder(self.Restriction_lineEdit1, self.Restriction_lineEdit2)
        SAPTableExtractor.setTabOrder(self.Restriction_lineEdit2, self.dbselect_pushButton)
        SAPTableExtractor.setTabOrder(self.dbselect_pushButton, self.DBName_lineEdit)
        SAPTableExtractor.setTabOrder(self.DBName_lineEdit, self.DBTable_lineEdit)
        SAPTableExtractor.setTabOrder(self.DBTable_lineEdit, self.Append_checkBox)
        SAPTableExtractor.setTabOrder(self.Append_checkBox, self.Extract_pushButton)
        SAPTableExtractor.setTabOrder(self.Extract_pushButton, self.Cancel_pushButton)
        SAPTableExtractor.setTabOrder(self.Cancel_pushButton, self.Choose_pushButton)
        SAPTableExtractor.setTabOrder(self.Choose_pushButton, self.Field_listWidget)

    def retranslateUi(self, SAPTableExtractor):
        SAPTableExtractor.setWindowTitle(_translate("SAPTableExtractor", "SAP Table Extractor", None))
        self.label.setText(_translate("SAPTableExtractor", "SAP Table", None))
        self.Choose_pushButton.setText(_translate("SAPTableExtractor", "Choose Fields", None))
        self.Cancel_pushButton.setText(_translate("SAPTableExtractor", "Cancel", None))
        self.label_2.setText(_translate("SAPTableExtractor", " Select Fields (Max. 512 Total Length)", None))
        self.Extract_pushButton.setText(_translate("SAPTableExtractor", "Extract Fields", None))
        self.label_3.setText(_translate("SAPTableExtractor", "ABAP Restriction (eg. MATL_TYPE = \'HALB\') - max 72 chars per line", None))
        self.Append_checkBox.setText(_translate("SAPTableExtractor", "Append to existing table?", None))
        self.label_4.setText(_translate("SAPTableExtractor", "Max Rows", None))
        self.label_5.setText(_translate("SAPTableExtractor", "Output Database Name", None))
        self.label_6.setText(_translate("SAPTableExtractor", "Database Table", None))
        self.dbselect_pushButton.setText(_translate("SAPTableExtractor", "Select New Database", None))

