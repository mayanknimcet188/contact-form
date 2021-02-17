from flask import Flask, render_template, flash, redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Email,Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from threading import Thread

import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)



app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

app.config['MAIL_SUBJECT_PREFIX'] = '[Query]'
app.config['MAIL_SENDER'] = 'Admin <mayank.nimcet.188@gmail.com>'

app.config['ADMIN'] = os.environ.get('ADMIN')


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr

class QueryForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    subject = StringField('Subject',validators=[DataRequired(),Length(0,64,'Subject Should be between 0 to 64 characters')])
    query = TextAreaField('Query',validators=[DataRequired()])

class Query(db.Model):
    __tablename__ = 'queries'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    subject = db.Column(db.String(100))
    query = db.Column(db.Text())

    def __repr__(self):
        return '<Query %r>' % self.name

@app.route('/',methods=['GET','POST'])
def index():
    form = QueryForm()
    if form.validate_on_submit():
        new_query = Query(name=form.name.data,email=form.email.data,subject=form.subject.data,query=form.query.data)
        db.session.add(new_query)
        db.session.commit()
        if app.config['ADMIN']:
            send_email(app.config['ADMIN'], 'New Query Posted', 'mail/new_query',query=new_query)
            flash('Your query has been submitted')
        return redirect(url_for('index'))
    return render_template('contact.html',form=form)



@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Query=Query)