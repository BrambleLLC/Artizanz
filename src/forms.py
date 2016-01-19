from flask_wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired


class SignUpForm(Form):
    username = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])


class LoginForm(Form):
    username = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RecoveryForm(Form):
    email = StringField("Email", validators=[DataRequired()])

