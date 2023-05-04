
from flask import Flask, request, render_template, redirect, url_for
import os
import pyodbc
import uuid
import time
from datetime import datetime
from Constants import connString

from ApprovedByModel import ApprovedByModel
from DocumentHolderModel import DocumentHolderModel
from RoleModel import RoleModel
from UploadedByModel import UploadedByModel
from UsersModel import UsersModel




app = Flask(__name__)
app.secret_key = "MySecret"
ctx = app.app_context()
ctx.push()

with ctx:
    pass
user_id = ""
emailid = ""
role_object = None
message = ""
msgType = ""
uploaded_file_name = ""

def initialize():
    global message, msgType
    message = ""
    msgType = ""

def process_role(option_id):

    
    if option_id == 0:
        if role_object.canApprovedBy == False:
            return False
        
    if option_id == 1:
        if role_object.canDocumentHolder == False:
            return False
        
    if option_id == 2:
        if role_object.canRole == False:
            return False
        
    if option_id == 3:
        if role_object.canUploadedBy == False:
            return False
        
    if option_id == 4:
        if role_object.canUsers == False:
            return False
    if option_id == 5:
        if role_object.canedit == False:
            return False
    if option_id == 6:
        if role_object.candelete == False:
            return False
        

    return True



@app.route("/")
def index():
    global user_id, emailid
    return render_template("Login.html")

@app.route("/processLogin", methods=["POST"])
def processLogin():
    global user_id, emailid, role_object
    emailid = request.form["emailid"]
    password = request.form["password"]
    conn1 = pyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM Users WHERE emailid = '" + emailid + "' AND password = '" + password + "' AND isActive = 1";
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()

    cur1.commit()
    if not row:
        return render_template("Login.html", processResult="Invalid Credentials")
    user_id = row[0]

    cur2 = conn1.cursor()
    sqlcmd2 = "SELECT * FROM Role WHERE RoleID = '" + str(row[6]) + "'"
    cur2.execute(sqlcmd2)
    row2 = cur2.fetchone()

    if not row2:
        return render_template("Login.html", processResult="Invalid Role")

    # role_object = RoleModel(row2[0], row2[1], row2[2], row2[3], row2[4], row2[5], row2[6])
    role_object = RoleModel(row2[0], row2[1], row2[2], row2[3], row2[4], row2[5], row2[6],row2[7],row2[8])

    return render_template("Dashboard.html")


@app.route("/ChangePassword")
def changePassword():
    global user_id, emailid
    return render_template("ChangePassword.html")


@app.route("/ProcessChangePassword", methods=["POST"])
def processChangePassword():
    global user_id, emailid
    oldPassword = request.form["oldPassword"]
    newPassword = request.form["newPassword"]
    confirmPassword = request.form["confirmPassword"]
    conn1 = pyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM Users WHERE emailid = '" + emailid + "' AND password = '" + oldPassword + "'";
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()
    cur1.commit()
    if not row:
        return render_template("ChangePassword.html", msg="Invalid Old Password")

    if newPassword.strip() != confirmPassword.strip():
        return render_template("ChangePassword.html", msg="New Password and Confirm Password are NOT same")

    conn2 = pyodbc.connect(connString, autocommit=True)
    cur2 = conn2.cursor()
    sqlcmd2 = "UPDATE Users SET password = '" + newPassword + "' WHERE emailid = '" + emailid + "'";
    cur1.execute(sqlcmd2)
    cur2.commit()
    return render_template("ChangePassword.html", msg="Password Changed Successfully")


@app.route("/Dashboard")
def Dashboard():
    global user_id, emailid
    return render_template("Dashboard.html")


@app.route("/Information")
def Information():
    global message, msgType
    return render_template("Information.html", msgType=msgType, message=message)


@app.route("/ApprovedByListing")
def ApprovedBy_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canApprovedBy = process_role(0)

    if canApprovedBy == False:
        message = "You Don't Have Permission to Access ApprovedBy"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = ApprovedByModel.get_all()

    return render_template("ApprovedByListing.html", records=records)

@app.route("/ApprovedByOperation")
def ApprovedBy_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canApprovedBy = process_role(0)

    if not canApprovedBy:
        message = "You Don't Have Permission to Access ApprovedBy"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = ApprovedByModel("", "")

    ApprovedBy = ApprovedByModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = ApprovedByModel.get_by_id(unique_id)

    return render_template("ApprovedByOperation.html", row=row, operation=operation, ApprovedBy=ApprovedBy, )

@app.route("/ProcessApprovedByOperation", methods=["POST"])
def process_ApprovedBy_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canApprovedBy = process_role(0)
    if not canApprovedBy:
        message = "You Don't Have Permission to Access ApprovedBy"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = ApprovedByModel("", "")

    if operation != "Delete":
       obj.approvedByID = request.form['approvedByID']
       obj.approvedByName = request.form['approvedByName']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.approvedByID = request.form["approvedByID"]
        obj.update(obj)

    if operation == "Delete":
        approvedByID = request.form["approvedByID"]
        obj.delete(approvedByID)


    return redirect(url_for("ApprovedBy_listing"))
                    
@app.route("/DocumentHolderListing")
def DocumentHolder_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canDocumentHolder = process_role(1)
    if canDocumentHolder == False:
        message = "You Don't Have Permission to Access DocumentHolder"
        msgType = "Error"
        return redirect(url_for("Information"))
    canedit=process_role(5)
    candelete=process_role(6)
    if canedit== False:
        message="You Don't have permission to edit"
        msgType="Error"
    if candelete== False:
        message="You Don't have permission to delete"
        msgType="Error"


    records = DocumentHolderModel.get_all()

    return render_template("DocumentHolderListing.html", records=records, role_object=role_object)

@app.route("/DocumentHolderOperation")
def DocumentHolder_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canDocumentHolder = process_role(1)

    if not canDocumentHolder:
        message = "You Don't Have Permission to Access DocumentHolder"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = DocumentHolderModel("", "")

    DocumentHolder = DocumentHolderModel.get_all()
    approvedBy_list = ApprovedByModel.get_name_id()
    uploadedBy_list = UploadedByModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = DocumentHolderModel.get_by_id(unique_id)

    return render_template("DocumentHolderOperation.html", row=row, operation=operation, DocumentHolder=DocumentHolder, approvedBy_list = approvedBy_list,uploadedBy_list = uploadedBy_list)

@app.route("/ProcessDocumentHolderOperation", methods=["POST"])
def process_DocumentHolder_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canDocumentHolder = process_role(1)
    if not canDocumentHolder:
        message = "You Don't Have Permission to Access DocumentHolder"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = DocumentHolderModel("", "")

    if operation != "Delete":
       obj.documentHolderID = request.form['documentHolderID']
       obj.documentHolderName = request.form['documentHolderName']
       obj.documentInformation = request.form['documentInformation']
       obj.documentName = request.form['documentName']
       obj.approvedByID = request.form['approvedByID']
       obj.uploadedByID = request.form['uploadedByID']
       obj.createdDate = request.form['createdDate']
       obj.expireDate = request.form['expireDate']
       if len(request.files) != 0 :
        
                file = request.files['documentFile']
                print(file)
                if file.filename != ' ':
                    print(file.filename)
                    documentFile = file.filename
                    obj.documentFile = documentFile
                    print(os.path)
                    # f = os.path.join('static/UPLOADED_FILES', documentFile)
                    f = os.path.join('D:\MYPROJECT\DocumentHolder\DocumentHolder\src\static/UPLOADED_FILES', documentFile)
                    
                    print(f)
                    file.save(f)
                else:
                    obj.documentFile = request.form['hdocumentFile']
                

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.documentHolderID = request.form["documentHolderID"]
        obj.update(obj)

    if operation == "Delete":
        documentHolderID = request.form["documentHolderID"]
        obj.delete(documentHolderID)


    return redirect(url_for("DocumentHolder_listing"))
                    
@app.route("/RoleListing")
def Role_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRole = process_role(2)

    if canRole == False:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = RoleModel.get_all()

    return render_template("RoleListing.html", records=records)

@app.route("/RoleOperation")
def Role_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRole = process_role(2)

    if not canRole:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = RoleModel("", "")

    Role = RoleModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = RoleModel.get_by_id(unique_id)

    return render_template("RoleOperation.html", row=row, operation=operation, Role=Role, )

@app.route("/ProcessRoleOperation", methods=["POST"])
def process_Role_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canRole = process_role(2)
    if not canRole:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = RoleModel("", "")

    if operation != "Delete":
       obj.roleID = request.form['roleID']
       obj.roleName = request.form['roleName']
       obj.canRole = 0 
       if request.form.get("canRole") != None : 
              obj.canRole = 1       
       obj.canUsers = 0 
       if request.form.get("canUsers") != None : 
              obj.canUsers = 1       
       obj.canApprovedBy = 0 
       if request.form.get("canApprovedBy") != None : 
              obj.canApprovedBy = 1       
       obj.canDocumentHolder = 0 
       if request.form.get("canDocumentHolder") != None : 
              obj.canDocumentHolder = 1       
       obj.canUploadedBy = 0 
       if request.form.get("canUploadedBy") != None : 
              obj.canUploadedBy = 1       
       if request.form.get("canedit") != None : 
              obj.canedit = 1       
       if request.form.get("candelete") != None : 
              obj.candelete = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.roleID = request.form["roleID"]
        obj.update(obj)

    if operation == "Delete":
        roleID = request.form["roleID"]
        obj.delete(roleID)


    return redirect(url_for("Role_listing"))
                    
@app.route("/UploadedByListing")
def UploadedBy_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUploadedBy = process_role(3)

    if canUploadedBy == False:
        message = "You Don't Have Permission to Access UploadedBy"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = UploadedByModel.get_all()

    return render_template("UploadedByListing.html", records=records)

@app.route("/UploadedByOperation")
def UploadedBy_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUploadedBy = process_role(3)

    if not canUploadedBy:
        message = "You Don't Have Permission to Access UploadedBy"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = UploadedByModel("", "")

    UploadedBy = UploadedByModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = UploadedByModel.get_by_id(unique_id)

    return render_template("UploadedByOperation.html", row=row, operation=operation, UploadedBy=UploadedBy, )

@app.route("/ProcessUploadedByOperation", methods=["POST"])
def process_UploadedBy_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canUploadedBy = process_role(3)
    if not canUploadedBy:
        message = "You Don't Have Permission to Access UploadedBy"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = UploadedByModel("", "")

    if operation != "Delete":
       obj.uploadedByID = request.form['uploadedByID']
       obj.uploadedByName = request.form['uploadedByName']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.uploadedByID = request.form["uploadedByID"]
        obj.update(obj)

    if operation == "Delete":
        uploadedByID = request.form["uploadedByID"]
        obj.delete(uploadedByID)


    return redirect(url_for("UploadedBy_listing"))
                    
@app.route("/UsersListing")
def Users_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUsers = process_role(4)

    if canUsers == False:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = UsersModel.get_all()

    return render_template("UsersListing.html", records=records)

@app.route("/UsersOperation")
def Users_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUsers = process_role(4)

    if not canUsers:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = UsersModel("", "")

    Users = UsersModel.get_all()
    role_list = RoleModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = UsersModel.get_by_id(unique_id)

    return render_template("UsersOperation.html", row=row, operation=operation, Users=Users, role_list = role_list)

@app.route("/ProcessUsersOperation", methods=["POST"])
def process_Users_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canUsers = process_role(4)
    if not canUsers:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = UsersModel("", "")

    if operation != "Delete":
       obj.userID = request.form['userID']
       obj.userName = request.form['userName']
       obj.emailid = request.form['emailid']
       obj.password = request.form['password']
       obj.contactNo = request.form['contactNo']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       obj.roleID = request.form['roleID']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.userID = request.form["userID"]
        obj.update(obj)

    if operation == "Delete":
        userID = request.form["userID"]
        obj.delete(userID)


    return redirect(url_for("Users_listing"))
                    


import hashlib
import json


@app.route("/BlockChainGeneration")
def BlockChainGeneration():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM DocumentHolder WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    sqlcmd = "SELECT COUNT(*) FROM DocumentHolder WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksNotCreated = dbrow[0]
    return render_template('BlockChainGeneration.html', blocksCreated=blocksCreated, blocksNotCreated=blocksNotCreated)


@app.route("/ProcessBlockchainGeneration", methods=['POST'])
def ProcessBlockchainGeneration():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM DocumentHolder WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    blocksCreated = 0
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    prevHash = ""
    if blocksCreated != 0:
        connx = pyodbc.connect(connString, autocommit=True)
        cursorx = connx.cursor()
        sqlcmdx = "SELECT * FROM DocumentHolder WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY sequenceNumber"
        cursorx.execute(sqlcmdx)
        dbrowx = cursorx.fetchone()
        if dbrowx:
            uniqueID = dbrowx[12]
            conny = pyodbc.connect(connString, autocommit=True)
            cursory = conny.cursor()
            sqlcmdy = "SELECT hash FROM DocumentHolder WHERE sequenceNumber < '" + str(uniqueID) + "' ORDER BY sequenceNumber DESC"
            cursory.execute(sqlcmdy)
            dbrowy = cursory.fetchone()
            if dbrowy:
                prevHash = dbrowy[0]
            cursory.close()
            conny.close()
        cursorx.close()
        connx.close()
    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT * FROM DocumentHolder WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY sequenceNumber"
    cursor.execute(sqlcmd)

    while True:
        sqlcmd1 = ""
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        unqid = str(dbrow[12])

        bdata = str(dbrow[1]) + str(dbrow[2]) + str(dbrow[3]) + str(dbrow[4])
        block_serialized = json.dumps(bdata, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(block_serialized).hexdigest()

        conn1 = pyodbc.connect(connString, autocommit=True)
        cursor1 = conn1.cursor()
        sqlcmd1 = "UPDATE DocumentHolder SET isBlockChainGenerated = 1, hash = '" + block_hash + "', prevHash = '" + prevHash + "' WHERE sequenceNumber = '" + unqid + "'"
        cursor1.execute(sqlcmd1)
        cursor1.close()
        conn1.close()
        prevHash = block_hash
    return render_template('BlockchainGenerationResult.html')


@app.route("/BlockChainReport")
def BlockChainReport():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()

    sqlcmd1 = "SELECT * FROM DocumentHolder WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd1)
    conn2 = pyodbc.connect(connString, autocommit=True)
    cursor = conn2.cursor()
    sqlcmd1 = "SELECT * FROM DocumentHolder ORDER BY sequenceNumber DESC"
    cursor.execute(sqlcmd1)
    records = []

    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        row = DocumentHolderModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12])
        records.append(row)
    return render_template('BlockChainReport.html', records=records)         

            

 
if __name__ == "__main__":
    app.run()

                    