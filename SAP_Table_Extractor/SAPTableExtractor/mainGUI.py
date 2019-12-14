'''
Created on 1 Dec 2019

@author: U104675
'''
import tkinter as tk
from tkinter import messagebox, filedialog
from SAPTableExtractor.loginGUI import loginGUI
import sqlite3
from SAPTableExtractor.SAP_thread import SAP_thread
from tkinter.filedialog import FileDialog
import os
from SAPTableExtractor.publisher import publisher
from pyrfc._exception import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError

class mainGUI(tk.Frame):
    def __init__(self, master=None):
        #GUI initialisations
        super().__init__(master)
        self._master = master
        self.borderwidth = 30
        self._master.title('SAP Table Extractor')
        #Ensure contents of frame resize with the frame
        self._master.rowconfigure(3, weight=1)
        self._master.columnconfigure(0, weight=1)
        self._master.columnconfigure(1, weight=2)
        self._master.minsize(400,530)
        #Setup some application required data values
        self._sqlite_db_name = 'SAP_tables.db'
        self._sqlite_ini_name = 'ini.db'
        self._logged_in = False
        self._SAP_conn = None
        self._FM = 'RFC_READ_TABLE'
        #Set up initialisations db and table if required
        conn = sqlite3.connect(self._sqlite_ini_name)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS SETTINGS (KEY TEXT PRIMARY KEY, VALUE TEXT)")
        #Subscribe to message publisher
        self._msg_publisher = publisher()
        self._msg_publisher.register(self, self.handle_messages)
        #Set the GUI up - must be last in constructor since method relies on constructor setup 
        self.setupGUI()
        
    def setupGUI(self):
        #Select Table Area
        label_table_name = tk.Label(self._master,text='SAP Table').grid(row=0, column=0, sticky='W')
        self._entry_table_name = tk.Entry(self._master)
        self._entry_table_name.grid(row=0, column=1, sticky='WE', columnspan=4)
        label_max_rows = tk.Label(self._master,text='Max Rows').grid(row=1, column=0, sticky='W')
        self._max_rows_var = tk.StringVar()
        self._max_rows_var.set('50000000')
        self._entry_max_rows = tk.Entry(self._master, textvariable=self._max_rows_var)
        self._entry_max_rows.grid(row=1, column=1, sticky='WE')
        #Select Fields Area
        label_select_fields = tk.Label(self._master,text='Select Fields (Max. 512 Total Length)').grid(row=2, column=0, sticky='W', columnspan=5)
        scrollbar_fields = tk.Scrollbar(self._master,orient=tk.VERTICAL)
        self._listbox_fields = tk.Listbox(self._master,selectmode='extended', yscrollcommand=scrollbar_fields.set)
        self._listbox_fields.grid(row=3, column=0,sticky='NSWE', columnspan=5)
        scrollbar_fields.config(command=self._listbox_fields.yview)
        scrollbar_fields.grid(row=3, column=5,sticky='NES')
        button_show_fields = tk.Button(self._master, text='Show Fields', command=self.showFields).grid(row=4, column=4, sticky='E')
        #ABAP Area
        label_ABAP = tk.Label(self._master,text="ABAP Restriction (eg. MATL_TYPE = 'HALB') - max 72 chars per line").grid(row=5, column=0, sticky='W', columnspan=5)
        self._entry_ABAP_1 = tk.Entry(self._master)
        self._entry_ABAP_1.grid(row=6, column=0, sticky='WE', columnspan=5)
        self._entry_ABAP_2 = tk.Entry(self._master)
        self._entry_ABAP_2.grid(row=7, column=0, sticky='WE', columnspan=5)
        self._entry_ABAP_3 = tk.Entry(self._master)
        self._entry_ABAP_3.grid(row=8, column=0, sticky='WE', columnspan=5)
        #Database area
        label_db_name = tk.Label(self._master,text="Output Database Name").grid(row=10, column=0, sticky='W', columnspan=4)
        self._entry_db_name = tk.Entry(self._master)
        self._entry_db_name.grid(row=11, column=0, sticky='WE', columnspan=5)  
        label_db_name = tk.Label(self._master,text="Output Database Table Name").grid(row=12, column=0, sticky='W', columnspan=4)
        self._entry_db_table = tk.Entry(self._master)
        self._entry_db_table.grid(row=13, column=0, sticky='WE', columnspan=5)                  
        self._checkbutton_onoff = tk.IntVar()  
        self._checkbutton_append = tk.Checkbutton(self._master, text='Append to existing table?', variable=self._checkbutton_onoff)
        self._checkbutton_append.grid(row=14, column=0, sticky='W', columnspan=4)
        button_choose_db = tk.Button(self._master, text='Choose Database', command=self.chooseDb).grid(row=14, column=4, sticky='E',pady=5)
        #Main Control Button Area
        button_extract = tk.Button(self._master, text='Extract Fields', command=self.extractFields).grid(row=15, column=3, sticky='E')  
        button_exit = tk.Button(self._master, text='Exit/Cancel', command=self.exit).grid(row=15, column=4, sticky='E')   
        #message area
        self._msg_bar_var = tk.StringVar()
        label_msg_bar = tk.Label(self._master,textvariable=self._msg_bar_var, fg='grey').grid(row=16, column=0, sticky='W', columnspan=5)
        self._msg_bar_var.set("No Message")
        #Initial focus
        self._entry_table_name.focus()  
        
        #Populate some fields from cached values
        conn = sqlite3.connect(self._sqlite_ini_name)
        c = conn.cursor()
        #Last Max rows to extract setting but ensure there is a default if non set.
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='MAX_ROWS'")
        for r in row: 
            if r[0] != '': self._max_rows_var.set(r[0])
        #sqlite3 database location and name
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='LAST_DB_NAME'")
        for r in row:
            if r[0] != '':
                self._entry_db_name.delete(0, tk.END) 
                self._entry_db_name.insert(0, r[0])
        conn.close()
    
    def showFields(self):
        """Populate list box with the fields details of the required table
        """
        #Was a table selected
        table_name = self._entry_table_name.get()
        if table_name.strip() == "":
            tk.messagebox.showerror('Error', 'Please enter a table name')
            self._entry_table_name.focus()
            return
            
        if self._SAP_conn is None:
            self.login()
            return
        else:
            try:
                result = self._SAP_conn.call(self._FM, QUERY_TABLE = table_name, NO_DATA = 'NO', ROWCOUNT = 0,
                                         ROWSKIPS = 0,  OPTIONS =  [], FIELDS = [])
            except(ABAPApplicationError) as e:
                self._msg_publisher.dispatch("error", "ABAPApplicationError " + '\n' + e.key + " : " + e.message)
                return
            except(ABAPRuntimeError):
                self._msg_publisher.dispatch("error", "ABAPRuntimeError " + '\n' + e.key + " : " + e.message)
                return
            except(CommunicationError):
                self._msg_publisher.dispatch("error", "CommunicationError " + '\n' + e.key + " : " + e.message)
                return
            #Display record specification
            self._listbox_fields.delete(0,tk.END)
            for field_info in result['FIELDS']:
                self._listbox_fields.insert(tk.END,
                    field_info['FIELDNAME'] +
                    " - " + field_info['FIELDTEXT'] +
                    " (" + field_info['LENGTH'] +")")
        return

    def extractFields(self):
        """
        Extract selected table columns or all columns if no selection was made. Checks are made that
        a) A table was selected
        b) A proper login to SAP was established (if not a login option is presented)
        c) The selected column lengths do not total > 512 which is the max the SAP function module can handle
        d) returns the data and adds it to a table in a sqlite3 database
        @return: Nothing
        """ 
        #Was a table selected
        SAP_table_name = str.upper(self._entry_table_name.get()) #SAP FM does not like lower case table name
        if SAP_table_name.strip() == "":
            tk.messagebox.showerror('Error', 'Please enter a table name')
            self._entry_table_name.focus()
            return        
    
        #Check we are logged in
        if self._SAP_conn is None:
            self.login()
            return
        
        # Check Data length does not exceed 512
        #Case 1 Data fields were selected in the selection box
        tbl_field_names = []
        if len(self._listbox_fields.curselection()) > 0:
            chosen_lines = [str(el) for el in self._listbox_fields.curselection()]
            chosen_data = [self._listbox_fields.get(i) for i in chosen_lines]
            tbl_field_names = [el[0 : el.find(' ')] for el in chosen_data]
            lengths_str = [el[el.rfind('(')+1 : el.rfind(')')] for el in chosen_data]
            lengths = [int(el.lstrip('0')) for el in lengths_str]
        else :
            #Case 2 NO Data fields were selected in the selection box
            result = self._SAP_conn.call(self._FM, QUERY_TABLE = SAP_table_name, NO_DATA = 'NO', ROWCOUNT = 0,
                         ROWSKIPS = 0,  OPTIONS =  [], FIELDS = [])
            lengths = []
            for field in result['FIELDS']: lengths.append (int(field['LENGTH'].lstrip('0')))
            tbl_field_names = [field_spec['FIELDNAME'] for field_spec in result['FIELDS']]
        tot_length = 0
        for i in lengths: tot_length += i
        if tot_length > 512:
            tk.messagebox.showerror('Error', 'Selected fields have total length of ' + repr(tot_length) + ': only 512 is allowed')
            return
        else:
            #tk.messagebox.showinfo('Information', repr(tot_length) + ' data length selected')
            #Read the data
            sqlite_db_name = str(self._entry_db_name.get())
            if sqlite_db_name.strip() == '': sqlite_db_name = self._sqlite_db_name
            max_rows = int(str(self._entry_max_rows.get()))
            selection = [{'TEXT': str(self._entry_ABAP_1.get())}]
            if str(self._entry_ABAP_2.get()) != '': 
                selection.append({'TEXT': str(self._entry_ABAP_2.get())})
            if str(self._entry_ABAP_3.get()) != '': 
                selection.append({'TEXT': str(self._entry_ABAP_3.get())})                         ,

            retrieve_data = '' #This means get data
    
            if self._checkbutton_onoff.get() == 1: append = True
            else: append = False
            #Initiate thread doing the SAP read and store to sqlite
            SAP_spec = {SAP_table_name : {'MAXROWS': max_rows,
                    'FIELDS': tbl_field_names,
                    'SELECTION': selection,
                    'RETRIEVEDATA': retrieve_data}}
            if self._entry_db_table.get() == '': sqlite_table = SAP_table_name
            else: sqlite_table = self._entry_db_table.get()

            data_process_thread = SAP_thread(self._SAP_conn,
                                             SAP_spec, 
                                             sqlite_db_name, 
                                             sqlite_table, 
                                             append,
                                             self._msg_publisher)
            self._msg_bar_var.set("Data extraction in process")
            data_process_thread.start()
            return
       
              
    def chooseDb(self):
        """Present file dialog and choose a db file
        """
        cwd = os.getcwd()
        f = filedialog.askopenfilename(initialdir=cwd)
        if f != '':
            self._entry_db_name.delete(0, tk.END)
            self._entry_db_name.insert(0, f)
        return
    
    def exit(self):
        """logout of SAP and close this GUI and dependent widgets
        """
        if self._SAP_conn is None: #We did not login to SAP
            pass
        else:
            self._SAP_conn.close()
        #Cache some values for next time    
        conn = sqlite3.connect(self._sqlite_ini_name)
        c = conn.cursor()
        if self._entry_db_name.get() != '':
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('LAST_DB_NAME',
                str(self._entry_db_name.get())))
        if self._max_rows_var.get() != '':
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('MAX_ROWS',
                str(self._max_rows_var.get())))
        conn.commit()
        conn.close()
        self._master.destroy()
        
    def login(self):
        """
        Login to SAP. To do this a simple UI is presented to allow user input of credentials and target system.
        LoginGUI sets a SAP "connection" object with all the methods required to access the SAP table. This is 
        passed back her by loginGUI calling method set_SAP_connection in this class.

        :return: None. 
        """
        lo = loginGUI(self)
        #TODO: Figure out why I need to call this method here and cannot do it within loginGUI class
        lo.fill_login_parms()
        return
    
    def get_ini_db_name(self):
        """
        Allows the login ui to get the sqlite db .ini it needs to store last selections to
        """
        return self._sqlite_ini_name
    
    def set_SAP_connection(self, connection):
        """
        Allows login gui to set the SAP object and pass it back to main parent
        """
        self._SAP_conn = connection
        return
    
    def handle_messages(self, message_type, message):
        '''
        This method is called by publisher class whenever it has a message the application needs to know about.
        This method reacts according to the type of error message. Information is placed in the
        message bar error message is displayed in a popup.
        '''
        if message_type == 'information':
            self._msg_bar_var.set(message)
        elif message_type == 'error':
            self._msg_bar_var.set('ERROR')
            tk.messagebox.showerror('Error', message)
        return
        
if __name__ == '__main__':
    #Start the GUI
    root = tk.Tk()
    app = mainGUI(master=root)
    app.mainloop()