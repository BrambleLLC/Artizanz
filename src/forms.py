from flask_wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired


class SignUp(Form):
    username = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
