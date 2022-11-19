from flask import Flask

def create_app(test_config=None):
    #configuration of the project
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.cfg', silent=True)
    from src.views.home import home
    from src.views.auth import auth
    from src.views.details import details
    from src.views.cart import cart
    from src.views.product import product
    from src.views.payment import payment
    app.register_blueprint(home,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/auth/') 
    app.register_blueprint(details,url_prefix='/details/')
    app.register_blueprint(cart,url_prefix="/cart/")
    app.register_blueprint(product,url_prefix="/product/")
    app.register_blueprint(payment,url_prefix="/payment/")
    return app
    