# _*_ coding:utf-8 _*_

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError

from ..models import Role, User


class EditProfileForm(Form):
    name = StringField('真实姓名', validators=[Length(0,64)])
    location = StringField('地址', validators=[Length(0,64)])
    about_me = TextAreaField('个人介绍', validators=[Length(0,200)])
    submit = SubmitField('提交修改')


class EditProfileAdminForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1,64), Email('邮箱地址有误')])
    username = StringField('用户名', validators=[DataRequired(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, "用户名由数字、字母、_、.组成")])
    confirmed = BooleanField('激活状态')
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(0,64)])
    location = StringField('地址', validators=[Length(0,64)])
    about_me = TextAreaField('个人介绍', validators=[Length(0,200)])
    submit = SubmitField('提交修改')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user


    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已注册')


