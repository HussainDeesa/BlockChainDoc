from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class ApprovedByModel:
    def __init__(self, approvedByID = '',approvedByName = ''):
        self.approvedByID = approvedByID
        self.approvedByName = approvedByName
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ApprovedBy ORDER BY approvedByName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ApprovedByModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT approvedByID, approvedByName FROM ApprovedBy ORDER BY approvedByName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ApprovedByModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ApprovedBy WHERE approvedByID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = ApprovedByModel(dbrow[0],dbrow[1])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.approvedByID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO ApprovedBy (approvedByID,approvedByName) VALUES(?,?)"
        cursor.execute(sqlcmd1, (obj.approvedByID,obj.approvedByName))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE ApprovedBy SET approvedByName = ? WHERE approvedByID = ?"
        cursor.execute(sqlcmd1,  (obj.approvedByName,obj.approvedByID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM ApprovedBy WHERE approvedByID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

