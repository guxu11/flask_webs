from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField,FloatField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from flask_wtf.file import file_required,FileField

class RegisterForm(FlaskForm):
    username = StringField('User Name',
                           validators=[DataRequired(),
                                       Length(min=4, max=16,
                                              message="Please enter 4-16 bits combination of letters and numbers")],
                           render_kw={'id': 'username',

                                      'placeholder': 'User Name:4-16 letters and numbers'})
    email = StringField('Email',
                        validators=[DataRequired(), Email(message="Wrong Email address format ")],
                        render_kw={'id': 'email',
                                   'placeholder': 'E-mail:xx@xx.com'})
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, max=16,
                                                message="Please Enter 6-16 bits combination of letters and numbers")],
                             render_kw={'id': 'password',
                                        'placeholder': 'Password:6-16 letters and numbers'})
    re_enter = PasswordField('re-enter',
                             validators=[DataRequired(), EqualTo('password', 'The passwords entered are not equal')],
                             render_kw={'placeholder': 'Re-enter Password'})
    license = FileField('license',
                        validators=[file_required()]
                        )

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'E-mail'})
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw={'placeholder': 'Password'})

