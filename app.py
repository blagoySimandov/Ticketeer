from flask import Flask, render_template, redirect,session,redirect,url_for,g
from flask_session import Session
from app.forms.signup import SignUpForm,LogInForm
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from sassutils.wsgi import SassMiddleware
from flask import Flask
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "generate_random_string(10)"

    app.wsgi_app = SassMiddleware(
        app.wsgi_app,
        {
            'app': {
                'sass_path': 'static/sass',
                'css_path': 'static/css',
                'wsgi_path': '/static/css',
                'strip_extension': False
            }
        }
    )
    @app.before_request
    def load_logged_in_user():
        g.user = session.get("user_id",None)
    from .views import auth,post
    app.register_blueprint(auth.bp)
    app.register_blueprint(post.bp)
    return app
app = create_app()
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


