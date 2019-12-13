'''
Created on 1 Dec 2019

@author: U104675
'''
import threading

class SAP_thread(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, SAP_unthreaded, SAP_spec, sqlite_db_name, append):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self._SAP_unthreaded = SAP_unthreaded
        self._sqlite_db_name = sqlite_db_name
        self._append = append
        self._retrieval_spec = SAP_spec
               
    def run(self):
        self._SAP_unthreaded.get_and_store_data(
                                          self._SAP_unthreaded, 
                                          self._retrieval_spec,
                                          self._sqlite_db_name,
                                          self._append,
                                          False
                                          )
        
        
        