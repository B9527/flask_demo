# coding:utf-8
from flask import render_template, redirect, flash, request, url_for
from os import path
from werkzeug.utils import secure_filename



def init_views(app):
    @app.route('/')
    def index():
        return render_template('index01.html', title='welcome', body='## header2')

    @app.route('/service')
    def service():
        return 'service'

    @app.route('/about')
    def about():
        return 'about'

    @app.route('/user/<username>')
    def user(username):
        return 'User: %s' % username

    # 定义传参数类型
    @app.route('/user_id/<int:user_id>')
    def user_id(user_id):
        return 'User: %s' % user_id

    # 增加正则定义路由
    @app.route('/regex/<regex("[a-z]{3}"):user_id>')
    def regex(user_id):
        return "User: %s" % user_id

    # 多路由对应一个
    @app.route('/projects/')
    @app.route('/project/')
    def project():
        return 'This is a project!'

    # 服务器上下文请求处理
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        from app.forms import LoginForm
        flash(u'登录成功')
        form = LoginForm()
        return render_template('login.html', title=u'登录', form=form)

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
            f = request.files['file']
            basepath = path.abspath(path.dirname(__file__))
            upload_path = path.join(basepath, 'static/uploads')
            f.save(path.join(upload_path, secure_filename(f.filename)))
            return redirect(url_for('upload'))
        return render_template('upload.html')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404



    @app.route('/base')
    def base():
        return render_template('base.html', title='welcome', body='## header2')

    @app.template_filter('md')
    def markdown_to_html(txt):
        from markdown import markdown
        return markdown(txt)

    def read_md(filename):
        with open(filename) as md_file:
            content = reduce(lambda x, y: x + y, md_file.readlines())
        return content.decode('utf-8')

    @app.context_processor
    def inject_methods():
        return dict(read_md=read_md)

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path
