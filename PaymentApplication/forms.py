from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TelField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import EmailField
from PaymentApplication.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Student Name', validators=[DataRequired(), Length(min=2, max=20)])
    rollnumber = StringField('Roll Number', validators=[DataRequired()])
    branch = StringField('Branch', validators=[DataRequired()])
    email = EmailField('Official Email-ID', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, Please choose a different one')


class LoginForm(FlaskForm):
    email = EmailField('Official Email-ID', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PaymentForm(FlaskForm):
    submit = SubmitField('Select Payment Method')
    cancel=SubmitField('Cancel',render_kw={'formnovalidate': True})
    amount = StringField('Amount', validators=[DataRequired()])
    myChoices = [('Mess', 'Mess Fee'), ('Tuition', 'Tuition Fee'), ('Hostel', 'Hostel Fee'),
                 ('Examination', 'Examination Fee')]
    myField = SelectField('Payment Category', choices=myChoices, validators=[DataRequired()])


class NetBankingForm(FlaskForm):
    myChoices = [('Please Select Your Bank', 'Please Select Your Bank'), ('SBI', 'SBI'), ('CANARA', 'CANARA'),
                 ('HDFC', 'HDFC'), ('KOTAK', 'KOTAK'), ('ICICI', 'ICICI')]
    bank = SelectField('Select Your Bank', choices=myChoices, validators=[DataRequired()])
    submit = SubmitField('Proceed Payment')


class UpiForm(FlaskForm):
    upiid = StringField('Please Enter Your UPI ID ', validators=[DataRequired()])
    submit = SubmitField('Proceed Payment')

class CardForm(FlaskForm):
    name=StringField("Cardholder's Name", validators=[DataRequired()])
    number=TelField("Card Number", validators=[DataRequired(),Length(max=19,min=19)])
    cvv=PasswordField('CVV',validators=[DataRequired(),Length(max=3,min=3)])
    expiry=PasswordField('Expiry',validators=[DataRequired(),Length(min=4,max=4)])
    submit = SubmitField('Proceed Payment')
    

   


