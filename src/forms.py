from flask_wtf import Form
from wtforms import *
from wtforms.validators import DataRequired


class SignUpForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    address_1 = StringField("Address Line 1", validators=[DataRequired()])
    address_2 = StringField("Address Line 2")
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired])
    country = StringField("Country", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired])
    profile_picture = FileField("Profile Picture")


class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired()])
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
