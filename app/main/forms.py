from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField , FileField
from wtforms.validators import DataRequired, Length


class AddPostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    post = TextAreaField('Text', validators=[DataRequired(), Length(min=10, max=158)])
    image = FileField('Image', validators=[])
    link = StringField('Link', validators=[DataRequired()])
    tags = StringField('Tags')

class addComment(Form):
    addYourComment = StringField('comment', validators=[DataRequired()])
