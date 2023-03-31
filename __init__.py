import csv
from datetime import timedelta,datetime
from os import path
import sqlite3
from flask import g,Flask,render_template,request,make_response
from flask_mail import Mail, Message
from os import path
import qrcode
from dict_factory import dict_factory
import hashlib
import json
import re
import pdfkit
from icalendar import Calendar, Event, vCalAddress, vText
# import pytz

fileDir = path.dirname(__file__) # for loading images

app = Flask(__name__)   #creates the application flask

app.secret_key = "b6jF" #sets secret key for encription i.e. my encription + first words quack

DATABASE = 'students.db'  #for sptinfo
currentTableName = None
alerts = []
messages = []

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(path.join(fileDir,DATABASE))
    return db

@app.teardown_appcontext  #closes the database when the file is closed
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def clearAlertsAndMessages():
    global messages,alerts
    alerts = []
    messages = []

def getIndexPage(tableName,tableData = None):
    global alerts,messages
    columnNames = query_db("SELECT name FROM pragma_table_info('{0}') ".format(tableName))
    # print(columnNames)
    if tableData is None:
        data = query_db("SELECT * FROM {0};".format(tableName))
    else:
        data = tableData
    if len(data)>0:
        columns = len(data[0])
    else:
        columns = 0
    tables = query_db("SELECT name FROM sqlite_master WHERE type='table' AND NOT (name = 'sqlite_sequence' OR name='Current');")
    global currentTableName
    if currentTableName is None:
        tableName = ""
    else:
        tableName = currentTableName
    return render_template("indexSPT.html",data=data,columns=columns,columnNames=columnNames,tables=tables,alerts=alerts,messages=messages,currentlyOpenTableName=tableName)

def updateTable(tableName,records):
    clearAlertsAndMessages()
    sql1 = 'DELETE FROM {0}'.format(str(tableName))
    query_db(sql1)

    for record in records:
        # print(record)
        columns = "?"
        for i in range(len(record)-1):
            columns = columns + ",?"
        sql2 = 'INSERT INTO {0} VALUES({1})'.format(tableName,columns)
        print(sql2,record)
        query_db(sql2,record)
        # try:
        # except:
            # done = False
            # while not done:
            #     nulls = ["NULL"]
            #     for i in range(len(nulls)-1):
            #         columns = columns + ",?"
            #     query_db("INSERT INTO {0} VALUES({1})".format(tableName,columns),nulls)
            #     try:
            #         query_db("INSERT INTO {0} VALUES({1})".format(tableName,columns),nulls)
            #         done=True
            #     except:
            #         nulls.append("NULL")
    get_db().commit()


@app.route("/tableUpdate",methods=["POST"])
def tableUpdate():
    clearAlertsAndMessages()
    data = request.get_json()
    if data is None:
        pass
    else:
        updateTable("Current",data)
        global currentTableName
        if currentTableName is None:
            print("Data is not being saved")
        else:
            updateTable(currentTableName,data)
    return ("nothing")

def searchSQLTable(tableName,columnName,searchValue):
    sql1 ="SELECT * FROM {0} WHERE {1} = '{2}'".format(tableName,columnName,searchValue)
    data = query_db(sql1)
    return data

@app.route("/searchTable",methods=["POST"])
def searchTable():
    clearAlertsAndMessages()
    tableName = "Current"
    data = request.get_json()
    if data is None:
        return ("nothing")
    else:
        # print(data)
        # print(data["columnName"])
        tableData = searchSQLTable(tableName,data["columnName"],data["searchValue"])
        # print(tableData)
        createCurrentTableFromSearch(tableData)
        # print(tableData)
        # return getIndexPage(tableName,tableData=tableData)
        return ("nothing")

@app.route("/test")
def test():
    print("testfunction")

def createCurrentTableFromSearch(tableData):
    sql1 = 'DELETE FROM Current;'
    query_db(sql1)
    for record in tableData:
        columns = "?"
        for i in range(len(record)-1):
            columns = columns + ",?"
        sql2 = 'INSERT INTO "Current" VALUES({0})'.format(columns)
        query_db(sql2,record)
    get_db().commit()
    if len(query_db("SELECT * FROM Current")) == 0:
        print("There are no rows that fit that criteria")

def createCurrentTable(tableName):
    columnNames = query_db("SELECT name FROM pragma_table_info('{0}')".format(tableName))
    columnInformation = ""
    for column in columnNames:
        columnInformation = columnInformation + "'{0}' TEXT,".format(column[0])
    columnInformation = columnInformation[0:len(columnInformation)-1]
    # print(columnInformation)
    data = query_db("SELECT * FROM {0};".format(tableName))
    query_db("DROP TABLE IF EXISTS Current")
    query_db("CREATE TABLE 'Current' ({0})".format(columnInformation))
    for record in data:
        columns = "?"
        for i in range(len(record)-1):
            columns = columns + ",?"
        sql2 = 'INSERT INTO "Current" VALUES({0})'.format(columns)
        query_db(sql2,record)
    get_db().commit()

def createCurrentTableFromData(data):
    print(data)
    columnNamesArray = []
    for row in data:
        columnName = list(row.keys())
        columnNamesArray.append(columnName)
    longestColumn = columnNamesArray[0]
    for column in columnNamesArray:
        if len(column) > len(longestColumn):
            longestColumn = column
    columnNames = longestColumn
    # print(columnNames)
    columnInformation = ""
    for column in columnNames:
        column = column.replace(" ","_")
        if column == "":
            column = "blank"
        columnInformation = columnInformation + "{0} TEXT,".format(column)
    columnInformation = columnInformation[0:len(columnInformation)-1]
    print(columnInformation)
    query_db("DROP TABLE IF EXISTS Current")
    query_db(("CREATE TABLE 'Current' ({0})").format(columnInformation))
    for record in data:
        record = list(record.values())
        # print(record)
        columns = "?"
        for i in range(len(record)-1):
            columns = columns + ",?"
        sql2 = 'INSERT INTO "Current" VALUES({0})'.format(columns)
        # print(sql2)
        query_db(sql2,record)
    get_db().commit()

def createBlankCurrentTable():
    columnInformation = "blank TEXT "
    query_db("DROP TABLE IF EXISTS Current")
    query_db(("CREATE TABLE 'Current' ({0})").format(columnInformation))
    get_db().commit()

@app.route('/openTable',methods=["POST"])
def openTable():
    clearAlertsAndMessages()
    tableName = request.get_json()
    if tableName is None:
        return ("nothing")
    else:
        global currentTableName
        currentTableName = tableName
        createCurrentTable(tableName)
    return("nothing")

# global currentTableName
@app.route('/spt',methods=["GET","POST"])
def spt():
    # createCurrentTable(currentTableName)
    global currentTableName
    if currentTableName is None:
        createBlankCurrentTable()
    else:
        if not checkIfTableExisits("Current"):
            createCurrentTable(currentTableName)
    return getIndexPage("Current")


@app.route('/openExcelFile',methods=["POST"])
def openExcelFile():
    clearAlertsAndMessages()
    data = request.get_json()
    if data is None:
        return ("nothing")
    else:
        createCurrentTableFromData(data)
        global currentTableName
        currentTableName = None
        # print(data)
    # index()
    return ("nothing")


def convertCurrentToCurrentOpenTable(tableName):
    columnNames = query_db("SELECT t.name FROM pragma_table_info('Current') t")
    columnInformation = ""
    for column in columnNames:
        columnInformation = columnInformation + "'{0}' TEXT,".format(column[0])
    columnInformation = columnInformation[0:len(columnInformation)-1]
    print(columnInformation)
    data = query_db("SELECT * FROM Current;")
    query_db("DROP TABLE IF EXISTS '{0}'".format(tableName))
    query_db("CREATE TABLE '{0}' ({1})".format(tableName,columnInformation))
    for record in data:
        columns = "?"
        for i in range(len(record)-1):
            columns = columns + ",?"
        sql2 = 'INSERT INTO "{0}" VALUES({1})'.format(tableName,columns)
        query_db(sql2,record)
    get_db().commit()

def hasNumbersOrSpaces(inputString):
    return any(char.isdigit() or char == " " for char in inputString)

@app.route('/saveTable',methods=["POST"])
def saveTable():
    clearAlertsAndMessages()
    data = request.get_json()
    print(data)
    if data is None:
        return ("nothing")
    else:
        if hasNumbersOrSpaces(data):
            alerts.append("The table name has a space or number. Please try a different name.")
            print("the table name as a space or number")
            return("nothing")
        else:
            tableNames = getTableNames()
            tableNamesArray = []
            for name in tableNames:
                tableNamesArray.append(name[0])
            # if data in tableNamesArray:
            #     alerts.append("There is already a table with that name")
            #     print("There is already a table with that name")
            #     return ("nothing")
            if data == "":
                alerts.append("The table name cannot be blank")
                print("The table name cannot be blank")
                return ("nothing")
            global currentTableName
            currentTableName = data
            convertCurrentToCurrentOpenTable(currentTableName)
            messages.append("The table was successfully saved as '{0}'".format(currentTableName))
    return ("nothing")

def createNewBlankTable(columns,tableName):
    columnInformation = ""
    for i,column in enumerate(columns):
        if i==len(columns)-1:
            columnInformation = columnInformation + "'{0}' TEXT".format(column)
        else:
            columnInformation  = columnInformation + "'{0}' TEXT".format(column) + ","
    print(columnInformation)
    sql1 = "CREATE TABLE {0} ({1})".format(tableName,columnInformation)
    query_db(sql1)
    record = []
    for i in range(len(columns)):
        record.append("")
    if len(record) > 0:
        record[0] = 1
    questionMarks = "?"
    for i in range(len(record)-1):
        questionMarks = questionMarks + ",?"
    sql2 = "INSERT INTO {0} VALUES({1})".format(tableName,questionMarks)
    query_db(sql2,record)
    get_db().commit()
    return True


@app.route('/deleteTable',methods=["POST"])
def deleteTable():
    clearAlertsAndMessages()
    data = request.get_json()
    if data is None:
        return ("nothing")
    else:
        sql1 = "DROP TABLE {0}".format(data)
        query_db(sql1)
        get_db().commit()
        global currentTableName
        if currentTableName == data:
            createBlankCurrentTable()
    return ("nothing")

@app.route('/createNewTable',methods=["POST"])
def createNewTable():
    clearAlertsAndMessages()
    data = request.get_json()
    print(data)
    if data is None:
        return ("nothing")
    else:
        try:
            tableName = data[0]
        except:
            alerts.append("The data was not sent correctly. Please try again")
            return ("nothing")
        if hasNumbersOrSpaces(tableName):
            alerts.append("The table name has a space or number. Please try a different name.")
            print("the table name as a space or number")
            return("nothing")
        if len(data) == 1:
            alerts.append("Please create at least one table name before creating the table.")
            return ("nothing")
        if checkIfTableExisits(tableName):
            alerts.append("That table name already exists. Please try again")
            return ("nothing")

        columnNames = data[1:]
        createBlankCurrentTable()
        createNewBlankTable(columnNames,tableName)
        global currentTableName
        currentTableName = tableName
        createCurrentTable(tableName)


    return ("nothing")

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def getTableNames():
    return query_db("SELECT name FROM sqlite_master WHERE type='table';")

def checkIfTableExisits(tableName):  #returns true or false if exisits or not
    results = query_db('SELECT name FROM sqlite_master WHERE type="table" AND name="{0}";'.format(tableName))
    if len(results)==1:
        return True
    else:
        return False



'''
SPT INFO

'''

@app.route("/resetTable",methods=["POST"])
def resetTable():
    createCurrentTable("students")
    return ("nothing")

@app.route("/sptinfo")
def sptinfo():
    if not checkIfTableExisits("Current"):
            createCurrentTable("students")
    return get_index_page("Current")

def get_index_page(tableName = None):
    if tableName is None:
        tableName = "Current"
    columnNames = query_db("SELECT name FROM pragma_table_info('{0}') WHERE name != 'id'".format(tableName))
    data = query_db("SELECT fname,sname,form,email,role FROM {0};".format(tableName))
    if len(data)>0:
        columns = len(data[0])
    else:
        columns = 0
    return render_template("indexInfo.html",data=data,columns=columns,columnNames=columnNames)


'''
QRCode
'''

def checkIfTableExisits_qr(tableName):  #returns true or false if exisits or not
    results = query_db_qr('SELECT name FROM sqlite_master WHERE type="table" AND name="{0}";'.format(tableName))
    if len(results)==1:
        return True
    else:
        return False

def query_db_qr(query, args=(), one=False):
    cur = get_db_qr().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db_qr():
    DATABASE = "results.db"
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(path.join(fileDir,DATABASE))
    return db

def create_results_table():
    query_db_qr('CREATE TABLE "results" ("id"	INTEGER NOT NULL UNIQUE,"forename"	TEXT NOT NULL,"surname"	TEXT NOT NULL,"email"	TEXT,"user_id"	TEXT,"group_id"	TEXT NOT NULL,	"visited" INTEGER, PRIMARY KEY("id" AUTOINCREMENT))')

def get_visited_percentage(group_id):
    visited = query_db_qr("SELECT id FROM results WHERE visited='1' AND group_id = '{0}'".format(group_id))
    # print(visited)
    total = query_db_qr("SELECT id FROM results WHERE  group_id = '{0}'".format(group_id))
    if len(total) == 0:
        return 0
    return len(visited)/len(total)

def update_results(info):
    id = info["id"]
    group_id = info["group_id"]
    # query_db_qr("INSERT INTO results (user_id,group_id,visited) VALUES (?,?,?)",(id,group_id,1))
    if query_db_qr("SELECT id FROM results WHERE user_id='{0}' AND group_id='{1}'".format(id,group_id)):
        query_db_qr("UPDATE results SET visited='1' WHERE user_id='{0}' AND group_id='{1}'".format(id,group_id))
    else:
        print("value does not exist")

@app.route("/display_page/<group_id>")
def display_page(group_id):
    if not checkIfTableExisits_qr("results"):
        print("test")
        create_results_table()
    column_names=["Forename","Surname","Visited"]
    data = query_db_qr("SELECT forename,surname,visited FROM results WHERE group_id = '{0}' ".format(group_id))
    print(data)
    visited_percentage = get_visited_percentage(group_id)
    visited_percentage = str(100-int(100*visited_percentage)) + "%"
    # print(visited_percentage)
    # visited_percentage = "20%"
    pie_chart_composition = "background:conic-gradient(red 0% {0}, green {1} 100%)".format(visited_percentage,visited_percentage)
    # pie_chart_composition = "background-color:red;"

    return render_template("display_page.html",group_id=group_id,data=data,column_names=column_names,columns=len(column_names),pie_chart_composition=pie_chart_composition)

@app.route("/qr_submit/<group_id>/<id>")
def qr_submit(group_id,id):
    if not checkIfTableExisits_qr("results"):
        print("test")
        create_results_table()

    update_results({"id":id,"group_id":group_id})

    get_db_qr().commit()
    info = query_db_qr("SELECT forename,surname FROM results WHERE user_id='{0}' AND group_id='{1}'".format(id,group_id))
    if len(info) == 0:
        print("person does not exist")
        forename=None
        surname=None
    else:
        forename = info[0][0]
        surname = info[0][1]
    # print("test")
    return render_template("qr_submit.html",id=id,forename=forename,surname=surname)

'''
Table plan
'''

number_of_tables = 20
number_of_seats_per_table = 10

class Table_plan_Login(object):
    def __init__(self):
        self.DATABASE = "table_plan.db"

    def query_db(self,query, args=()):
        cur = self.get_db().execute(query, args)
        cur.row_factory = dict_factory
        rv = cur.fetchall()
        cur.close()
        return rv

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(path.join(fileDir,self.DATABASE))
        return db

    def send_login_email(self,email_record):
        forename = email_record["forename"]
        surname = email_record["surname"]
        email_address = email_record["email"]
        table_link = self.get_table_link(email_address)
        # print(forename,surname,email_address)
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        app.config["MAIL_USERNAME"] = "test68duck@gmail.com"
        app.config["MAIL_PASSWORD"] = "qlosiorsjujiuoga"
        subject = "Table Plan Link"
        message = "Hello {0} {1},\n\nThank you for logging into the table plan. Here is your link to the table plan:\n{2}\nPlease don't share this with anyone else since this link is unique to you and any changes made will be associated with this email, so any untoward behaviour will be able to be tracked to this email.\n\nIf you have any issues with this system or the table plan in general, don't hesitate to contact me on HenryJP@rgshw.com.\n\nRegards,\nJosh Henry".format(forename,surname,table_link)
        mail = Mail(app)
        msg = Message(subject,sender="test68duck@gmail.com",recipients = [email_address])
        msg.body = message
        mail.send(msg)
        #the message was changed to above since below did not work with the raspberry pi.
        # message = f"""
        # Hello {forename} {surname},
        #
        # Thank you for logging into the table plan. Here is your link to the table plan:
        # {table_link}
        # Please don't share this with anyone else since this link is unique to you and any changes made will be associated with this email, so any malicious behaviour will be able to be tracked to this email.
        #
        # If you have any issues with this system or the table plan in general, don't hesitate to contact me on HenryJP@rgshw.com.
        #
        # Regards,
        # Josh Henry
        # """

    def get_table_link(self,email_address):
        m = hashlib.sha256()
        m.update(email_address.encode("utf8"))
        hash = m.hexdigest()
        link = "http://68duck.co.uk/table_plan/" + hash
        return link

class Table_plan(object):
    def __init__(self):
        self.DATABASE = "table_plan.db"

    def query_db(self,query, args=()):
        cur = self.get_db().execute(query, args)
        cur.row_factory = dict_factory
        rv = cur.fetchall()
        cur.close()
        return rv

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(path.join(fileDir,self.DATABASE),isolation_level = None)
        return db

    def get_hash(self,email_address):
        m = hashlib.sha256()
        m.update(email_address.encode("utf8"))
        hash = m.hexdigest()
        return hash

    def insert_into_table(self,table_name,record_values):
        question_marks = ""
        for i in range(len(record_values)):
            question_marks = question_marks + "?,"
        question_marks = question_marks[0:len(question_marks)-1]
        query = "INSERT INTO {0} VALUES ({1})".format(table_name,question_marks)
        self.query_db(query,record_values)

@app.route("/table_plan/admin/<id>")
def table_plan_admin(id):
    table_plan = Table_plan()
    table_names = ["Guests","RGS_students","people_in_tables","student_guest_link"]
    if id == "ba01338ba5fa0c1584a6d41f93fe550b1d715a8de2da10d6c673131a85658394":
        return render_template("table_plan_admin.html",table_names=table_names)
    else:
        return render_template("table_plan_error_page.html")

@app.route("/table_plan_admin_open_table",methods=["POST"])
def admin_open_table():
    data = request.get_json()
    if data is None:
        return "No data recieved"
    else:
        table_name = data
        table_plan = Table_plan()
        table_information = table_plan.query_db("SELECT * FROM {0}".format(table_name,))
        table_information = [list(dict.values()) for dict in table_information]
        headings_info = table_plan.query_db("PRAGMA table_info({0})".format(table_name,))
        table_information.insert(0,[header["name"] for header in headings_info])
        return json.dumps(table_information)

@app.route("/table_plan_admin_update_table",methods=["POST"])
def admin_update_table():
    data = request.get_json()
    if data is None:
        return "No data recieved"
    else:
        table_name = data.pop()
        table_data = data
        table_plan = Table_plan()
        table_plan.query_db("BEGIN")
        table_plan.query_db("DELETE FROM {0}".format(table_name))
        for val in table_data:
            table_plan.insert_into_table(table_name,val)
        table_plan.query_db("COMMIT")

        return json.dumps("nothing")


@app.route("/table_plan_logon")
def table_plan_logon():
    return render_template("table_plan_logon.html")

@app.route("/table_plan/<id>")
def table_plan(id):
    table_plan = Table_plan()
    record = None
    results = table_plan.query_db("SELECT forename,surname,email,student_id FROM RGS_students")
    for result in results:
        if table_plan.get_hash(result["email"]) == id:
            record = result
            student_id = result["student_id"]
    if record is None:
        return render_template("table_plan_error_page.html")
    else:
        database_table_information = table_plan.query_db("SELECT table_number,student_id,guest_id,seat_number,modified_by_id FROM people_in_tables")
        table_data = []
        changeable_array = []
        for i in range(number_of_tables):
            row = []
            for j in range(number_of_seats_per_table):
                row.append(None)
            table_data.append(row[:])
            changeable_array.append(row[:])
        for val in database_table_information:
            if val["student_id"] is not None:
                # print(val["student_id"])
                student = table_plan.query_db("SELECT forename,surname,email FROM RGS_students WHERE student_id = ?",(val["student_id"],))[0]
                table_data[val["table_number"]-1][val["seat_number"]-1] = [val["seat_number"],student["forename"],student["surname"]]
                if student_id == val["modified_by_id"] or student_id == val["student_id"]:
                    changeable_array[val["table_number"]-1][val["seat_number"]-1] = True
                else:
                    changeable_array[val["table_number"]-1][val["seat_number"]-1] = False
            elif val["guest_id"] is not None:
                guest = table_plan.query_db("SELECT forename,surname FROM Guests WHERE guest_id = ?",(val["guest_id"],))[0]
                table_data[val["table_number"]-1][val["seat_number"]-1] = [val["seat_number"],guest["forename"],guest["surname"]]
                if student_id == val["modified_by_id"]:
                    changeable_array[val["table_number"]-1][val["seat_number"]-1] = True
                else:
                    changeable_array[val["table_number"]-1][val["seat_number"]-1] = False
            else:
                pass
        # print(changeable_array)
        # print(table_data)
        forenames = []
        surnames = []
        names = []
        records = table_plan.query_db("SELECT forename,surname FROM RGS_students")
        for r in records:
            forenames.append(r["forename"])
            surnames.append(r["surname"])
            names.append([r["forename"],r["surname"]])
        records = table_plan.query_db("SELECT forename,surname FROM Guests")
        for r in records:
            forenames.append(r["forename"])
            surnames.append(r["surname"])
            names.append([r["forename"],r["surname"]])
        fnames = []
        for i in forenames:
            if i not in fnames:
                fnames.append(i)
        snames = []
        for i in surnames:
            if i not in snames:
                snames.append(i)
        # surnames = set(surnames)
        return render_template("table_plan.html",forename=record["forename"],surname=record["surname"],email=record["email"],table_data=table_data,no_tables=len(table_data),changeable_array=changeable_array,names=names,forenames=fnames,surnames=snames)

@app.route("/table_plan_login_email",methods=["POST"])
def send_login_email():
    data = request.get_json()
    if data is None:
        return "There was no email input"
    else:
        table_plan = Table_plan_Login()
        email = data
        email_record = table_plan.query_db("SELECT forename,surname,email FROM RGS_students WHERE email = ? COLLATE NOCASE",(email.replace(" ",""),))
        if len(email_record) == 0:
            return "There is no student with that email address. Please try again"
        elif len(email_record) > 1:
            return "There are multiple records with the same email. This should not reach this point so please contact Josh that this happened."
        else:
            table_plan.send_login_email(email_record[0])
            return "Email sent"

@app.route("/table_plan_find_changes",methods=["POST"])
def find_changes():
    data = request.get_json()
    if data is None:
        return "No data was sent"
    else:
        try:
            a = data[0][0][0]
        except:
            return "Data is not in the correct format"
        for i,table in enumerate(data):
            for j,val in enumerate(table):
                if val[1] == "" and val[2] == "":
                    data[i][j] = None
            data[i].pop(0)
        table_plan = Table_plan()
        database_table_information = table_plan.query_db("SELECT table_number,student_id,guest_id,seat_number FROM people_in_tables")
        table_data = []
        for i in range(number_of_tables):
            row = []
            for j in range(number_of_seats_per_table):
                row.append(None)
            table_data.append(row)
        for val in database_table_information:
            if val["student_id"] is not None:
                student = table_plan.query_db("SELECT forename,surname,email FROM RGS_students WHERE student_id = ? COLLATE NOCASE",(val["student_id"],))[0]
                table_data[val["table_number"]-1][val["seat_number"]-1] = [str(val["seat_number"]),student["forename"],student["surname"]]
            elif val["guest_id"] is not None:
                guest = table_plan.query_db("SELECT forename,surname FROM Guests WHERE guest_id = ? COLLATE NOCASE",(val["guest_id"],))[0]
                table_data[val["table_number"]-1][val["seat_number"]-1] = [str(val["seat_number"]),guest["forename"],guest["surname"]]
            else:
                pass

        changes = []
        for a in range(len(data)):
            for b in range(len(data[a])):
                if data[a][b] is None and data[a][b] != table_data[a][b]:
                    changes.append([None,None,a+1,b+1])
                elif data[a][b] != table_data[a][b]:
                    changes.append([data[a][b][1],data[a][b][2],a+1,b+1])

        # print(changes)
        return json.dumps(changes)

@app.route("/table_plan_confirm_changes",methods=["POST"])
def confirm_changes():
    data = request.get_json()
    if data is None:
        return "No data was sent"
    else:
        table_plan = Table_plan()
        forename = data["forename"]
        surname = data["surname"]
        check_data = data["check_data"]

        database_table_information = table_plan.query_db("SELECT table_number,student_id,guest_id,seat_number FROM people_in_tables")
        current_table_data = []
        for i in range(number_of_tables):
            row = []
            for j in range(number_of_seats_per_table):
                row.append(None)
            current_table_data.append(row[:])
        for val in database_table_information:
            if val["student_id"] is not None:
                # print(val["student_id"])
                student = table_plan.query_db("SELECT forename,surname,email FROM RGS_students WHERE student_id = ?",(val["student_id"],))[0]
                current_table_data[val["table_number"]-1][val["seat_number"]-1] = [val["seat_number"],student["forename"],student["surname"]]
            elif val["guest_id"] is not None:
                guest = table_plan.query_db("SELECT forename,surname FROM Guests WHERE guest_id = ?",(val["guest_id"],))[0]
                current_table_data[val["table_number"]-1][val["seat_number"]-1] = [val["seat_number"],guest["forename"],guest["surname"]]

        if check_data != current_table_data:
            return "Someone else has made some changes whilst you have been viewing this page. Please refresh to see these changes before making your changes."

        modifying_student_id_dict = table_plan.query_db("SELECT student_id FROM RGS_students WHERE forename = ? AND surname = ? COLLATE NOCASE",(forename,surname))
        if len(modifying_student_id_dict) == 0:
            return "Modifing student could not be found"
        else:
            modifying_student_id = modifying_student_id_dict[0]["student_id"]
        data = data["table_data"]
        try:
            a = data[0][0][0]
        except:
            return "Data is not in the correct format"
        for i,table in enumerate(data):
            for j,val in enumerate(table):
                if val[1] == "" and val[2] == "":
                    data[i][j] = None
            # data[i].remove(['Seat Number', 'Forename', 'Surname'])
            data[i].pop(0)
        database_table_information = table_plan.query_db("SELECT table_number,student_id,guest_id,seat_number FROM people_in_tables")
        table_data = []
        for i in range(number_of_tables):
            row = []
            for j in range(number_of_seats_per_table):
                row.append(None)
            table_data.append(row)
        for val in database_table_information:
            if val["student_id"] is not None:
                student = table_plan.query_db("SELECT forename,surname,email FROM RGS_students WHERE student_id = ? COLLATE NOCASE",(val["student_id"],))[0]
                table_data[val["table_number"]-1][val["seat_number"]-1] = [str(val["seat_number"]),student["forename"],student["surname"]]
            elif val["guest_id"] is not None:
                guest = table_plan.query_db("SELECT forename,surname FROM Guests WHERE guest_id = ? COLLATE NOCASE",(val["guest_id"],))[0]
                table_data[val["table_number"]-1][val["seat_number"]-1] = [str(val["seat_number"]),guest["forename"],guest["surname"]]
            else:
                pass

        changes = []
        for a in range(len(data)):
            for b in range(len(data[a])):
                if data[a][b] is None and data[a][b] != table_data[a][b]:
                    changes.append([None,None,a+1,b+1])
                elif data[a][b] != table_data[a][b]:
                    changes.append([data[a][b][1],data[a][b][2],a+1,b+1])

        if len(changes) == 0:
            return "No changes were made"

        table_plan.query_db("BEGIN")
        for val in changes:
            if val[0] == None and val[1] == None:
                guests_on_table = table_plan.query_db("SELECT guest_id FROM people_in_tables WHERE table_number = ? COLLATE NOCASE",(val[2],))
                student_id = table_plan.query_db("SELECT student_id FROM people_in_tables WHERE table_number = ? and seat_number = ? COLLATE NOCASE",(val[2],val[3]))
                if len(student_id) == 0:
                    pass
                else:
                    student_id = student_id[0]["student_id"]
                    guests_with_student = table_plan.query_db("SELECT guest_id FROM student_guest_link WHERE student_id = ? COLLATE NOCASE" ,(student_id,))
                    for g in guests_with_student:
                        if g in guests_on_table:
                            valid = False
                            guest_seat_number = table_plan.query_db("SELECT seat_number FROM people_in_tables WHERE guest_id = ?",(g["guest_id"],))
                            for v in changes:
                                if v[2] == val[2]: #so same table number
                                    if guest_seat_number[0]["seat_number"] == v[3]:
                                        valid = True
                            if not valid:
                                student = table_plan.query_db("SELECT forename,surname FROM RGS_students WHERE student_id = ? COLLATE NOCASE",(student_id,))
                                guest = table_plan.query_db("SELECT forename,surname FROM Guests WHERE guest_id = ?",(g["guest_id"],))
                                return "The student {0} {1} cannot be removed since they are on the same table as their guest {2} {3}. Please delete the guest before trying to delete the RGS student.".format(student[0]["forename"],student[0]["surname"],guest[0]["forename"],guest[0]["surname"])

                table_plan.query_db("DELETE FROM people_in_tables WHERE table_number = ? AND seat_number = ? COLLATE NOCASE",(val[2],val[3]))

            else:
                already_sitting_person = table_plan.query_db("SELECT student_id FROM people_in_tables WHERE table_number = ? AND seat_number = ?",(val[2],val[3]))
                if len(already_sitting_person) > 0:
                    guests_on_table = table_plan.query_db("SELECT guest_id FROM people_in_tables WHERE table_number = ? COLLATE NOCASE",(val[2],))
                    student_id = table_plan.query_db("SELECT student_id FROM people_in_tables WHERE table_number = ? and seat_number = ? COLLATE NOCASE",(val[2],val[3]))
                    if len(student_id) == 0:
                        pass
                    else:
                        student_id = student_id[0]["student_id"]
                        guests_with_student = table_plan.query_db("SELECT guest_id FROM student_guest_link WHERE student_id = ? COLLATE NOCASE" ,(student_id,))
                        for g in guests_with_student:
                            if g in guests_on_table:
                                valid = False
                                guest_seat_number = table_plan.query_db("SELECT seat_number FROM people_in_tables WHERE guest_id = ?",(g["guest_id"],))
                                for v in changes:
                                    if v[2] == val[2]: #so same table number
                                        if guest_seat_number[0]["seat_number"] == v[3]:
                                            valid = True
                                if not valid:
                                    student = table_plan.query_db("SELECT forename,surname FROM RGS_students WHERE student_id = ? COLLATE NOCASE",(student_id,))
                                    guest = table_plan.query_db("SELECT forename,surname FROM Guests WHERE guest_id = ?",(g["guest_id"],))
                                    return "The student {0} {1} cannot be removed since they are on the same table as their guest {2} {3}. Please delete the guest before trying to delete the RGS student.".format(student[0]["forename"],student[0]["surname"],guest[0]["forename"],guest[0]["surname"])


                student_id = table_plan.query_db("SELECT student_id FROM RGS_students WHERE forename = ? AND surname = ? COLLATE NOCASE",(val[0],val[1]))
                if len(student_id) == 0:
                    guest_id = table_plan.query_db("SELECT guest_id FROM Guests WHERE forename = ? AND surname = ? COLLATE NOCASE",(val[0],val[1]))
                    if len(guest_id) == 0:
                        return "No student or guest found with name {0} {1}".format(val[0],val[1])
                    else:
                        guest_links = table_plan.query_db("SELECT student_id FROM student_guest_link WHERE guest_id = ? COLLATE NOCASE",(guest_id[0]["guest_id"],))
                        if len(guest_links) == 0:
                            return "The guest is not associated with a student. This should not be possible"

                        guest_id = table_plan.query_db("SELECT guest_id FROM Guests WHERE forename = ? AND surname = ? COLLATE NOCASE",(val[0],val[1]))
                        students_on_table = table_plan.query_db("SELECT student_id FROM people_in_tables WHERE table_number = ? COLLATE NOCASE",(val[2],))
                        for v in changes:
                            if v[2] == val[2]: #so student is on the same table as the guest
                                student_id = table_plan.query_db("SELECT student_id FROM RGS_students WHERE forename = ? and surname = ?",(v[0],v[1]))
                                if len(student_id)>0:
                                    students_on_table.append({"student_id":student_id[0]["student_id"]})
                        valid = False
                        for student_dict in students_on_table:
                            if guest_links[0]["student_id"] == student_dict["student_id"]:
                                valid = True
                        if valid:
                            table_plan.query_db("DELETE FROM people_in_tables WHERE table_number = ? AND seat_number = ?",(val[2],val[3]))
                            table_plan.query_db("INSERT INTO people_in_tables(table_number,guest_id,seat_number,modified_by_id) VALUES (?,?,?,?)",(val[2],guest_id[0]["guest_id"],val[3],modifying_student_id))
                        else:
                            student = table_plan.query_db("SELECT forename,surname FROM RGS_students WHERE student_id = ?",(guest_links[0]["student_id"],))
                            return "Any guest must be placed on the same table as the student responsible for them. Guest {0} {1} must be placed on the same table as {2} {3}. If you would like to change the student resposible for this guest, please email Josh on HenryJP@rgshw.com.".format(val[0],val[1],student[0]['forename'],student[0]['surname'])

                else:
                    table_plan.query_db("DELETE FROM people_in_tables WHERE table_number = ? AND seat_number = ?",(val[2],val[3]))
                    table_plan.query_db("INSERT INTO people_in_tables(table_number,student_id,seat_number,modified_by_id) VALUES (?,?,?,?)",(val[2],student_id[0]["student_id"],val[3],modifying_student_id))

        student_ids = table_plan.query_db("SELECT student_id FROM people_in_tables")
        for i,id in enumerate(student_ids):
            id = id["student_id"]
            student_ids[i] = id
        while None in student_ids:
            student_ids.remove(None)
        student_ids_set = set(student_ids)
        guest_ids = table_plan.query_db("SELECT guest_id FROM people_in_tables")
        for i,id in enumerate(guest_ids):
            id = id["guest_id"]
            guest_ids[i] = id
        while None in guest_ids:
            guest_ids.remove(None)
        guest_ids_set = set(guest_ids)
        if len(student_ids) == len(student_ids_set):
            if len(guest_ids) == len(guest_ids_set):
                table_plan.query_db("COMMIT")
            else:
                for id in guest_ids_set:
                    guest_ids.remove(id)
                table_plan.query_db("ROLLBACK")
                guest = table_plan.query_db("SELECT forename,surname FROM guests WHERE guest_id = ?",(guest_ids[0],))[0]
                return "There are duplicate students. Guest {0} {1} is entered multiple times".format(guest["forename"],guest["surname"])

        else:
            for id in student_ids_set:
                student_ids.remove(id)
            table_plan.query_db("ROLLBACK")
            student = table_plan.query_db("SELECT forename,surname FROM RGS_students WHERE student_id = ?",(student_ids[0],))[0]
            return "There are duplicate students. Student {0} {1} is entered multiple times".format(student["forename"],student["surname"])


        return "All OK"

'''
SLST sign in
'''


def query_db_slst(query, args=(), one=False):
    cur = get_db_slst().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db_slst():
    DATABASE = "slst.db"
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(path.join(fileDir,DATABASE))
    return db

@app.teardown_appcontext  #closes the database when the file is closed
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/slst_sign_in")
def slst_sign_in():
    names = query_db_slst("SELECT forename,surname,signed_in FROM sign_in")
    # names = [["Test","Person"],["Josh","Henry"]]
    return render_template("slst_index.html",names=names)

@app.route("/slst_changes_made",methods=["POST"])
def slst_changes_made():
    data = request.get_json()
    if data is None:
        return "nothing"
    else:
        ids = query_db_slst("SELECT person_id FROM sign_in")
        for i in range(len(data)):
            query_db_slst("UPDATE sign_in SET signed_in = {0} WHERE person_id = {1}".format(data[i],ids[i][0]))
            get_db_slst().commit()
        return "nothing"


'''
Book a session
'''

class Book_a_session(object):
    def __init__(self):
        self.DATABASE = "book_a_session.db"

    def query_db(self,query, args=()):
        cur = self.get_db().execute(query, args)
        cur.row_factory = dict_factory
        rv = cur.fetchall()
        cur.close()
        self.get_db().commit()
        return rv

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(path.join(fileDir,self.DATABASE))
        return db

    def send_login_email(self,email_record):
        email_address = email_record["email"].lower()
        link = self.get_table_link(email_address)
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        app.config["MAIL_USERNAME"] = "test68duck@gmail.com"
        app.config["MAIL_PASSWORD"] = "qlosiorsjujiuoga"
        subject = "68 Duck Tuition logon link"
        message = render_template("book_a_session_logon_email_message.html",name=email_record["full_name"],link=link)
        mail = Mail(app)
        msg = Message(subject,sender="test68duck@gmail.com",recipients = [email_address])
        msg.html = message
        mail.send(msg)

    def send_confirmation_email(self,email_record):
        email_address = email_record["email"]
        link = self.get_table_link(email_address)
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        app.config["MAIL_USERNAME"] = "test68duck@gmail.com"
        app.config["MAIL_PASSWORD"] = "qlosiorsjujiuoga"
        subject = "Booking confirmation"
        message = render_template("book_a_session_confirmation_email.html",full_name=email_record["full_name"],name=email_record["name"],words_date=email_record["words_date"],time=email_record["time"],hour=email_record["hour"],mins=email_record["mins"])
        mail = Mail(app)
        msg = Message(subject,sender="test68duck@gmail.com",recipients = [email_address])
        msg.html = message
        mail.send(msg)

    def send_approval_email(self,email_record):
        email_address = "Josh@68duck.co.uk"
        link = self.get_table_link(email_address)
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        app.config["MAIL_USERNAME"] = "test68duck@gmail.com"
        app.config["MAIL_PASSWORD"] = "qlosiorsjujiuoga"
        subject = "Booking approval"
        message = render_template("book_a_session_approval_email.html",full_name=email_record["full_name"],name=email_record["name"],words_date=email_record["words_date"],time=email_record["time"],hour=email_record["hour"],mins=email_record["mins"])
        mail = Mail(app)
        msg = Message(subject,sender="test68duck@gmail.com",recipients = [email_address])
        msg.html = message
        mail.send(msg)

    def send_approved_email(self,email_record):
        cal = Calendar()
        cal.add('attendee', 'MAILTO:josh68duck@gmail.com')

        meeting_title = "Tutoring " + email_record["name"]

        event = Event()
        event.add('summary', meeting_title)
        dt = email_record["date"] + " " + email_record["time"]
        dt = datetime.strptime(dt,"%Y-%m-%d %H:%M")
        event.add('dtstart', dt)
        final_dt = dt + timedelta(hours=email_record["hour"],minutes=email_record["mins"])
        event.add('dtend', final_dt)
        # event.add('dtstamp', datetime(2022, 10, 24, 0, 10, 0, tzinfo=pytz.utc))

        organizer = vCalAddress('MAILTO:test68duck@gmail.com')
        organizer.params['cn'] = vText('Josh Henry')
        organizer.params['role'] = vText('Tutor')
        event['organizer'] = organizer
        event['location'] = vText('Gerrards Cross, UK')

        # Adding events to calendar
        cal.add_component(event)

        directory = fileDir + "/invites"
        f = open(path.join(directory, 'invite.ics'), 'wb')
        f.write(cal.to_ical())
        f.close()

        email_address = email_record["email"]
        link = self.get_table_link(email_address)
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        app.config["MAIL_USERNAME"] = "test68duck@gmail.com"
        app.config["MAIL_PASSWORD"] = "qlosiorsjujiuoga"
        subject = "Booking approval"
        message = render_template("book_a_session_approved_email.html",full_name=email_record["full_name"],name=email_record["name"],date=email_record["date"],time=email_record["time"],hour=email_record["hour"],mins=email_record["mins"],email=email_record["email"])
        mail = Mail(app)
        msg = Message(subject,sender="test68duck@gmail.com",recipients = [email_address])
        msg.html = message
        with app.open_resource(fileDir+"/invites/invite.ics") as fp:
            msg.attach("invite.ics", "text/calendar", fp.read())
        mail.send(msg)

    def send_check_email(self,email_record):
        cal = Calendar()
        cal.add('attendee', 'MAILTO:josh68duck@gmail.com')

        meeting_title = "Tutoring " + email_record["name"]

        event = Event()
        event.add('summary', meeting_title)
        dt = email_record["date"] + " " + email_record["time"]
        dt = datetime.strptime(dt,"%Y-%m-%d %H:%M")
        event.add('dtstart', dt)
        final_dt = dt + timedelta(hours=email_record["hour"],minutes=email_record["mins"])
        event.add('dtend', final_dt)
        # event.add('dtstamp', datetime(2022, 10, 24, 0, 10, 0, tzinfo=pytz.utc))

        organizer = vCalAddress('MAILTO:test68duck@gmail.com')
        organizer.params['cn'] = vText('Josh Henry')
        organizer.params['role'] = vText('Tutor')
        event['organizer'] = organizer
        event['location'] = vText('Gerrards Cross, UK')

        # Adding events to calendar
        cal.add_component(event)

        directory = fileDir + "/invites"
        f = open(path.join(directory, 'invite.ics'), 'wb')
        f.write(cal.to_ical())
        f.close()


        email_address = "Josh@68duck.co.uk"
        link = self.get_table_link(email_address)
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        app.config["MAIL_USERNAME"] = "test68duck@gmail.com"
        app.config["MAIL_PASSWORD"] = "qlosiorsjujiuoga"
        subject = "Booking approval"
        message = render_template("book_a_session_check_email.html",full_name=email_record["full_name"],name=email_record["name"],date=email_record["date"],time=email_record["time"],hour=email_record["hour"],mins=email_record["mins"],email=email_record["email"])
        mail = Mail(app)
        msg = Message(subject,sender="test68duck@gmail.com",recipients = [email_address])
        msg.html = message
        with app.open_resource(fileDir+"/invites/invite.ics") as fp:
            msg.attach("invite.ics", "text/calendar", fp.read())
        mail.send(msg)

    def get_email_hash(self,email_address):
        before_hash = "fhsadjkhr2389horuih789q34h" + email_address + "34892y78oghdfuihdfsa789dhsfsadfjkh"
        m = hashlib.sha256()
        m.update(before_hash.encode("utf8"))
        hash = m.hexdigest()
        return hash

    def get_table_link(self,email_address):
        hash = self.get_email_hash(email_address)
        link = "http://68duck.co.uk/book_a_session/" + hash
        return link

def valid_email_format(email_address):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return re.match(regex,email_address)

@app.route("/book_a_session_login_email",methods=["POST"])
def book_a_session_login_email():
    data = request.get_json()
    if data is None:
        return "There was no email input"
    else:
        email_address = data["email"]
        if valid_email_format(email_address):
            book = Book_a_session()
            email_record = data
            book.query_db("INSERT INTO people(full_name,email,price_per_hour) VALUES(?,?,?)",(email_record["full_name"],email_record["email"].lower(),25.00))
            book.send_login_email(email_record)
            return "Email Sent"
        else:
            return "Your email is not in a valid format. Please try again"

@app.route("/book_a_session/<id>")
def book_a_session(id):
    book = Book_a_session()
    emails = book.query_db("SELECT email FROM people")
    for email_dict in emails:
        email = email_dict["email"]
        if id == book.get_email_hash(email):
            full_name = book.query_db("SELECT full_name FROM people WHERE email = ?",(email,))
            if len(full_name) == 0:
                pass
            else:
                table_data = book.query_db("SELECT name,date,time,hour,mins,approved,paid FROM bookings WHERE date > ? AND email = ?",(datetime.now(),email))
                arr = []
                for val in table_data:
                    arr.append([val["name"],val["date"],val["time"],val["hour"],val["mins"],val["approved"],val["paid"]])
                table_data2 = book.query_db("SELECT name,date,time,hour,mins,approved,paid FROM bookings WHERE date < ? AND email = ?",(datetime.now(),email))
                arr2 = []
                for val in table_data2:
                    arr2.append([val["name"],val["date"],val["time"],val["hour"],val["mins"],val["approved"],val["paid"]])
                return render_template("book_a_session.html",full_name = full_name[0]["full_name"],email=email,future_table_data = arr,past_table_data = arr2)
    return render_template("book_a_session_error_page.html")

@app.route("/request_booking",methods=["POST"])
def request_booking():
    data = request.get_json()
    if data is None:
        return "There was no data recieved"
    else:
        date = datetime.strptime(data["date"],"%Y-%m-%d")
        if date < datetime.today():
            return "The date is before today"
        book = Book_a_session()
        name = data["name"]
        time = data["time"]
        hour = data["hour"]
        mins = data["mins"]
        date = data["date"]
        email = data["email"]
        book.query_db("INSERT INTO bookings(email,name,date,time,hour,mins,approved,paid) VALUES (?,?,?,?,?,?,?,?)",(email,name,date,time,hour,mins,0,0))
        email_record = data
        book.send_confirmation_email(email_record)
        book.send_approval_email(email_record)
        return "All OK"

@app.route("/approve_bookings/<id>")
def approve_bookings(id):
    if id != "27a2ec9e892ad4f8d06d2b2adf1156212b1e557bb8626defda96a198aa59c2dc":
        return render_template("book_a_session_error_page.html")
    else:
        book = Book_a_session()
        table_data = book.query_db("SELECT id,email,name,date,time,hour,mins,approved,paid FROM bookings WHERE date > ?",(datetime.now(),))
        arr = []
        for val in table_data:
            arr.append([val["id"],val["email"],val["name"],val["date"],val["time"],val["hour"],val["mins"],val["approved"],val["paid"]])

        previous_table_data = book.query_db("SELECT id,email,name,date,time,hour,mins,approved,paid FROM bookings WHERE date <= ?",(datetime.now(),))
        arr2 = []
        for val in previous_table_data:
            arr2.append([val["id"],val["email"],val["name"],val["date"],val["time"],val["hour"],val["mins"],val["approved"],val["paid"]])

        account_data = book.query_db("SELECT id,full_name,email,price_per_hour FROM people")
        arr3 = []
        for val in account_data:
            arr3.append([val["id"],val["full_name"],val["email"],val["price_per_hour"]])

        return render_template("book_a_session_approve_bookings.html",table_data=arr,previous_table_data=arr2,accounts_data=arr3)


@app.route("/update_approved_bookings",methods=["POST"])
def update_approved_bookings():
    data = request.get_json()
    if data is None:
        return "No data"
    else:
        book = Book_a_session()
        table_data = data["table_information"]
        send_email = data["send_email"]
        for row in table_data:
            id = row[0]
            email = row[1]
            name = row[2]
            date = row[3]
            time = row[4]
            hour = row[5]
            mins = row[6]
            approved = row[7]
            paid = row[8]
            book.query_db("UPDATE bookings SET email = ? WHERE id = ? ",(email,id))
            book.query_db("UPDATE bookings SET name = ? WHERE id = ? ",(name,id))
            book.query_db("UPDATE bookings SET date = ? WHERE id = ? ",(date,id))
            book.query_db("UPDATE bookings SET time = ? WHERE id = ? ",(time,id))
            book.query_db("UPDATE bookings SET hour = ? WHERE id = ? ",(hour,id))
            book.query_db("UPDATE bookings SET mins = ? WHERE id = ? ",(mins,id))
            book.query_db("UPDATE bookings SET approved = ? WHERE id = ? ",("0" if approved == False else "1",id))
            book.query_db("UPDATE bookings SET paid = ? WHERE id = ? ",("0" if paid == False else "1",id))

            if approved and send_email:
                info = book.query_db("SELECT email,name,date,time,hour,mins FROM bookings WHERE id = ?",(id,))
                email_record = info[0]
                full_name = book.query_db("SELECT full_name FROM people WHERE email = ?",(email_record["email"],))
                email_record["full_name"] = full_name[0]["full_name"]
                book.send_approved_email(email_record)
                book.send_check_email(email_record)


        return "All OK"

@app.route("/view_invoice/<full_name>/<email>")
def view_invoice(full_name,email):
    book = Book_a_session()

    table_data = book.query_db("SELECT id,name,date,time,hour,mins FROM bookings WHERE date <= ? AND approved = ? AND paid = ? AND email = ?",(datetime.now(),"1","0",email))
    arr = []
    price_per_hour = book.query_db("SELECT price_per_hour FROM people WHERE email = ?",(email,))[0]["price_per_hour"]
    total_cost = 0
    for val in table_data:
        cost = (val["hour"] + val["mins"]/60) * price_per_hour
        total_cost += cost
        cost = format(cost,".2f")
        arr.append([val["name"],val["date"],val["time"],val["hour"],val["mins"],cost])
    total_cost = format(total_cost,".2f")
    date = datetime.now()
    template = render_template("invoice_email_template.html", date = date.strftime("%d-%m-%y"), name=full_name,table_data = arr,total_cost=total_cost)
    pdf = pdfkit.from_string(template,False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response


'''
Normal website
'''

currentPrice = "40.00"

@app.route("/")
def index():
    return render_template("index.html",currentPrice = currentPrice)

@app.route("/createFile")
def createFile():
    return render_template("createFile.html")

@app.route("/learn")
def learn():
    return render_template("learnFlask.html")

@app.route("/11+Tutoring")
def elevenPlusTutoring():
    return render_template("11+Tutoring.html",currentPrice = currentPrice)

@app.route("/computingAndMathsTutoring")
def computingAndMathsTutoring():
    return render_template("computingAndMathsTutoring.html",currentPrice = currentPrice)

@app.route("/book_a_session_logon")
def book_a_session_logon():
    return render_template("book.html")


if __name__ == "__main__":      #runs the application
    app.run()     #debug allows us to not have to refresh every time
