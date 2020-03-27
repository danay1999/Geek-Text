from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length


class TitleForm1(FlaskForm):
    title1 = StringField('List 1 Title:', validators=[Length(min=2, max=20)])
    submit1 = SubmitField('Update Title')
    
class TitleForm2(FlaskForm):
    title2 = StringField('List 2 Title:', validators=[Length(min=2, max=20)])
    submit2 = SubmitField('Update Title')


class TitleForm3(FlaskForm):
    title3 = StringField('List 3 Title:', validators=[Length(min=2, max=20)])
    submit3 = SubmitField('Update Title')