# 　_*_ coding:utf-8 _*_
# encoding = utf-8
import sys, os
from datetime import datetime
from threading import Thread

from flask import Flask, request, current_app, g, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired  # Require将过期
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import  Migrate, MigrateCommand
from flask.ext.mail import Mail, Message

reload(sys)
sys.setdefaultencoding('utf-8')
# 获取当前项目路径
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# flask-wtf设置的表单密钥，用来验证CSRF
app.config["SECRET_KEY"] = "hello world"
# 配置数据库路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# 每次请求结束后自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['MAIL_SERVER'] = 'smtp.sina.com'
app.config['MAIL_PORT'] = 25
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

app.config['FLASKBLOG_MAIL_SUBJECT_PREFIX'] = '[FLASKBLOG]'
app.config['FLASKBLOG_MAIL_SENDER'] = 'henulwj@sina.com'
app.config['FLASKBLOG_ADMIN'] = 'henulwj@qq.com'



manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKBLOG_MAIL_SUBJECT_PREFIX']+subject, sender=app.config['FLASKBLOG_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


class NameForm(Form):
    name = StringField("姓名：", validators=[DataRequired()])
    submit = SubmitField("提交")


class Role(db.Model):

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __str__(self):
        return '<Role %r>' % self.name

    __repr__ = __str__

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __str__(self):
        return '<User %r>' % self.username

    __repr__ = __str__


@app.route('/', methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data, role_id=3)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKBLOG_ADMIN']:
                send_mail(app.config['FLASKBLOG_ADMIN'], '新用户', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), known = session.get('known', False))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    manager.run()
