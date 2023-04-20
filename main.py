from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


with open("config.json","r") as c:
    params=json.load(c)["params"] #yha left wala params main.py ka variable hai ar ye wala- ["params"] config.json se aya hai
local_server=True
app = Flask(__name__)
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):# Contacts must start with capital letter
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(120),nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12),nullable=True)
    email = db.Column(db.String(20), nullable=False)

@app.route("/")
def home():
    return render_template('index.html',params=params)


@app.route("/about")
def about():
    return render_template('about.html',params=params) #left wala params jinjaa temp ka hai right wala params main.py ka hai

@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        """Add entry to the database"""
        name=request.form.get("name")
        email=request.form.get("email")
        phone=request.form.get("phone")
        message=request.form.get("message")

        """ sno,name,phone,msg,date,email"""
        entry=Contacts(name=name,phone=phone,msg=message,date=datetime.now( ),email=email)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html',params=params)

@app.route("/post")
def post():
    return render_template('post.html',params=params)

app.run(debug=True)