from flask_wtf import FlaskForm
from flask_table import Table, Col, BoolCol, DateCol
from wtforms.fields import (
    TextAreaField,
    SubmitField,
    StringField,
    PasswordField,
    SelectField,
    HiddenField
)
from wtforms.validators import InputRequired, Length, Email, EqualTo


# creates the login information
class LoginForm(FlaskForm):
    emailid = StringField("Email Address", validators=[
        InputRequired('Enter email address')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    name = StringField("First Name", validators=[InputRequired()])
    lastName = StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[
                        Email("Please enter a valid email")])

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")


class CreateForm(FlaskForm):

    tool_name = StringField("Title", validators=[InputRequired()])
    modelNo = StringField("Model Number", validators=[InputRequired()])
    list_price = StringField("Price", validators=[InputRequired()])
    category = SelectField(
        u"Category",
        choices=[
            ("Gardening", "Gardening"),
            ("Garage Tools", "Garage Tools"),
            ("Renovation Tools", "Renovation Tools"),
            ("Industrial Tools", "Industrial Tools"),
            ("Other Tools", "Other Tools"),
        ],
    )
    desc = StringField("Description", validators=[InputRequired()])
    brand = StringField("Brand", validators=[InputRequired()])
    submit = SubmitField("Create")


class SearchForm(FlaskForm):
    search = StringField("")
    search_button = SubmitField("Search")


class LandingForm(FlaskForm):
    landing_search = StringField("", validators=[InputRequired()])
    landing_search_button = SubmitField("Search")


class Results(Table):
    tool_name = Col("title")
    modelNo = Col("modelNo")
    list_price = Col("price")
    category = Col("category")
    desc = Col("description")
    brand = Col("brand")
    date_created = DateCol("date")
    sold_status = Col("sold")


class MarkSold(FlaskForm):
    bid_user_id = HiddenField('bid_user id', '{{user.user_id}}')
    submit = SubmitField("Mark as Sold")


class UndoSold(FlaskForm):
    undoSold = HiddenField("zero")
    submit_undo = SubmitField("Undo")


class BidForm(FlaskForm):
    bidamount = StringField("Bid Amount", validators=[InputRequired()])
    submit = SubmitField("Submit Bid")
