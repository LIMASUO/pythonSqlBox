# SQL Interpreter

import sqlite3 as sql

class SqlBox():
    __all__ = ['close','connect','in_']
    ERROR_PROMPT = "AN ERROR OCCURED|"
    
    def __init__(self, name):
        #- GET DATABASE NAME -#
        self.db_name = name

        #-  ADD FILE FORMAT  -# 
        if self.db_name[-3:] != '.db':
            self.db_name += '.db'
    
        #- DECLARE CONNeCTION VARIABLES -#
        self.conn = None
        self.cur = None
        
        #- CONNECT TO FILE -#
        self.connect()
        #-------------------#
    
    def close(self):
        """close the connection to the database."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cur = None

    def connect(self):
        """ connect to the database """
        if not self.conn:
            try:                
                self.conn = sql.connect(self.db_name)
                self.cur = self.conn.cursor()
            except sql.OperationalError:
                return SqlBox.ERROR+"UNABLE TO OPEN: {}".format(self.db_name) 
        
        
    def in_(self, text):
        """ Give SqlBox a command. If there is an output it is returned;
        else none is returned."""
        #- OPEN CONNECTION -# 
        self.connect()
        try:
            if sql.complete_statement(text):
                try:
                    response = self._out_(self.cur.execute(text))
                    self.conn.commit()
                    return response
                    
                except sql.OperationalError:
                    return SqlBox.ERROR_PROMPT +"OPERATIONAL"
            else:
                return SqlBox.ERROR_PROMPT +"INCOMPLETE"
        #- CLOSE THE CONNECTION
        finally:
            self.close()
            
    def _out_(self, response):
        """Manage the output of results"""
        # SHOULD A STRING BE RETURNED OR THE OBJECT?
        data = response.fetchall()
        if data:
            return data
        else:
            return None
    
