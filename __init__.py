import csv
from datetime import timedelta
from os import path
import sqlite3
from flask import g,Flask,render_template,request
from os import path

fileDir = path.dirname(__file__) # for loading images

app = Flask(__name__)   #creates the application flask

app.secret_key = "b6jF" #sets secret key for encription i.e. my encription + first words quack

DATABASE = 'flaskTest.db'
currentTableName = None
alerts = []
messages = []

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
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


currentPrice = "£25.00"

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


if __name__ == "__main__":      #runs the application
    app.run()     #debug allows us to not have to refresh every time
