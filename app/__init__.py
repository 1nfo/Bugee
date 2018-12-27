import logging
import sys
from uuid import uuid4

from flask import Flask

from core.settings import settings
from .api import bp as reset_bp
from .view import bp as view_bp, login_manager

app = Flask(__name__, **{k: v for k, v in settings.flask_setting.items()})

app.logger.addHandler(logging.StreamHandler(sys.stdout))

app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    SECRET_KEY=str(uuid4()),
)

login_manager.init_app(app)

app.register_blueprint(view_bp)
app.register_blueprint(reset_bp)
