from flask_wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms.validators import DataRequired


class SignUpForm(Form):
    username = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])


class LoginForm(Form):
    username = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")


class RecoveryForm(Form):
    email = StringField("Email", validators=[DataRequired()])


class AdvancedSearchForm(Form):
    vendor_name = StringField("Vendor_name")
    piece_name = StringField("Piece_name")
    medium = StringField("Medium")
    price_low = StringField("Price_low")
    price_high = StringField("Price_high")
    width = StringField("Width")
    height = StringField("Height")
