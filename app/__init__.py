from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)
    
    from .carts import bp as cart_bp
    app.register_blueprint(cart_bp)
    
    from .purchases import bp as purchase_bp
    app.register_blueprint(purchase_bp)

    from .feedback import bp as feedback_bp
    app.register_blueprint(feedback_bp)

    from .inventories import bp as inventory_bp
    app.register_blueprint(inventory_bp)


    from .products import bp as products_bp
    app.register_blueprint(products_bp)


    return app
