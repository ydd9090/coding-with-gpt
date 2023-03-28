from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Regexp
from wtforms import StringField,SubmitField,ValidationError
from .models import Account


class AccountForm(FlaskForm):
    phone_num = StringField('Phone Number', validators=[DataRequired(),Regexp("^\d{11}$",message="请输入有效的手机号码")])
    phone_code = StringField('Phone Code', validators=[DataRequired(),Regexp("^\d{4}$",message="请输入有效的验证码")])
    session_id = StringField('Session ID', validators=[])
    submit = SubmitField('Submit')


    def validate_phone_num(self,field):
        if Account.query.filter_by(phone_num=field.data).first():
            raise ValidationError('Phone number already exists.')