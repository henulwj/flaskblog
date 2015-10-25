# _*_ coding:utf-8 _*_

import sys, os

reload(sys)
sys.setdefaultencoding('utf-8')
# 获取当前项目路径
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # flask-wtf设置的表单密钥，用来验证CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hello world'
    # 每次请求结束后自动提交数据库中的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKBLOG_MAIL_SUBJECT_PREFIX = '[FLASKBLOG]-'
    FLASKBLOG_MAIL_SENDER = 'henulwj@sina.com'
    FLASKBLOG_ADMIN = 'henulwj@qq.com'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUGE = True
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 25
    # MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}