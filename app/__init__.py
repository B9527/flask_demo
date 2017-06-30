# coding:utf-8

from os import path
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from werkzeug.routing import BaseConverter
from flask_sqlalchemy import SQLAlchemy
from .views import init_views


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


basedir = path.abspath(path.dirname(__file__))
bootstrap = Bootstrap()
nav = Nav()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///' + path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config.from_pyfile('config')
    nav.register_element('top', Navbar(u'Flask入门',
                                       View(u'主页', 'index'), View(u'关于', 'about'),
                                       View(u'服务', 'service'), View(u'项目', 'project'),

                                       ))
    db.init_app(app)
    bootstrap.init_app(app)
    nav.init_app(app)
    init_views(app)
    return app
