from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
DB_NAME = 'example-dev.db'

app.config['SECRET_KEY'] = 'ebf217de553d09b6c3187a6b74e2a488'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

"""
    register blueprints
"""
from example.main.routes import main_bp
from example.user.routes import user_bp

app.register_blueprint(main_bp)
app.register_blueprint(user_bp)

"""
    flask-login
"""
from example.user.models import User

login_manager.login_view = 'user.login'
# login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

"""
    DB creation
"""
with app.app_context():
    db.create_all()

"""
    error handlers
"""

@app.errorhandler(403)
def forbidden_page(error):
    render_template('errors/403.html'), 403