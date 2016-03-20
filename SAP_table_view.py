import sqlite3
import PyQt4.QtGui
import PyQt4.QtCore
__author__ = 'U104675'

class SAP_table_view(PyQt4.QtCore.QThread):
    def __init__(self, SAP_connection):
        self._FM = 'RFC_READ_TABLE'
        self._SAP_conn = SAP_connection

    def read_SAP_table_spec(self, table_name):
        '''
        Retrieve the table specification of a SAP table
        :param table_name: The table we are interested in
        :return: A list of dictionaries each being in format {u'FIELDTEXT': u'Material Group', u'TYPE': u'C', u'LENGTH': u'000009', u'FIELDNAME': u'MATKL', u'OFFSET': u'000097'}
        '''
        try:
            result = self._SAP_conn.call(self._FM, QUERY_TABLE = table_name, NO_DATA = 'NO', ROWCOUNT = 0,
                                     ROWSKIPS = 0,  OPTIONS =  [], FIELDS = [])

            for v in result['FIELDS']: print v
            return result['FIELDS']
        except Exception, message:
            msg = PyQt4.QtGui.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Selection Error")
            msg.setIcon(PyQt4.QtGui.QMessageBox.Critical)
            msg.setInformativeText(repr(message))
            msg.exec_()
            return
