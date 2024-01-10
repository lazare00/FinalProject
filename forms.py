from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms.fields import StringField, IntegerField, SubmitField, PasswordField, RadioField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, length, equal_to

class AddWorkForm(FlaskForm):
    name = StringField("Work name", validators=[DataRequired()])
    person = StringField("Author's name", validators=[DataRequired()])
    img = FileField("Upload work", validators=[FileRequired()])

    submit = SubmitField("Add")


class EditWorkForm(FlaskForm):
    name = StringField("Work name", validators=[DataRequired()])
    person = StringField("Author's name", validators=[DataRequired()])
    img = FileField("Upload work")

    submit = SubmitField("Add")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired(),
                                 length(min=8, max=99)
                             ])
    repeat_password = PasswordField("Repeat password",
                                    validators=[
                                        DataRequired(),
                                        equal_to("password", message="Passwords do not match")
                                    ])

    register = SubmitField("Registration")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    login = SubmitField("Login")

class AddCommentForm(FlaskForm):
    text = TextAreaField("Comments", validators=[DataRequired()])
    submit = SubmitField("Add comment")


