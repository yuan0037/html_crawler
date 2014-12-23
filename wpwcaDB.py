import sqlite3


#a class for sqlite database

class wpwcaDB():
    """
    A database to keep track of the URLs parsed
    """

    def __init__(self, **kwargs):       

        self.filename = kwargs.get('filename', 'wpwca.db')
        self.table = kwargs.get('table', 'url')
        
        self.db = sqlite3.connect(self.filename)
        self.db.row_factory = sqlite3.Row        
        self.db.execute('''CREATE TABLE IF NOT EXISTS {}
                            (urlID INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, level INT,
                            count INTEGER)'''.format(self.table))
                  
    def __iter__(self):
        #Return generator object with dicts of entire DB contents
        cursor = self.db.execute('SELECT * FROM {} ORDER BY urlID'.format(self.table))
        for row in cursor: yield dict(row)
       
    def get_data_for_all(self):
        #return a generator of rows
        cursor = self.db.execute('''SELECT urlID, url, level, count
                                   FROM {} order by level'''.format(self.table))
        for row in cursor:
            yield dict(row)
    
            
    def is_url_exist(self, url):

        print ("select * FROM {0} where url='{1}'".format(self.table, url))
        cursor = self.db.execute("select * FROM {0} where url='{1}'".format(self.table, url))
        if (len(cursor.fetchall())>0):
            return True
        else:
            return False
    
    def _update_data_for_url(self, id, count):
        self.db.execute('''UPDATE {} set COUNT=? where urlID=?'''.format(self.table), (count,id))
        self.db.commit()
               
    def _insert_data_for_url(self, url, level):
        self.db.execute('''INSERT INTO {} (url, level)
                                VALUES (?, ?)'''.format(self.table), (url,level))
        self.db.commit()
        
    def _insert_fulldata_for_url(self, url, level, count):
        #insert a record with full url, level and count fields
        self.db.execute('''INSERT INTO {} (url, level, count)
                                VALUES (?,?,?)'''.format(self.table), (url,level, count))
        self.db.commit()
        
    def clear(self):
        #Clears out the database by dropping the current table
        self.db.execute('DROP TABLE IF EXISTS {}'.format(self.table))
    
    def createtable(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS {}
                        (urlID INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, level INT,
                        count INTEGER)'''.format(self.table))  
        self.db.commit()  
      
    def close(self):
        #Safely close down the database
        self.db.close()


def test():
    """
    A simple test routine
    """
    # create/clear/close to empty db before testing
    db = wpwcaDB(filename = 'test.db', table = 'Test')
    db.clear()
    db.close()
    
    # create db for testing
    db = wpwcaDB(filename = 'test.db', table = 'Test')
    
    # verify the db is empty
    if dict(db) != {}:
        print('Error in wpwcaDB test(): Database is not empty')

    # add data for current date
    try:
        db._insert_data_for_url("http://www.cbc.ca", 2)        
    except:
        print('ERROR in wpwcaDB.test(): Could not update data')
    
    if (db.is_url_exist("http://www.cbc.ca")):
        print ("found it")
    for entry in db:
        print(entry)
    
    db.close()

# if this module is run as main it will execute the test routine    

if __name__ == "__main__": test()