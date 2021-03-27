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



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/createFile")
def createFile():
    return render_template("createFile.html")

@app.route("/learn")
def learn():
    return render_template("learnFlask.html")

@app.route("/11+Tutoring")
def elevenPlusTutoring():
    return render_template("11+Tutoring.html")

@app.route("/computingAndMathsTutoring")
def computingAndMathsTutoring():
    return render_template("computingAndMathsTutoring.html")


if __name__ == "__main__":      #runs the application
    db.create_all() #creates the database if dosent already exist
    app.run()     #debug allows us to not have to refresh every time
