from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class Search(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Search")


class Add(FlaskForm):
    name = StringField("Name", validators=[DataRequired("Please enter your name.")])
    email = StringField(
        "E-Mail", validators=[DataRequired("Please enter your email address.")]
    )
    phone = StringField("Phone", validators=[DataRequired("Please enter your phone.")])
    submit = SubmitField("Add")
