'''
Created on 1 Dec 2019

@author: U104675
'''
import threading

class SAP_thread(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, SAP_unthreaded, SAP_spec, sqlite_db_name, append, publisher):
        '''
        Constructor:
        @param SAP_Unthreaded: An instance of class SAP_to_sqlite_table (in package SAPConnection.Extractions at time of writing)
        @param publisher: publisher class to send messages to for distribution to subscribers
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
        '''
        threading.Thread.__init__(self)
        self._SAP_unthreaded = SAP_unthreaded
        self._sqlite_db_name = sqlite_db_name
        self._append = append
        self._retrieval_spec = SAP_spec
        self._publisher = publisher
               
    def run(self):
        #TODO: Trap errors ABAPApplicationError
        self._publisher.dispatch("Date extraction and storage underway")
        self._SAP_unthreaded.get_and_store_data(
                                          self._SAP_unthreaded, 
                                          self._retrieval_spec,
                                          self._sqlite_db_name,
                                          self._append,
                                          False
                                          )
        self._publisher.dispatch("Date extraction and storage complete")   
        
        
        