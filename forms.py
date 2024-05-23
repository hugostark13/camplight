from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp
import email_validator


class Search(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Search")


class Add(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired("Please enter your name."), Length(min=2, max=50)],
    )
    email = StringField(
        "E-Mail",
        validators=[
            DataRequired("Please enter your email address."),
            Email(message="Invalid email address."),
            Length(max=120),
        ],
    )
    phone = StringField(
        "Phone",
        validators=[
            DataRequired("Please enter your phone."),
            Regexp(
                r"^\+?\d{8,15}$",
                message="Invalid phone number format. (e.g., +359889789)",
            ),
        ],
    )
    submit = SubmitField("Add")
