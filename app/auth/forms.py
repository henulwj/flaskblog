# _*_ coding:utf-8 _*_

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User


class LoginFrom(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1,64), Email('邮箱地址有误')])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我？')
    submit = SubmitField('登录')


class RegistrationForm(Form):
    username = StringField('用户名', validators=[DataRequired(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, "用户名由数字、字母、_、.组成")])
    email = StringField('邮箱', validators=[DataRequired(), Length(1,64), Email('邮箱地址有误')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message="两次输入密码必须相同")])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册')


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message="两次输入密码必须相同")])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('修改密码')


class PasswordResetRequestForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1,64), Email('邮箱地址有误')])
    submit = SubmitField('发送邮件')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('邮箱还未注册')


class PasswordResetForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),Email('邮箱地址有误')])
    password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='两次输入密码必须相同')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('邮箱还未注册')


class ChangeEmailForm(Form):
    email = StringField('新邮箱', validators=[DataRequired(), Length(1, 64), Email('邮箱地址有误')])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('更新邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册')


