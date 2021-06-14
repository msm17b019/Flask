from datetime import datetime
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail


with open("config.json","r") as c:
    params=json.load(c)["params"]

local_server=True

app=Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-pswd']
)

mail=Mail(app)

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI']=params['prod_uri']

db=SQLAlchemy(app)

class Contact(db.Model):
    '''
    sno,name,email,phone_num,msg,date
    '''
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(120),nullable=False)
    email=db.Column(db.String(20),nullable=False)
    phone_num=db.Column(db.String(12),nullable=False)
    msg=db.Column(db.String(120),nullable=False)
    date=db.Column(db.String(12),nullable=True)


@app.route('/')
def home():
    return render_template('index.html',params=params)

@app.route('/about')
def about():
    return render_template('about.html',params=params)

@app.route('/contact',methods=['GET','POST'])
def contact():
    if (request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')

        '''
            sno,name,email,phone_num,msg,date
        '''

        entry=Contact(name=name,email=email,phone_num=phone,msg=message,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New Message from '+ name,
        sender=email,
        recipients=[params['gmail-user']],
        body=message + "\n" + phone 
        )

    return render_template('contact.html',params=params)

@app.route('/post')
def post():
    return render_template('post.html',params=params)


if __name__=="__main__":
    app.run(debug=True)