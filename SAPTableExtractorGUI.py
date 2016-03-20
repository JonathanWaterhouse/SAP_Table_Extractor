import os
from SAPTableExtractor import Ui_SAPTableExtractor
from SAPLogonUI import SAPLogonUI
from Get_SAP_Table_Data_Thread import *
from SAP_table_view import SAP_table_view
from PyQt4.QtCore import *
import PyQt4.QtGui

__author__ = 'U104675'

class SAPTableExtractorGUI(Ui_SAPTableExtractor):
    """
    GUI for SAP table extractor. The only real link to SAP is in the self._SAP_conn object which is set in the
    SAPLogonUI and passed to this GUI by call of method set_SAP_connection. The methods of that connection object
    (which are provided by pyrfc module from SAP) are called by invoking methods of the connection object. because
    these can be time consuming for large table extractions they are kept out of the GUI and performed in a separate
    thread so that GUI actions such as cancel, and display of status bar changes can be performed during processing.
    """
    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        self._otherGuiSetup()
        #Setup some internally required file locations
        dataDir = self.getDataDir() + os.sep
        self._logged_in = False #Logged in to SAP
        self._selected_fields = []
        self._sqlite_ini_name = 'ini.db'
        # Initialisations of other stuff
        self._IsRFCError = False
        self._RFC_READ_TABLE_output  = None
        self._msg_display_time = 20000
        self._progress_bar_interval = 200
        #Initilisations from last time in
        conn = sqlite3.connect(self._sqlite_ini_name)
        c = conn.cursor()
        #Settings database
        c.execute("CREATE TABLE IF NOT EXISTS SETTINGS (KEY TEXT PRIMARY KEY, VALUE TEXT)")
        #Last table extracted
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='LAST_TABLE'")
        for r in row: self.SAPTable_lineEdit.setText(r[0])
        #Last Max rows to extract setting but ensure there is a default if non set.
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='MAX_ROWS'")
        for r in row: self.maxRows_lineEdit.setText(r[0])
        if self.maxRows_lineEdit.text() == '': self.maxRows_lineEdit.setText('50000000')
        #sqlite3 database location and name
        self._db_file_name = 'SAPTables.db'
        row.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='DB_NAME'")
        for r in row: self._sqlite_db_name = r[0]
        self.DBName_lineEdit.setText(self._sqlite_db_name)
        conn.close()

    def getDataDir(self):
        """
        This application may have a windows executable built from it using cx_Freeze in
        which case the local directly that the script runs from assumed by python
        will be incorrect. Here we derive the data directory. This allows the ini file
        Maestro.ini to be found and intermediate files for Graphviz
        """
        if getattr(sys, 'frozen', False):
        # The application is frozen
            datadir = os.path.dirname(sys.executable)
        else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
            datadir = os.getcwd()

        return datadir

    def _otherGuiSetup(self):
        """ Do other setup things required to get the static GUI components set up, and
        components acting correctly upon user interaction. There should NOT be any
        code associated with date reading or population in here.
        """
        self.progressBar.setVisible(False)
        self.progressBar.setMaximum(10)
        self.progressBar.setMinimum(0)
        #Actions
        self.DBName_lineEdit.setReadOnly(True)
        self.Cancel_pushButton.clicked.connect(self.exit)
        self.Choose_pushButton.clicked.connect(self.displayTableFields)
        self.Extract_pushButton.clicked.connect(self.extract)
        self.SAPTable_lineEdit.editingFinished.connect(self.reset_SAP_table_fields)
        self.dbselect_pushButton.clicked.connect(self.db_select)
        #Timers
        self.msg_timer = QTimer()
        self.msg_timer.setSingleShot(True)
        self.msg_timer.timeout.connect(self.clear_message)
        self.progressBarTimer = QTimer()
        self.progressBarTimer.timeout.connect(self.adjust_progress_bar)
        return

    def set_SAP_connection(self, conn):
        """
        Called by SAPLogonUI to pass the SAP connection string to this class
        """
        self._SAP_conn = conn
        if self._SAP_conn == None : self.logged_in = False #If login was cancelled
        else: self._logged_in = True

    def get_ini_db_name(self):
        """
        used by the SAPLogonUI to get the ini database location
        :return: ini database location.
        """
        return self._sqlite_ini_name

    def login_to_SAP(self):
        """
        Login to SAP. To do this a simple UI is presented to allow user input of credentials and target system. This
        avoids any hard coding of credentials and flexibility as to target system eg dev, QA, Prod.
        :return: None. Sets a class connection object used by other methods by calling the parent class (ie this one)
        set_SAP_connection method..
        """
        login_ui = SAPLogonUI(self)

    def displayTableFields(self):
        """
        Reads SAP function module to get the list of fields in specified SAP table and displays them in a
        line edit widget. Also sets the widget to allow multiple non contiguous selections. It is allowed to not
        display any table fields ie not use this method at all. In that case any extraction of data will extract
        all table fields.
        :return: Nothing
        """
        if str(self.SAPTable_lineEdit.text()) == '':
            msg = PyQt4.QtGui.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(PyQt4.QtGui.QMessageBox.Critical)
            msg.setInformativeText("Please enter a table name.")
            msg.exec_()
            return

        if not self._logged_in: self.login_to_SAP()
        #Check login worked or was not cancelled
        if not self._logged_in: return

        SAP_table = SAP_table_view(self._SAP_conn)

        self.Field_listWidget.setSelectionMode(3) #Allow multiple selections
        fields = SAP_table.read_SAP_table_spec(str(self.SAPTable_lineEdit.text()))
        names = []
        for field in fields: names.append (field['FIELDNAME'] + " (" + field['LENGTH'].lstrip('0') + ') ' +
            field['FIELDTEXT'])
        self.Field_listWidget.addItems(names)

    def extract(self):
        """
        Extract selected table columns or all columns if no selection was made. Checks arae made that
        a) A table was selected
        b) A proper login to SAP was established (if not a login option is presented)
        c) The selected column lengths do not total > 512 which is the max the SAP function module can handle
        d) returns the data and adds it to a table in a sqlite3 database
        :return:
        """
        #No table chosen
        if str(self.SAPTable_lineEdit.text()) == '':
            msg = PyQt4.QtGui.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(PyQt4.QtGui.QMessageBox.Critical)
            msg.setInformativeText("Please enter a table name.")
            msg.exec_()
            return

        if not self._logged_in: self.login_to_SAP()
        SAP_table = SAP_table_view(self._SAP_conn)
        #Check login worked or was not cancelled
        if not self._logged_in: return

        # Check Data length does not exceed 512
        #Case 1 Data fields were selected in the selection box
        if len(self.Field_listWidget.selectedItems()) > 0:
            chosen_lines = [str(el.text()) for el in self.Field_listWidget.selectedItems()]
            lengths_str = [el[el.find('(')+1 : el.find(')')] for el in chosen_lines]
            lengths = [int(el) for el in lengths_str]
        else :
            #Case 2 NO Data fields were selected in the selection box
            fields = SAP_table.read_SAP_table_spec(str(self.SAPTable_lineEdit.text()))
            lengths = []
            for field in fields: lengths.append (int(field['LENGTH'].lstrip('0')))
        tot_length = 0
        for i in lengths: tot_length += i
        if tot_length > 512:
            msg = PyQt4.QtGui.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(PyQt4.QtGui.QMessageBox.Critical)
            msg.setInformativeText("Selected fields add to " + repr(tot_length) + " which is > 512 max.")
            msg.exec_()
            return

        #Show progress bar
        self.progressBar.setVisible(True)
        self.progressBar.setTextVisible(False)
        self.progressBarTimer.start(self._progress_bar_interval)
        #Read the data
        table = str(self.SAPTable_lineEdit.text())
        max_rows = int(str(self.maxRows_lineEdit.text()))
        skip_rows = 0
        selection = [{'TEXT': str(self.Restriction_lineEdit.text())}]
        fields = []
        for el in self.Field_listWidget.selectedItems():
            table_field = str(el.text())
            fields.append(table_field[0:table_field.find(' ')])
        retrieve_data = '' #This means get data

        if self.Append_checkBox.isChecked(): append = True
        else: append = False
        self._execution_thread = Get_SAP_Table_Data(self._SAP_conn, table, max_rows, skip_rows, selection,
                                                    fields, retrieve_data, self._sqlite_db_name, append)
        #Thread events
        PyQt4.QtCore.QObject.connect(self._execution_thread, SIGNAL("SAP_extract_complete"), self.SAP_result_out)
        PyQt4.QtCore.QObject.connect(self._execution_thread, SIGNAL("SAP_extract_error"), self.SAP_error)
        PyQt4.QtCore.QObject.connect(self._execution_thread, SIGNAL("sqlite_error"), self.sqlite_error)
        PyQt4.QtCore.QObject.connect(self._execution_thread, SIGNAL("display_msg"), self.display_msg)
        self._execution_thread.start()
        return

    def SAP_result_out(self,result):
        """
        This method is connected to event "SAP_extract_complete" emitted by the _execution_thread doing the
        database read and load. It sets a screen message and removes the progress bar.
        :param result: Contains number of records returned from the SAP _execution_thread
        :return: nothing
        """
        num_records = result
        self.message_label.setText(str(num_records) + ' records returned.')
        self.progressBarTimer.stop()
        self.progressBar.setVisible(False)
        self.msg_timer.start(self._msg_display_time)
        return

    def SAP_error(self, message):
        """
        This method is connected to event "SAP_extract_error" emitted by the _execution_thread doing the
        database read and load. It raises an error dialog and sets a screen message.
        :param result: Contains a repr of the RFC error originating from pyrfc module
        :return: nothing
        """
        self.progressBarTimer.stop()
        self.progressBar.setVisible(False)
        #Dialog box warning of error and a message bar text
        msg = PyQt4.QtGui.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("RFC_READ_TABLE Error")
        msg.setIcon(PyQt4.QtGui.QMessageBox.Critical)
        msg.setInformativeText(message)
        msg.exec_()

        self.message_label.setText('Error in RFC Read.')
        self.msg_timer.start(self._msg_display_time)
        return

    def sqlite_error(self, message):
        """
        This method is connected to event "sqlite_error" emitted by the _execution_thread doing the
        database read and load. It raises an error dialog and sets a screen message.
        :param message: Contains a repr of the sqlite error
        :return: nothing
        """
        self.progressBarTimer.stop()
        self.progressBar.setVisible(False)
        #Dialog box warning of error and a message bar text
        msg = PyQt4.QtGui.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Sqlite3 Error")
        msg.setIcon(PyQt4.QtGui.QMessageBox.Critical)
        msg.setInformativeText(message)
        msg.exec_()

        self.message_label.setText('Error in sqlite database load.')
        self.msg_timer.start(self._msg_display_time)
        return

    def display_msg (self,msg):
        """
        This method is connected to event "display_msg" emitted by the _execution_thread doing the
        database read and load. It displays informational messages passed from time to time by that thread
        for display on the gui.
        :param msg: Contains the text message passed from the thread for display
        :return: nothing
        """
        self.message_label.setText(msg)
        self.msg_timer.start(self._msg_display_time)
        return

    def reset_SAP_table_fields(self):
        """
        Reset contents of the widget containing SAP table field information. Done if SAP table name selected changes
        :return: Nothing
        """
        self.Field_listWidget.clear()
        self.Restriction_lineEdit.clear()
        return

    def db_select(self):
        """
        Allow selection of a database location and name.
        :return: Nothing
        """
        db = PyQt4.QtGui.QFileDialog(parent=None)
        db.setFileMode(PyQt4.QtGui.QFileDialog.Directory)
        db.exec_()
        self.DBName_lineEdit.setText(str(db.selectedFiles()[0]) + os.sep + self._db_file_name)
        conn = sqlite3.connect(self._sqlite_ini_name)
        c = conn.cursor()
        if self.SAPTable_lineEdit.text() != '':
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('DB_NAME',
                str(self.DBName_lineEdit.text())))
            self._sqlite_db_name = str(self.DBName_lineEdit.text())
        else:
            msg = PyQt4.QtGui.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(PyQt4.QtGui.QMessageBox.Critical)
            msg.setInformativeText("You did not select a table.")
            msg.exec_()
            return
        conn.commit()
        conn.close()

    def exit(self):
        conn = sqlite3.connect(self._sqlite_ini_name)
        c = conn.cursor()
        if self.SAPTable_lineEdit.text() != '':
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('LAST_TABLE',
                str(self.SAPTable_lineEdit.text())))
        if self.maxRows_lineEdit.text() != '':
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('MAX_ROWS',
                str(self.maxRows_lineEdit.text())))
        conn.commit()
        conn.close()
        sys.exit(0)

    def clear_message(self):
        """
        Purely timer driven to remove status text after displaying for a few seconds. See _otherGUISetup method
        :return: Nothing
        """
        self.message_label.setText('')

    def adjust_progress_bar(self):
        """
        Purely timer driven to adjust progress shown on progress bar. See _otherGUISetup method.
        :return: Nothing
        """
        val = self.progressBar.value()
        if val < 10: self.progressBar.setValue(val + 1)
        else : self.progressBar.setValue(0)
        return

if __name__ == '__main__':
    import sys
    app = PyQt4.QtGui.QApplication(sys.argv)
    MainWindow = PyQt4.QtGui.QDialog()
    ui = SAPTableExtractorGUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
#TODO Allow selection of database + sqlite3 table.
#TODO If append, what happens if table structure changed.

