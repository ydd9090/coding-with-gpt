from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Regexp
from wtforms.fields import StringField,SubmitField,SelectField,TextAreaField
from wtforms import ValidationError
from .models import Account
from flask_codemirror.fields import CodeMirrorField
from flask import current_app
import json


class AccountForm(FlaskForm):
    phone_num = StringField('Phone Number', validators=[DataRequired(),Regexp("^\d{11}$",message="请输入有效的手机号码")])
    phone_code = StringField('Phone Code', validators=[DataRequired(),Regexp("^\d{4}$",message="请输入有效的验证码")])
    session_id = StringField('Session ID', validators=[])
    submit = SubmitField('Submit')


    def validate_phone_num(self,field):
        if Account.query.filter_by(phone_num=field.data).first():
            raise ValidationError('Phone number already exists.')
        

class DiffForm(FlaskForm):
    text_from = SelectField('Request Type', choices=[(1,"Bytest request"),(2,"Bytediff request")])
    text = TextAreaField('Request Text',validators=[DataRequired()],render_kw={"rows": 10, "cols": 100})
    base_env = StringField('基准环境',default="prod_env", validators=[DataRequired()])
    test_env = StringField('测试环境', default="test_env",validators=[DataRequired()])
    submit = SubmitField('Submit')


    def validate_text(self,field):
        if self.text_from.data == "1":
            try:
                d = eval(field.data)
            except Exception as e:
                raise ValidationError("Bytest数据格式校验错误:{}".format(e))
        elif self.text_from.data == "2":
            try:
                json.loads(field.data)
            except Exception as e:
                raise ValidationError("Bytediff数据格式校验错误:{}".format(e))
