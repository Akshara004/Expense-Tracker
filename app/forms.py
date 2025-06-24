from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class ExpenseForm(FlaskForm):
    amount = FloatField('Amount', validators=[InputRequired()])
    category = StringField('Category', validators=[InputRequired(), Length(max=100)])
    description = StringField('Description', validators=[Length(max=255)])
    submit = SubmitField('Add Expense')

