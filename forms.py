from flask_security.forms import ConfirmRegisterForm, TextField,ForgotPasswordForm, SendConfirmationForm
from wtforms import  validators
from settings import flash
from model import User
#create new forms for name

class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
    name=TextField('Name',[validators.Length(min=1, max=35)])

class CustomForgotPasswordForm(ForgotPasswordForm):
    def validate(self):

        user = User.query.filter_by(email=self.email.data).first()
        if not user is None and user.has_role("blocked"):
            flash('You are in blacklist')
            return False
        else:
            return super(CustomForgotPasswordForm, self).validate()

class CustomSendConfirmationForm(SendConfirmationForm):
    def validate(self):

        user = User.query.filter_by(email=self.email.data).first()
        if not user is None and user.has_role("blocked"):
            flash('You are in blacklist')
            return False
        else:
            return super(CustomSendConfirmationForm, self).validate()
