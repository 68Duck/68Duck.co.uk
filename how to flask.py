from flask import *
import csv
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from os import path


fileDir = path.dirname(__file__) # for loading images

app = Flask(__name__)   #creates the application flask

app.secret_key = "b6jF" #sets secret key for encription i.e. my encription + first words quack

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"       #configures the app/ "users" is the table used
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  #removes deprication warning

app.permanent_session_lifetime = timedelta(minutes = 5)     #sets the session data timer for 5 mins

db = SQLAlchemy(app)    #creates database


admin = True


class Users(db.Model): #interits from database
    _id = db.Column("id",db.Integer,primary_key = True) #creates id number. primary_key tells it that this is the thing we will use to identify it
    username = db.Column(db.String(100))    #100 in db.String is the max length of the string able to be stored
    password = db.Column(db.String(100))        #the name of the column will use the variable name i.e. username or password so we dont need to define it

    def __init__(self,username,password):   #we dont need the id as priamry key automatically creates one
        self.username = username
        self.password = password

def addCharsToList(theList,start,length):
    for i in range(length):
        theList.append(chr(i+start))
    return theList

def generateCharacters():
    characters = []
    characters = addCharsToList(characters,48,10)
    characters = addCharsToList(characters,65,26)
    characters = addCharsToList(characters,97,26)
    return characters


def encrypt(word):
    wordLength = len(word)
    characters = generateCharacters()

    firstWord = []
    for letterNumber in range(len(word)):
        for characterNumber in range(len(characters)):
            if characters[characterNumber] == word[letterNumber]:
                break

        letterKey = letterNumber + 1
        letterKey = letterKey**wordLength + wordLength*letterNumber*68 + letterNumber + 68**2 - wordLength*letterKey*characterNumber
        letterKey = letterKey//1
        if letterKey<0:
            letterKey = letterKey * -1
        #print(letterKey)
        newCharacterNumber = characterNumber + letterKey
        while newCharacterNumber >= len(characters):
            newCharacterNumber -= len(characters) + 1
        newLetter = characters[newCharacterNumber]
        #print(newLetter)
        firstWord.append(newLetter)

    secondWord = []

    for letterNumber in range(len(firstWord)):
        for characterNumber in range(len(characters)):
            if characters[characterNumber] == word[letterNumber]:
                break
        letter = firstWord[letterNumber]
        if letterNumber == len(firstWord):
            method = "1"
        elif (characterNumber+letterNumber**2-len(firstWord))//1 % 2 == 0:
            method = "2"
        else:
            method = "3"

        if method == "1":
            secondWord.append(letter)
        elif method == "2":
            newLetterNumber1 = (characterNumber/wordLength + wordLength*characterNumber)//1
            newLetterNumber2 = maths.sqrt(wordLength*characterNumber)//1
            while newLetterNumber1 >= len(characters):
                newLetterNumber1 -= len(characters) + 1
            while newLetterNumber2 >= len(characters):
                newLetterNumber2 -= len(characters) + 1
            newLetterNumber1 = int(newLetterNumber1)
            newLetterNumber2 = int(newLetterNumber2)
            newLetter1 = characters[newLetterNumber1]
            newLetter2 = characters[newLetterNumber2]
            secondWord.append(newLetter1)
            secondWord.append(newLetter2)

        else:       #i.e. method == 3
            pass

    returningWord = ""
    for character in secondWord:
        returningWord+=character
    return returningWord



def reader(fileName):
    with open(fileName, newline='') as f:
        reader = csv.reader(f)
        returning = []
        for row in reader:
            returning.append(row)
        return returning


def writer(fileToWrite,fileName):
    with open(fileName, mode = "w", newline = "") as file:
        writer = csv.writer(file)
        for row in fileToWrite:
            writer.writerow(row)


@app.route("/test")  #how to get to the home page e.g. youtube.com/watch where watch is the inserted element here. / is the default
def home():
    return "<h1>Hello</h1> hello2"


@app.route("/<name>")   #the name in <name> when typed in will be passed into function user
def user(name):
    return f"Hello {name}"

@app.route("/index")
def home2():
    return render_template("index.html",test = "test",theList = ["red","green","blue"])  #renders the html file in templates called index.html
                                            #you can pass in values after a comma and use {{variable}} in the html to use that variable
                                                #in the html file use {% python code%} write actual code instead of "python code" to write python in the html file

@app.route("/loginError")
def loginError():
    return render_template("loginError.html")


@app.route("/learn")
def learn():
    return render_template("learn.html")


#@app.route("/imageTest")
#def test2():
#    return render_template("imageTest.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":        #so using post not get meaning that has tried to log in
        if "accessGranted" in session:
            if session["accessGranted"] == True:
                flash("You have already logged in","info")
                return redirect(url_for("loggedInPage"))
        username = request.form["username"] #gets username entered into the username box
        password = request.form["password"]
        usersList = reader(path.join(fileDir,"users.csv"))
        accessGranted = False
        session["username"] = username
        session["password"] = password
        for user in usersList:
            if user[0] == username:
                if user[1] == password:
                    accessGranted = True
                    session["accessGranted"] = True
        if accessGranted == True:
            flash("You have been logged in","info") #creates a flash bar with icon info. needs stuff in login page also
            return redirect(url_for("loggedInPage"))
        else:
            flash("An error occured. Your username or password may be incorrect. Please try again","error") #creates a flash bar with icon info. needs stuff in login page also
            return render_template("login.html")
            #return render_template("loginError.html")
    else:
        #if logout == True:
        #    return render_template("login.logout")
        #else:
        if "accessGranted" in session:
            if session["accessGranted"] == True:
                flash("You have already logged in","info")
                return redirect(url_for("loggedInPage"))
        return render_template("login.html")


@app.route("/login/user")
def loggedInPage():
    if session["accessGranted"] == True:   #i.e. if logged in
        username = session["username"]
        password = session["password"]
        return render_template("loggedin.html")
    else:
        print("bye")
        #return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "username" in session and "password" in session:
        username = session["username"]
        password = session["password"]
        flash("You have been logged out","info") #creates a flash bar with icon info. needs stuff in login page also

    session.pop("username",None)
    session.pop("password",None)
    session.pop("accessGranted",None)

    return redirect(url_for("login"))

@app.route("/")
def test():
    return render_template("index2.html")

@app.route("/admin") #admin page
def admin():
    if admin:
        return redirect(url_for("user", name = "Admin"))  #goes to user page with name being Admin. DONT MAKE THE VARIABLE NAMES THE SAME AS A FUNCTION!
    else:
        return redirect(url_for("home"))  # goes to the home function if you type into the url /admin


@app.route("/learnFlask")
def learnFlask():
    return render_template("learnFlask.html")


if __name__ == "__main__":      #runs the application
    db.create_all() #creates the database if dosent already exist
    app.run()     #debug allows us to not have to refresh every time
