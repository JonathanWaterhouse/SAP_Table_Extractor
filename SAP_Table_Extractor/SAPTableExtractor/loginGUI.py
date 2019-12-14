'''
Created on 1 Dec 2019

@author: U104675
'''
import tkinter as tk
from tkinter import messagebox
#import COMSAPConn as SC
import pyrfc
import sqlite3
from pyrfc._exception import LogonError

#class loginGUI(tk.Frame):
class loginGUI(tk.Toplevel):
    '''
    classdocs
    '''
    def __init__(self, parent_gui):
        '''
        Constructor. Sets up Gui and populates last used parameters from sqlite db
        
        @param parent_gui: GUI calling this login popup. Gives access to parent gui methods 
                        in particular to pass back SAP object and get the ini db name
        '''
        self._parent_gui = parent_gui
        #Setup GUI
        super().__init__(parent_gui)
        self.title('SAP Logon')
        self.minsize(250,200)
        label_user = tk.Label(self,text='User')
        self.entry_user = tk.Entry(self)
        label_pw = tk.Label(self,text='Password')
        self.entry_pw = tk.Entry(self, show='*')
        label_system = tk.Label(self,text='System')
        self.entry_system = tk.Entry(self)
        label_client = tk.Label(self,text='Client')
        self.entry_client = tk.Entry(self)
        label_lang = tk.Label(self,text='Language')
        self.entry_lang = tk.Entry(self)
        label_group = tk.Label(self,text='Group')
        self.entry_group = tk.Entry(self)
        label_msgsrvr = tk.Label(self,text='Message Server')
        self.entry_msgsrvr = tk.Entry(self)
        button_exit = tk.Button(self, text='Exit/Cancel', command=self.exit)
        button_login = tk.Button(self, text='Login', command=self.login)
        #Layout
        label_user.grid(row=0, column=0, sticky='W')
        self.entry_user.grid(row=0, column=1, sticky='WE')
        label_pw.grid(row=1, column=0, sticky='W')
        self.entry_pw.grid(row=1, column=1, sticky='WE')
        label_system.grid(row=2, column=0, sticky='W')
        self.entry_system.grid(row=2, column=1, sticky='WE')
        label_client.grid(row=3, column=0, sticky='W')
        self.entry_client.grid(row=3, column=1, sticky='WE')
        label_lang.grid(row=4, column=0, sticky='W')
        self.entry_lang.grid(row=4, column=1, sticky='WE')
        label_group.grid(row=5, column=0, sticky='W')
        self.entry_group.grid(row=5, column=1, sticky='WE')
        label_msgsrvr.grid(row=6, column=0, sticky='W')
        self.entry_msgsrvr.grid(row=6, column=1, sticky='WE')
        button_exit.grid(row=8, column=0, sticky='E')
        button_login.grid(row=8, column=1, sticky='E')
        
        #Make dialog modal
        self.focus_set() #TODO: Make login dialog modal - not working now.
        #self.grab_set()
        #if not self.initial_focus:
        #    self.initial_focus = self
        #entry_user.focus()
        
        #Initial focus
        self.entry_user.focus()  
     
        
        return
    
    def fill_login_parms(self):    
        #Attempt to set up parameters used from last login from ini database
        conn = sqlite3.connect(self._parent_gui.get_ini_db_name())
        c = conn.cursor()
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='CLIENT'")
        for r in row: self.entry_client.insert(0,r[0])
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='LANGU'")
        for r in row: self.entry_lang.insert(0,r[0])
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='MSG_SERVER'")
        for r in row: self.entry_msgsrvr.insert(0,r[0])
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='SYSTEM'")
        for r in row: self.entry_system.insert(0,r[0])
        row = c.execute("SELECT VALUE FROM SETTINGS WHERE KEY ='GROUP'")
        for r in row: self.entry_group.insert(0,r[0])
        conn.close()
        return
        
    def login(self):
        #SAP = SC.SAP_to_sqlite_table()
        client = str(self.entry_client.get())
        user = str(self.entry_user.get())
        passwd = str(self.entry_pw.get())
        lang = str(self.entry_lang.get())
        mshost = str(self.entry_msgsrvr.get())
        sysid = str(self.entry_system.get())
        group = str(self.entry_group.get())
        params = {'client' : client, 'user' : user, 'passwd' : passwd , 'lang' : lang,
                  'mshost' : mshost, 'sysid' : sysid, 'group' : group}
        try:
            #SAP.login_to_SAP(params)
            SAP_conn = pyrfc.Connection(**params)
            #Store last used values for later use
            conn = sqlite3.connect(self._parent_gui.get_ini_db_name())
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('CLIENT',
                str(self.entry_client.get())))
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('LANGU',
                str(self.entry_lang.get())))
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('MSG_SERVER',
                str(self.entry_msgsrvr.get())))
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('SYSTEM',
                str(self.entry_system.get())))
            c.execute("INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?,?)", ('GROUP',
                str(self.entry_group.get())))
            conn.commit()
            conn.close()
            #Pass back the SAP object to parent GUI
            self._parent_gui.set_SAP_connection(SAP_conn)
            #Finish up
            self.destroy()
            return
        
        except(LogonError) as e:
            tk.messagebox.showerror('Error', 'Unable to login to SAP' + '\n' + e.key + ' : ' + e.message)
            #self._parent_gui.set_SAP_connection(None)
            return
        
    def exit(self):
        self.destroy()
        