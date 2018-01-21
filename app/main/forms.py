from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddPostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    post = TextAreaField('Text', validators=[DataRequired(), Length(min=10, max=158)])
    image = StringField('Image', validators=[Length(min=6, max=512)])
    link = StringField('Link', validators=[DataRequired()])
    tags = StringField('Tags')

class addMyComment(Form):
    postId = StringField('postId', validators=[DataRequired()])
    comment = TextAreaField('Text' , validators=[DataRequired() , Length(min=1 , max=256)])
    userId = StringField('userId' , validators=[DataRequired()])