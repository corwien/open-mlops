from flask import Flask

from .data import data
from .routes import api_routes, ui_routes, error_routes

from flask_cors import CORS

app = Flask(__name__, static_url_path="")

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'hard to guess string'

app.register_blueprint(api_routes, url_prefix="/")
app.register_blueprint(error_routes, url_prefix="/")
app.register_blueprint(ui_routes, url_prefix="/")

#data.init_database()
