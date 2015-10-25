# _*_ coding:utf-8 _*_

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(Form):
    name = StringField("姓名：", validators=[DataRequired()])
    submit = SubmitField("提交")

