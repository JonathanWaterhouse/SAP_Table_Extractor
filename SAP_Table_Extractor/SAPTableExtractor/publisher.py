'''
Created on 13 Dec 2019

@author: U104675
'''

class publisher(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor creating a dictionary of subscribers which will be keyed on object with value the callback method
        '''
        self._subscribers = dict()
        
    def register(self, who, callback=None):
        '''
        Register an object to receive upates
        @param who: the object being registered
        @param callback: the method within the object registered to call and pass messgae back to.
            If no callback is sent this defaults to method update which it is assumed exists
        '''
        if callback is None: callback = getattr(who, 'update')
        self._subscribers[who] = callback
        
    def unregister(self, who):
        '''
        Unregister an object from receiving updates
        @param who: The object to unregister
        '''
        del self._subscribers[who]
        
    def dispatch(self, message_type, message):
        '''
        Called by the publisher with a message to be passed to all subscribers
        @param message: the messgae to be passed to subscribers.
        @param message_type: defines what type of message this is eg informational, error etc
        '''
        for subscriber, callback in self._subscribers.items():
            callback(message_type, message)
        
        
    
        
        