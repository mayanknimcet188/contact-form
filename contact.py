from flask import Flask, render_template, flash, redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Email,Length
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess'
class QueryForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    subject = StringField('Subject',validators=[DataRequired(),Length(0,64,'Subject Should be between 0 to 64 characters')])
    query = TextAreaField('Query',validators=[DataRequired()])

@app.route('/',methods=['GET','POST'])
def index():
    form = QueryForm()
    if form.validate_on_submit():
        flash('Your query has been submitted')
        return redirect(url_for('index'))
    return render_template('contact.html',form=form)

