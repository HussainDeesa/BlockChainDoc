from Constants import connString
import pyodbc
import datetime
import uuid
import time    
from Constants import contract_address
from web3 import Web3, HTTPProvider
import json
import pprint
        
class DocumentHolderModel:
    def __init__(self, documentHolderID = '',documentHolderName = '',documentInformation='', documentName = '',documentFile = '',approvedByID = '',uploadedByID = '',createdDate = None,expireDate = None,isBlockChainGenerated = False,hash = '',prevHash = '',sequenceNumber = 0,approvedByModel = None,uploadedByModel = None):
        self.documentHolderID = documentHolderID
        self.documentHolderName = documentHolderName
        self.documentInformation = documentInformation
        self.documentName = documentName
        self.documentFile = documentFile
        self.approvedByID = approvedByID
        self.uploadedByID = uploadedByID
        self.createdDate = createdDate
        self.expireDate = expireDate
        self.isBlockChainGenerated = isBlockChainGenerated
        self.hash = hash
        self.prevHash = prevHash
        self.sequenceNumber = sequenceNumber
        self.approvedByModel = approvedByModel
        self.uploadedByModel = uploadedByModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM DocumentHolder ORDER BY documentName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = DocumentHolderModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT documentHolderID, documentName FROM DocumentHolder ORDER BY documentName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = DocumentHolderModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM DocumentHolder WHERE documentHolderID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = DocumentHolderModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.documentHolderID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO DocumentHolder (documentHolderID,documentHolderName,documentInformation,documentName,documentFile,approvedByID,uploadedByID,createdDate,expireDate,isBlockChainGenerated,hash,prevHash,sequenceNumber) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.documentHolderID,obj.documentHolderName,obj.documentInformation,obj.documentName,obj.documentFile,obj.approvedByID,obj.uploadedByID,datetime.datetime.strptime(obj.createdDate.replace('T', ' '), '%Y-%m-%d %H:%M'),datetime.datetime.strptime(obj.expireDate.replace('T', ' '), '%Y-%m-%d'),obj.isBlockChainGenerated,obj.hash,obj.prevHash,obj.sequenceNumber))
        cursor.close()
        conn.close()
        

        w3 = Web3(HTTPProvider('http://localhost:7545'))
        
        
        compiled_contract_path = 'D:/MYPROJECT/DocumentHolder-Truffle/build/contracts/DocumentHolderContract.json'
        deployed_contract_address = contract_address
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]
        
        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        
        accounts = w3.eth.accounts
    
        
        tx_hash = contract.functions.perform_transactions(obj.documentHolderID, obj.documentHolderName, obj.documentName, obj.documentFile, obj.approvedByID, obj.uploadedByID).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)        
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE DocumentHolder SET documentHolderName = ?,documentInformation = ?,documentName = ?,documentFile = ?,approvedByID = ?,uploadedByID = ?,createdDate = ?,expireDate = ?,isBlockChainGenerated = ?,hash = ?,prevHash = ?,sequenceNumber = ? WHERE documentHolderID = ?"
        cursor.execute(sqlcmd1,  (obj.documentHolderName,obj.documentInformation,obj.documentName,obj.documentFile,obj.approvedByID,obj.uploadedByID,datetime.datetime.strptime(obj.createdDate.replace('T', ' '), '%Y-%m-%d %H:%M'),datetime.datetime.strptime(obj.expireDate.replace('T', ' '), '%Y-%m-%d'),obj.isBlockChainGenerated,obj.hash,obj.prevHash,obj.sequenceNumber,obj.documentHolderID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM DocumentHolder WHERE documentHolderID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

