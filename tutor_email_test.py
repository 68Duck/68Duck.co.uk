from os import path
import sqlite3
from flask import g,Flask,render_template,request,make_response
from flask_mail import Mail, Message
from os import path
import hashlib
import json
from datetime import datetime
import pdfkit

fileDir = path.dirname(__file__) # for loading images
app = Flask(__name__)   #creates the application flask
app.secret_key = "b6jF" #sets secret key for encription i.e. my encription + first words quack


def send_email(email_record):
    email_address = email_record["email_address"]
    pdf = email_record["pdf"]
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config["MAIL_USERNAME"] = "test68duck@gmail.com"
    app.config["MAIL_PASSWORD"] = "qlosiorsjujiuoga"

    subject = "Tuition Invoice"
    message = render_template("invoice_message.html",name=email_record["full_name"])
    mail = Mail(app)
    msg = Message(subject,sender="test68duck@gmail.com",recipients=[email_address])
    msg.html = message
    msg.attach("invoice.pdf","application/pdf",pdf)
    mail.send(msg)



@app.route("/test")
def test():
    date = datetime.now()
    full_name = "Test Person"
    template = render_template("invoice_email_template.html", date = date.strftime("%d-%m-%y"), name=full_name)
    pdf = pdfkit.from_string(template,False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    record = {"email_address":"josh68duck@gmail.com","pdf":pdf,"full_name":full_name}
    send_email(record)
    return response


if __name__ == "__main__":
    app.run()
