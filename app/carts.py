from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('carts', __name__)


@bp.route('/carts')
def carts():
    # get all available products for sale:
    #uid=keyboard input field
    products = Cart.get(1)
    # find the products current user has bought:
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                           printprods = products)
