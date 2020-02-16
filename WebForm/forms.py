from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import (StringField,SelectField,SelectMultipleField ,PasswordField,DecimalField,DateField,
 BooleanField,IntegerField,TextAreaField, SubmitField, MultipleFileField)
from wtforms.validators import DataRequired, Length, ValidationError, Email,NumberRange


#
class BaseForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    #整型数值，範圍在18到70之间
    age=IntegerField('age',validators=[NumberRange(min=18,max=70)])
    # Text Field 保留小數一位
    height = DecimalField('Height (Centimeter)', places=1)
    # Text Field "%Y/%m/%d
    birthday = DateField('Birthday', format='%Y/%m/%d')
     # Select类型，下拉单选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    job = SelectField('Job', choices=[
        ('teacher', 'Teacher'),
        ('doctor', 'Doctor'),
        ('engineer', 'Engineer'),
        ('lawyer', 'Lawyer')
    ])
     # Select类型，多选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    hobby = SelectMultipleField('Hobby', choices=[
        ('swim', 'Swimming'),
        ('skate', 'Skating'),
        ('hike', 'Hiking')
    ])

     # Text Area类型，段落输入框
    description = TextAreaField('Introduction of yourself')

    # Checkbox类型，加上default='checked'即默认是选上的
    accept_terms = BooleanField('I accept the Terms of Use', default='checked',
                                validators=[DataRequired()])

    submit = SubmitField('Log in')

class SelectForm(FlaskForm):

    #init 傳入資料

    dayStart = DateField('Birthday', format='%Y/%m/%d')
    dayEnd = DateField('Birthday', format='%Y/%m/%d')

    modelGroup = SelectField('ModelGroup', choices=[
        ('3806', '3806'),
        ('7020', '7020'),       
    ])

    accept_terms = BooleanField('I accept the Terms of Use', default='checked',
                                validators=[DataRequired()])

    submit = SubmitField('submit')        
