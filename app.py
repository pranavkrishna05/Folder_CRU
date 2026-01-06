import logging
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from backend.controllers.auth.auth_controller import auth_bp
from backend.controllers.products.products_controller import products_bp
from backend.controllers.cart.cart_controller import cart_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

logging.basicConfig(level=logging.INFO)

@app.before_request
def before_request():
    g.db = db.session

@app.teardown_request
def teardown_request(exception=None):
    db.session.remove()

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(cart_bp, url_prefix='/cart')

if __name__ == '__main__':
    app.run(debug=True)