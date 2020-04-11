from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Form, BooleanField, PasswordField, validators, IntegerField, SelectField, DateField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from datetime import date



class TitleForm1(FlaskForm):
    title1 = StringField('List 1 Title:', validators=[Length(min=2, max=20)])
    submit1 = SubmitField('Update Title')
    
class TitleForm2(FlaskForm):
    title2 = StringField('List 2 Title:', validators=[Length(min=2, max=20)])
    submit2 = SubmitField('Update Title')


class TitleForm3(FlaskForm):
    title3 = StringField('List 3 Title:', validators=[Length(min=2, max=20)])
    submit3 = SubmitField('Update Title')
    
class SignupForm(Form):
    name = StringField('Name and Last Name', [DataRequired(), validators.Length(min=6, max=30)])
    username = StringField('Username', [DataRequired(), validators.Length(min=6, max=25)])
    email = StringField('Email', [DataRequired(), validators.Length(min=6, max=35), validators.Email(message='Enter a valid email.')])
    password = PasswordField('Password', [validators.Length(min=8),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Sign up')

    

class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class EditAccountForm(FlaskForm):
    def __init__(self, name, username, email, password, confirm, submit):
        username = StringField('Username',
                           validators.Length(min=6, max=25))
        email = StringField('Email',
                        validators=[Email()])
        password = PasswordField('Password', [validators.Length(min=8),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
        confirm = PasswordField('Repeat Password')
        submit = SubmitField('Submit')

    def __repr__(self):
        return f'<User: {self.email}>'

class CreditcardForm(Form):
    card_type = StringField('Card Type')
    name_on_card = StringField('Name on Card', [DataRequired(), validators.Length(min=6, max=30)])
    card_number = IntegerField('Card Number', [DataRequired(), validators.NumberRange(min=100000000000000, max=9999999999999999)])
    cvv = IntegerField('CVV', [DataRequired(), validators.NumberRange(min=000, max=9999)])
    exp_month = StringField('Expiration Month')
    exp_year = StringField('Expiration Year')
    submit = SubmitField('Submit')

class AddressForm(Form):
    nickname = StringField('Nickname')
    name = StringField('Name and Last name')
    address_line_1 = StringField('Address Line 1')
    address_line_2 = StringField('Address Line 2')
    city = StringField('City')
    state = SelectField('State', choices=['Alabama','Alaska' , 'Arizona' ,'Arkansas' ,'California' ,'Colorado' ,'Connecticut', 'Delaware' ,
                        'Florida' ,'Georgia' ,'Hawaii', 'Idaho' ,'Illinois', 'Indiana' ,'Iowa' , 'Kansas' ,'Kentucky' ,'Louisiana' ,
                        'Maine', 'Maryland' ,'Massachusetts' ,'Michigan' ,'Minnesota' ,'Mississippi' ,'Missouri' ,'Montana' 'Nebraska' ,'Nevada' ,
                        'New Hampshire' ,'New Jersey', 'New Mexico' ,'New York' ,'North Carolina' ,'North Dakota' ,'Ohio' ,
                        'Oklahoma' ,'Oregon','Pennsylvania' ,'Rhode Island','South Carolina' , 'South Dakota','Tennessee' ,'Texas' ,
                        'Utah','Vermont' ,'Virginia' ,'Washington' ,'West Virginia','Wisconsin' ,'Wyoming'])
    zip = StringField('Zip Code')
    submit = SubmitField('Submit')

