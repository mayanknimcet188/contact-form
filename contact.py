from flask import Flask, render_template, flash, redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Email,Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)



app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
        flash('Your query has been submitted')
        return redirect(url_for('index'))
    return render_template('contact.html',form=form)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Query=Query)