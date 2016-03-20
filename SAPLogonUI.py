import pyrfc
from SAPLogon import Ui_Dialog
import PyQt4.QtGui
import PyQt4.QtCore
import PyQt4.Qt
import sqlite3
from decimal import * #Its required when you try and cx_freeze the app, by pyrfc module.
__author__ = 'U104675'


class SAPLogonUI(Ui_Dialog):
    def __init__(self, parent):
        """
        Create a GUI to allow supply of SAP login credentials
        :parent: This is the calling object (screen). It must have a method set_SAP_connection() by which the
            SAP connection object can be returned
        :return: None
        """
        #Set up screen layout
        self._dlg = PyQt4.QtGui.QDialog()
        self.setupUi(self._dlg)
        self._parent = parent
        #Attempt to set up parameters used from last login from ini database
        conn = sqlite3.connect(self._parent.get_ini_db_name())
        c = conn.cursor()
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='CLIENT'")
        for r in row: self.client_lineEdit.setText(r[0])
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='LANGU'")
        for r in row: self.langu_lineEdit.setText(r[0])
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='MSG_SERVER'")
        for r in row: self.msg_server_lineEdit.setText(r[0])
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='SYSTEM'")
        for r in row: self.system_lineEdit.setText(r[0])
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='GROUP'")
        for r in row: self.group_lineEdit.setText(r[0])
        conn.close()

        self._SAPConn = None
        self.cancel_pushButton.clicked.connect(self._exit)
        self.OK_pushButton.clicked.connect(self.login)
        self._dlg.setVisible(True)
        self._dlg.exec_()

    def _exit(self):
        """
        Close the dialog without having logged in so call the parent method and pass a "None" connection object.
        :return: Nothing
        """
        self._parent.set_SAP_connection(None)
        self._dlg.close()

    def login(self):
        """
        Get the login information from the user dialog (which is populated with some handy defaults) and attempt
        to connect to SAP. If there is a problem, fail with an informative message. Pass connection object back to the
        parent with the parents set_SAP_connection() method.
        :return: Nothing
        """
        client = str(self.client_lineEdit.text())
        user = str(self.user_lineEdit.text())
        passwd = str(self.password_lineEdit.text())
        lang = str(self.langu_lineEdit.text())
        mshost = str(self.msg_server_lineEdit.text())
        sysid = str(self.system_lineEdit.text())
        group = str(self.group_lineEdit.text())
        params = {'client' : client, 'user' : user, 'passwd' : passwd , 'lang' : lang,
                  'mshost' : mshost, 'sysid' : sysid, 'group' : group}
        try:
            self._SAPConn = pyrfc.Connection(**params)
            self._parent.set_SAP_connection(self._SAPConn) #Pass connection back to parent
            #Store last used values for later use
            conn = sqlite3.connect(self._parent.get_ini_db_name())
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('CLIENT',
                str(self.client_lineEdit.text())))
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('LANGU',
                str(self.langu_lineEdit.text())))
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('MSG_SERVER',
                str(self.msg_server_lineEdit.text())))
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('SYSTEM',
                str(self.system_lineEdit.text())))
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('GROUP',
                str(self.group_lineEdit.text())))
            conn.commit()
            conn.close()
            #Finish up
            self._dlg.close()
            return
        except Exception, message:
            msg = PyQt4.QtGui.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(PyQt4.QtGui.QMessageBox.Critical)
            msg.setInformativeText("RFC Error : " + repr(message))
            msg.exec_()
            self._parent.set_SAP_connection(None)
            return