from sassutils.wsgi import SassMiddleware
from flask import Flask
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
