from flask_wtf import Form
from wtforms import StringField, PasswordField, FileField, BooleanField, HiddenField, TextAreaField
from wtforms.validators import DataRequired


class SignUpForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    address_1 = StringField("Address Line 1", validators=[DataRequired()])
    address_2 = StringField("Address Line 2")
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip = StringField("Zip Code", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    phone_number = StringField("Phone Number")
    profile_picture = FileField("Profile Picture")
    profile_picture_crop_options = HiddenField()


class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")


class RecoveryForm(Form):
    email = StringField("Email", validators=[DataRequired()])


class AdvancedSearchForm(Form):
    vendor_name = StringField("Vendor name")
    piece_name = StringField("Piece name")
    medium = StringField("Medium")
    price_low = StringField("Price low")
    price_high = StringField("Price high")
    width = StringField("Width")
    height = StringField("Height")


class SellAnArtworkForm(Form):
    piece_name = StringField("Piece Name")
    medium = StringField("Medium", validators=[DataRequired()])
    width = StringField("Width", validators=[DataRequired()])
    height = StringField("Height", validators=[DataRequired()])
    starting_bid = StringField("Starting Bid", validators=[DataRequired()])
    buy_now = StringField("Buy Now")
    artwork_picture = FileField("Artwork", validators=[DataRequired()])
    artwork_description = TextAreaField("Artwork Description")


