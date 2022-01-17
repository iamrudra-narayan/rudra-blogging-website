from flask_wtf import FlaskForm 
from wtforms import StringField,PasswordField,SubmitField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import InputRequired,Length,EqualTo,Email,ValidationError

#FORMS
class RegistrationForm(FlaskForm):
    username = StringField('username_label', validators=[InputRequired(message="Username Required")])
    email = StringField('email_label', validators=[InputRequired(message="Email Required"), Email(message="Wrong email format")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password Required"), Length(min=6, max=25, message="Please enter password")])
    confirm_pswd = PasswordField('Confirm_pswd_label', validators=[InputRequired(message="ConfirmPswd Required"), EqualTo('password', message="Confirm Password Should be Equal to Password")])

    submit_button = SubmitField('Register')
    
    #def validate_username(self, username):
        #user = User.query.filter_by(username=username).first()
        #if user:
            #raise ValidationError("That Username is Taken. Try different Username!")
        
    #def validate_email(self, email):
        #user = User.query.filter_by(email=email).first()
        #if user:
            #raise ValidationError("That Email is Taken. Try different Email!")
            
class LoginForm(FlaskForm):
    email = StringField('email_label', validators=[InputRequired(message="Email Required"), Email(message="Wrong email format")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password Required"), Length(min=6, max=25, message="Please enter a validpassword")])

    submit_button = SubmitField('Login')
    
    
class BlogPostForm(FlaskForm):
    title = StringField('username_label', validators=[InputRequired(message="Title Required")])
    description = StringField('email_label', validators=[InputRequired(message="Description Required")])
    file = FileField('Post an Image', validators=[FileAllowed(['jpg','jpeg','png']), InputRequired(message="Please Select an Image") ])
    submit_button = SubmitField('POST')
    
class UpdateBlogForm(FlaskForm):
    title = StringField('username_label', validators=[InputRequired(message="Title Required")])
    description = StringField('email_label', validators=[InputRequired(message="Description Required")])
    file = FileField('Post an Image', validators=[FileAllowed(['jpg','jpeg','png']), InputRequired(message="Please Select an Image") ])
    submit_button = SubmitField('UPDATE')
        