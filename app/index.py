from flask import render_template, jsonify
from flask_login import current_user
import datetime
import json
from decimal import *
from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)

@bp.route('/index')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None

    # response_body = {
    #     "products": avail_products,
    #     "purchases":purchasehistory
    # }
    
    # return {
    #     "products": avail_products,
    #     "purchases": purchasehistory
    # }
    # render the page by adding information to the index.html file
    return render_template('index.html',
                            product=avail_products,purchases=purchasehistory)
    #json.dumps(list(map(lambda x: x.__dict__,products)),cls=DecimalEncoder)

