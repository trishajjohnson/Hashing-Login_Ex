from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, EqualTo, Length

class AddUserForm(FlaskForm):
    """Form for adding a new user."""

    username = StringField("Username", validators=[InputRequired(message="Please enter a unique username"), Length(max=20, message="Username must be 2o characters or less")])
    password = PasswordField("Password", validators=[InputRequired(message="Please enter a password"), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    email = StringField("Email Address", validators=[InputRequired(message="Please enter an email address"), Length(max=50, message="Email must be 50 characters or less")])
    first_name = StringField("First Name", validators=[InputRequired(message="Please enter your first name"), Length(max=30, message="First name must be 3o characters or less")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Please enter your last name"), Length(max=30, message="Last name must be 3o characters or less")])


class LoginUserForm(FlaskForm):
    """For for loggin in user."""

    username = StringField("Username", validators=[InputRequired(message="Please enter your username"), Length(max=20, message="Username must be 2o characters or less")])
    password = PasswordField("Password", validators=[InputRequired(message="Please enter your password")])
    

class NewFeedbackForm(FlaskForm):
    """Create new Feedback form."""

    title = StringField("Title", validators=[InputRequired(message="Please enter a title"), Length(max=100, message="Title must be 100 characters or less")])
    content = TextAreaField("Content", validators=[InputRequired(message="Please enter content")])


class EditFeedbackForm(FlaskForm):
    """Edit Feedback form."""

    title = StringField("Title", validators=[InputRequired(message="Please enter a title"), Length(max=100, message="Title must be 100 characters or less")])
    content = TextAreaField("Content", validators=[InputRequired(message="Please enter content")])