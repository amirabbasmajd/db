from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class AddPostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    post = TextAreaField('Text', validators=[DataRequired(), Length(min=10, max=158)])
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    link = StringField('Link', validators=[DataRequired()])
    tags = StringField('Tags')

class EditPostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    post = TextAreaField('Text', validators=[DataRequired(), Length(min=10, max=158)])
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    link = StringField('Link', validators=[DataRequired()])
    tags = StringField('Tags')


class addComment(Form):
    addYourComment = StringField('comment', validators=[DataRequired()])


class SearchForm(Form):
    search_text = StringField('text', validators=[DataRequired()])


class RegistrationForm(Form):
    full_name = StringField('Full name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
