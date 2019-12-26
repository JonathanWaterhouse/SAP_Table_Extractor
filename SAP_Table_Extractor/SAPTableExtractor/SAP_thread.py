'''
Created on 1 Dec 2019

@author: U104675
'''
import threading
import sqlite3
from pyrfc._exception import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError

class SAP_thread(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, SAP_conn, SAP_spec, sqlite_db_name, sqlite_tab_name, append, publisher):
        '''
        Constructor:
        @param SAP_conn: pyrfc Connection object passed from main gui logon
        @param publisher: publisher class to send messages to for distribution to subscribers (eg the gui)
        @param SAP_spec: extraction specification in format
            {SAP_table_name : {'MAXROWS': max_rows,
                    'FIELDS': tbl_field_names,
                    'SELECTION': selection,
                    'RETRIEVEDATA': retrieve_data}}
                tbl_field_names is a list of field names from SAP_table_name
                retrieve_data blank means retrieve, 'N' means no retrieval of data, if not only record definitions are retrieved. 1 character.
                selection A list of dictionaries of SAP open sql statements to limit the extraction.
                    Example format : selection = [{'TEXT' : "DTA = 'ZO00014'"}]
        @param sqlite_db_name: fully qualified name of sqlite database. Could be just sqlite db file name and db will be in program path
        @param sqlite_tab_name: table name to populate in sqlite database
        '''
        threading.Thread.__init__(self)
        self._SAP_conn = SAP_conn
        self._sqlite_db_name = sqlite_db_name
        self._sqlite_tab_name = sqlite_tab_name
        self._append = append
        self._retrieval_spec = SAP_spec
        self._publisher = publisher
        self._FM = 'RFC_READ_TABLE'


    #def read_SAP_table(self, table, maxrows, skip_rows, selection, fields, retrieve_data):
    def read_SAP_table(self, retrieval_spec):
        """
        Return selected data from a table using SAP FM RFC_READ_TABLE. Python relies on SAP pyrfc module to do this
        and installation of nwrfcsdk from SAP. This is described here http://sap.github.io/PyRFC/install.html
        @param: retrieval_spec: See constructor for a definition

        @return: The RFC_READ_TABLE FM returns a dictionary with 3 entries, keyed on values "DATA", "FIELDS", "OPTIONS"
            "OPTIONS" specifies the options that were chosen in the selection. It is a list of dictionaries in the same
            format as the "selection" parameter described earlier

            "FIELDS" gives a fields spec for each field returned. It only returns specs for fields requested in the "fields"
            option described above. The format is a list of dictionaries each one having format like
            {u'FIELDTEXT': u'Data Source or Target for Status Manager', u'TYPE': u'C', u'LENGTH': u'000045', u'FIELDNAME': u'DTA', u'OFFSET': u'000000'}

            "DATA" is the returned data payload and is a list of dictionaries (one per record returned) formatted like
            {u'WA': u'ZO00014                                      ODSO  201208142012081405262..........}
            In order to know which part of he record contains a given field you need to use the "FIELDS" output to get
            field positions in the record.
        """
        for tab in retrieval_spec.keys():
            #Get incoming field list into correct format for RFC call [{'FIELDNAME': 'DTA'}, {'FIELDNAME':'DTA_TYPE'}]
            SAP_fld_spec = []
            for fld in retrieval_spec[tab]['FIELDS']: SAP_fld_spec.append(dict(FIELDNAME = fld))
            result = self._SAP_conn.call(self._FM, 
                                         QUERY_TABLE = tab, 
                                         NO_DATA = retrieval_spec[tab]['RETRIEVEDATA'], 
                                         ROWCOUNT = retrieval_spec[tab]['MAXROWS'],
                                         ROWSKIPS = 0,  
                                         OPTIONS =  retrieval_spec[tab]['SELECTION'], 
                                         FIELDS = SAP_fld_spec)
            return result

    def update_sqlite_table(self, sqlite_db_name, table, append, RFC_READ_TABLE_input):
        """
        Update sqlite database
        @param sqlite_db_name: database name as known to windows eg database.db
        @param table: table to create and populate in database.db
        @param RFC_READ_TABLE_input: the output of RFC_READ_TABLE having format defined in method read_SAP_table
        @return: nothing. Result of running this method is a sqlite db with newly filled table.
        """
        RFC_out = RFC_READ_TABLE_input
        #Create the table in local sqlite database
        sqlite_conn = sqlite3.connect(sqlite_db_name)
        c = sqlite_conn.cursor()
        #Delete table if already exists
        if not append:
            c.execute('DROP TABLE IF EXISTS ' + table)
            #Define table structure from the SAP "FIELDS" Information
            sql_stmt_field_defs = []
            for field in RFC_out['FIELDS']:
                sql_stmt_field_defs.append('[' + field['FIELDNAME'] + ']' + ' CHAR(' + field['LENGTH'].lstrip('0') + ')')
            sql_stmt = 'CREATE TABLE ' + table + ' (' + ','.join(sql_stmt_field_defs) + ')'
            c.execute(sql_stmt)

        ##Now load the data
        #Create a list of tuples of start and ends of fields in SAP supplied records
        field_boundaries = []
        i = 0
        for field in RFC_out['FIELDS']:
            field_boundaries.append((i, i+ int(field['LENGTH']))) #A tuple
            i += int(field['LENGTH'])

        #Process the SAP datarecords, defining fields according to field boundaries
        record_tup = [] #List of 2-tuples
        payload = ''
        for record in RFC_out['DATA']:
            payload = record['WA']
            record_tup.append(tuple([payload[bound[0]: bound[1]].strip() for bound in field_boundaries]))

        #Build sql to post to the sqlite database table
        sql_stmt_field_defs = []
        for field in RFC_out['FIELDS']:
            sql_stmt_field_defs.append('[' + field['FIELDNAME'] + ']')
        val_qmarks = ['?' for el in sql_stmt_field_defs]
        sql_stmt = 'INSERT INTO ' + table + ' (' + ','.join(sql_stmt_field_defs) + ') VALUES (' + ','.join(val_qmarks) + ')'
        #print sql_stmt
        c.executemany(sql_stmt,record_tup)

        #We are done. Commit and close sqlite connection
        sqlite_conn.commit()
        sqlite_conn.close()          

    def run(self):
        self._publisher.dispatch("information", "SAP Data extraction underway")

        #SAP extraction
        try:        
            result = self.read_SAP_table(self._retrieval_spec)
            num_recs = len(result['DATA'])
            self._publisher.dispatch("information", "SAP Data extraction of " + repr(num_recs) + " records complete")
        except(ABAPApplicationError) as e:
            self._publisher.dispatch("error", "ABAPApplicationError " + '\n' + e.key + " : " + e.message)
            return
        except(ABAPRuntimeError) as e:
            self._publisher.dispatch("error", "ABAPRuntimeError " + '\n' + e.key + " : " + e.message)
            return
        except(CommunicationError):
            self._publisher.dispatch("error", "CommunicationError " + '\n' + e.key + " : " + e.message)
            return             
                   
        #Output to sqlite
        try:
            self._publisher.dispatch("information", "Data input to sqlite table starting")
            self.update_sqlite_table(self._sqlite_db_name, '[' + self._sqlite_tab_name + ']', self._append, result)

            num_recs = len(result['DATA'])
            self._publisher.dispatch("information", "Data input to sqlite table of " + repr(num_recs) + " records complete")
        except (sqlite3.Error):
            self._publisher.dispatch("error", "Sqlite3.Error " + '\n' + e.key + " : " + e.message)
            return 
            
        return  
   
        
        