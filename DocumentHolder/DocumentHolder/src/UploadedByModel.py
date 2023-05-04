from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class UploadedByModel:
    def __init__(self, uploadedByID = '',uploadedByName = ''):
        self.uploadedByID = uploadedByID
        self.uploadedByName = uploadedByName
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM UploadedBy ORDER BY uploadedByName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = UploadedByModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT uploadedByID, uploadedByName FROM UploadedBy ORDER BY uploadedByName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = UploadedByModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM UploadedBy WHERE uploadedByID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = UploadedByModel(dbrow[0],dbrow[1])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.uploadedByID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO UploadedBy (uploadedByID,uploadedByName) VALUES(?,?)"
        cursor.execute(sqlcmd1, (obj.uploadedByID,obj.uploadedByName))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE UploadedBy SET uploadedByName = ? WHERE uploadedByID = ?"
        cursor.execute(sqlcmd1,  (obj.uploadedByName,obj.uploadedByID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM UploadedBy WHERE uploadedByID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

