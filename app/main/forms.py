from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
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


class addComment(Form):
    addYourComment = StringField('comment', validators=[DataRequired()])


class SearchForm(Form):
    search_text = StringField('text', validators=[DataRequired()])


class addMyComment(Form):
    postId = StringField('postId', validators=[DataRequired()])
    comment = TextAreaField('Text', validators=[DataRequired(), Length(min=1, max=256)])
    userId = StringField('userId', validators=[DataRequired()])
