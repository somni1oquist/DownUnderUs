from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, InputRequired

class CreatePostForm(FlaskForm):
    title = StringField('Give it a title:', validators=[Length(min=3,max=100, message='Please enter a proper title')])
    body = StringField('Content', validators=[Length(min=10,message='Please enter a proper content')])
    topic = StringField('Topic', validators=[InputRequired(message='Please select a topic')])
    location = StringField('Location')
    submit = SubmitField('Post')